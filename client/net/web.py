"""The browser transport (M12, docs/WEB_BUILD.md): the same interface as client/net/rest.py
and client/net/ws_client.py, for the pygbag web build, where there are no threads, no raw
sockets and no httpx.

A few lines of JavaScript (JS below, installed once into the page) do the real work with the
browser's own `fetch` and `WebSocket` and keep what came back in plain arrays. The game loop
drains them once per frame in `poll()`, exactly where the desktop version drains its queues,
so no scene can tell the two apart.

One trap of pygbag's bridge, found by testing: text going from Python to JavaScript loses its
accents (UTF-8 read as Latin-1), while text coming back is fine. So everything sent to JS here
is ASCII: JSON with \\u escapes, and URLs percent-encoded.

Nothing here runs on the desktop; the tests drive it through a fake bridge.
"""
from __future__ import annotations

import json
import time
from urllib.parse import parse_qs, quote

from .rest import NETWORK_ERROR, Api, ApiError, _Job, response_result
from .ws_client import CONNECTING, OFFLINE, ONLINE, STOPPED, WsClient

JS = r"""
(function () {
  if (window.kvtt) return;
  const K = {done: [], socks: {}, n: 0};
  K.req = function (id, method, url, headers, body, timeoutMs) {
    const ctl = new AbortController();
    let late = false;
    const timer = setTimeout(function () { late = true; ctl.abort(); }, timeoutMs);
    const opts = {method: method, headers: JSON.parse(headers), signal: ctl.signal};
    if (body) opts.body = body;
    fetch(url, opts).then(function (r) {
      return r.text().then(function (text) {
        clearTimeout(timer);
        K.done.push({id: id, status: r.status, text: text});
      });
    }).catch(function (e) {
      clearTimeout(timer);
      K.done.push({id: id, status: 0, text: "", timeout: late, error: String(e)});
    });
  };
  K.take = function () {
    if (!K.done.length) return "";
    const s = JSON.stringify(K.done);
    K.done = [];
    return s;
  };
  K.wsOpen = function (url) {
    const id = ++K.n;
    const s = {q: [], ws: null};
    K.socks[id] = s;
    try {
      const ws = new WebSocket(url);
      s.ws = ws;
      ws.onopen = function () { s.q.push('{"t":"_open"}'); };
      ws.onmessage = function (e) { if (typeof e.data === "string") s.q.push(e.data); };
      ws.onclose = function (e) { s.q.push(JSON.stringify({t: "_closed", code: e.code})); };
    } catch (e) {
      s.q.push('{"t":"_closed","code":0}');
    }
    return id;
  };
  K.wsSend = function (id, text) {
    const s = K.socks[id];
    if (s && s.ws && s.ws.readyState === 1) { s.ws.send(text); return 1; }
    return 0;
  };
  K.wsTake = function (id) {
    const s = K.socks[id];
    if (!s || !s.q.length) return "";
    const out = JSON.stringify(s.q);
    s.q = [];
    return out;
  };
  K.wsClose = function (id) {
    const s = K.socks[id];
    if (!s) return;
    try { if (s.ws) s.ws.close(); } catch (e) {}
    delete K.socks[id];
  };
  K.get = function (key) { try { return localStorage.getItem(key) || ""; } catch (e) { return ""; } };
  K.set = function (key, value) { try { localStorage.setItem(key, value); } catch (e) {} };
  window.kvtt = K;
})();
"""

# Phones (M12): a canvas never raises the on-screen keyboard and the game is played with keys,
# so on a touch screen (or with ?pad=1) the page gets a few HTML buttons that send the very key
# events a keyboard would: a D-pad (held = key held), Space (đánh), E, Enter, Esc, 1-6, and
# "⌨", which focuses a hidden text box so the phone's keyboard opens; what is typed there is
# forwarded to the game key by key (Vietnamese letters included), Backspace and Enter too.
TOUCH_JS = r"""
(function () {
  if (window.kvttPad) return;
  const cv = document.getElementById("canvas");
  const KEYS = {
    ArrowUp: 38, ArrowDown: 40, ArrowLeft: 37, ArrowRight: 39, " ": 32, e: 69, Enter: 13,
    Escape: 27, Backspace: 8, Tab: 9, "1": 49, "2": 50, "3": 51, "4": 52, "5": 53, "6": 54
  };
  function code(k) {
    if (k === " ") return "Space";
    if (/^[0-9]$/.test(k)) return "Digit" + k;
    if (/^[a-z]$/i.test(k)) return "Key" + k.toUpperCase();
    return k;
  }
  function ev(type, k, extra) {
    const kc = KEYS[k] || (k.length === 1 ? k.toUpperCase().charCodeAt(0) : 0);
    const o = Object.assign({key: k, code: code(k), keyCode: kc, which: kc, bubbles: true, cancelable: true}, extra || {});
    cv.dispatchEvent(new KeyboardEvent(type, o));
  }
  function down(k) { ev("keydown", k); }
  function up(k) { ev("keyup", k); }
  const queue = [];
  let busy = false;
  function pump() {          // one key every 90 ms: the game reads its input once per frame
    if (!queue.length) { busy = false; return; }
    busy = true;
    const k = queue.shift();
    if (k.length === 1 && k !== " " && KEYS[k] === undefined) {
      const cc = k.codePointAt(0);
      ev("keydown", k);
      ev("keypress", k, {charCode: cc, keyCode: cc, which: cc});
      ev("keyup", k);
    } else if (k.length === 1 && /[0-9 ]/.test(k)) {
      const cc = k.charCodeAt(0);
      ev("keydown", k);
      ev("keypress", k, {charCode: cc, keyCode: cc, which: cc});
      ev("keyup", k);
    } else {
      down(k); up(k);
    }
    setTimeout(pump, 90);
  }
  function tap(k) { queue.push(k); if (!busy) pump(); }

  const css = document.createElement("style");
  css.textContent = `
    #kvttpad { position: fixed; left: 0; right: 0; bottom: 0; height: 0; z-index: 50; pointer-events: none;
               font: bold 16px sans-serif; user-select: none; -webkit-user-select: none; touch-action: none; }
    #kvttpad button { pointer-events: auto; position: absolute; width: 52px; height: 52px; border-radius: 12px;
               border: 2px solid rgba(43,43,43,.7); background: rgba(244,235,217,.55); color: #2b2b2b;
               font: inherit; padding: 0; touch-action: none; }
    #kvttpad button:active, #kvttpad button.on { background: rgba(201,154,58,.8); }
    #kvtttext { position: fixed; left: -2000px; top: 0; width: 10px; height: 10px; opacity: 0; }
  `;
  document.head.appendChild(css);
  const pad = document.createElement("div");
  pad.id = "kvttpad";
  const B = 64;
  const layout = [
    ["▲", "ArrowUp", "left", B + 12, 2 * B + 12, true], ["▼", "ArrowDown", "left", B + 12, 12, true],
    ["◀", "ArrowLeft", "left", 12, B + 12, true], ["▶", "ArrowRight", "left", 2 * B + 12, B + 12, true],
    ["Đánh", " ", "right", 12, B + 12], ["E", "e", "right", B + 12, B + 12], ["↵", "Enter", "right", 12, 12],
    ["Esc", "Escape", "right", B + 12, 12], ["⌨", "kbd", "right", 2 * B + 12, 12],
    ["1", "1", "right", 12, 2 * B + 12], ["2", "2", "right", B + 12, 2 * B + 12], ["3", "3", "right", 2 * B + 12, 2 * B + 12]
  ];
  const text = document.createElement("input");
  text.id = "kvtttext";
  text.setAttribute("autocomplete", "off");
  text.setAttribute("autocapitalize", "off");
  text.setAttribute("autocorrect", "off");
  text.setAttribute("spellcheck", "false");
  document.body.appendChild(text);
  text.addEventListener("beforeinput", function (e) {
    if (e.inputType === "deleteContentBackward") tap("Backspace");
    else if (e.inputType === "insertLineBreak") tap("Enter");
    else if (e.data) for (const ch of e.data) tap(ch);
    e.preventDefault();
  });
  text.addEventListener("keydown", function (e) {
    if (e.key === "Enter" || e.key === "Backspace" || e.key === "Tab") { tap(e.key); e.preventDefault(); }
  });
  for (const [label, k, side, x, y, held] of layout) {
    const b = document.createElement("button");
    b.textContent = label;
    b.style[side] = x + "px";
    b.style.bottom = y + "px";
    if (k === "kbd") {
      b.addEventListener("pointerdown", function (e) {
        e.preventDefault();
        if (document.activeElement === text) { text.blur(); b.classList.remove("on"); }
        else { text.focus(); b.classList.add("on"); }
      });
    } else if (held) {
      b.addEventListener("pointerdown", function (e) { e.preventDefault(); b.setPointerCapture(e.pointerId); down(k); });
      b.addEventListener("pointerup", function (e) { e.preventDefault(); up(k); });
      b.addEventListener("pointercancel", function () { up(k); });
    } else {
      b.addEventListener("pointerdown", function (e) { e.preventDefault(); tap(k); });
    }
    pad.appendChild(b);
  }
  document.body.appendChild(pad);
  window.kvttPad = pad;
})();
"""

_bridge = None          # window.kvtt in the browser; tests put a fake here


def bridge():
    global _bridge
    if _bridge is None:
        import platform     # pygbag's platform module: platform.window is the page's window
        platform.window.eval(js_source(JS))
        _bridge = platform.window.kvtt
    return _bridge


def js_source(src: str) -> str:
    """JavaScript source made ASCII-only (\\u escapes) so it survives pygbag's bridge; every
    non-ASCII character in JS/TOUCH_JS sits inside a string literal, where escapes mean the same."""
    return src.encode("ascii", "backslashreplace").decode("ascii")


def install_touch_controls() -> bool:
    """Show TOUCH_JS's buttons on a touch screen, or anywhere with ?pad=1 (?pad=0 hides them)."""
    import platform
    want = page_query("pad")
    try:
        coarse = bool(platform.window.matchMedia("(pointer: coarse)").matches)
    except Exception:
        coarse = False
    if want == "0" or not (want == "1" or coarse):
        return False
    platform.window.eval(js_source(TOUCH_JS))
    return True


def _ascii(obj) -> str:
    return json.dumps(obj, ensure_ascii=True, separators=(",", ":"))


def _url(url: str) -> str:
    return quote(url, safe=":/?&=#%+@,;~!$'()*[]")


# ------------------------------------------------------------------ the page
def location():
    import platform
    return platform.window.location


def page_query(name: str) -> str:
    """`?server=...` and the like from the page's address ("" when absent)."""
    try:
        vals = parse_qs(str(location().search).lstrip("?")).get(name)
    except Exception:
        return ""
    return vals[0].strip() if vals else ""


def default_server(port: int = 8000) -> str:
    """Where the game server is when nobody said: the page's own origin when the game server
    itself handed the page out (at /web/, the way docs/WEB_BUILD.md recommends: same origin,
    nothing for the browser to block), else port 8000 of the machine that served the page."""
    try:
        loc = location()
        proto, host = str(loc.protocol) or "http:", str(loc.hostname) or "127.0.0.1"
        if str(loc.pathname).startswith("/web"):
            return str(loc.origin)
    except Exception:
        proto, host = "http:", "127.0.0.1"
    return f"{proto}//{host}:{port}"


def storage_get(key: str) -> str:
    """localStorage: what the desktop keeps in config.json / session.json survives a reload."""
    try:
        return str(bridge().get(key) or "")
    except Exception:
        return ""


def storage_set(key: str, data: dict) -> None:
    try:
        bridge().set(key, _ascii(data))
    except Exception:
        pass


def report_fps(fps: float, frame_ms: float) -> None:
    """Frames per second, and the milliseconds one frame of the game itself takes (what a
    hidden, throttled tab cannot distort), readable as window.kvtt_fps / kvtt_frame_ms."""
    try:
        import platform
        platform.window.kvtt_fps = round(fps, 1)
        platform.window.kvtt_frame_ms = round(frame_ms, 1)
    except Exception:
        pass


# ------------------------------------------------------------------ REST
class WebApi(Api):
    """client/net/rest.py's Api over the browser's fetch: same requests, retries, timeouts,
    error codes and callbacks (run in poll())."""

    def _start_worker(self) -> None:
        self._inflight: dict[int, tuple[_Job, int]] = {}
        self._retry: list[tuple[float, _Job, int]] = []
        self._next_id = 0

    def request(self, method: str, path: str, body: dict | None = None, on_ok=None, on_err=None,
                raw: bool = False, retries: int = 2, timeout: float = 10.0) -> None:
        self.pending += 1
        self._send(_Job(method.upper(), path, body, on_ok, on_err, raw, retries, timeout), 0)

    def _send(self, job: _Job, attempt: int) -> None:
        external = job.path.startswith("http")
        url = job.path if external else self.base_url + job.path
        headers = {"Authorization": f"Bearer {self.token}"} if self.token and not external else {}
        body = ""
        if job.body is not None:
            headers["Content-Type"] = "application/json"
            body = _ascii(job.body)
        self._next_id += 1
        self._inflight[self._next_id] = (job, attempt)
        bridge().req(self._next_id, job.method, _url(url), _ascii(headers), body, int(job.timeout * 1000))

    def poll(self) -> None:
        raw = bridge().take()
        for r in json.loads(str(raw)) if raw else []:
            job, attempt = self._inflight.pop(r["id"], (None, 0))
            if job is None:
                continue
            if r["status"]:
                ok, payload = response_result(r["status"], r["text"].encode("utf-8"), job.raw)
                self._deliver(job, ok, payload)
            elif attempt < job.retries:     # network error: try again a little later, like the desktop
                self._retry.append((time.monotonic() + 0.4 * (attempt + 1), job, attempt + 1))
            else:
                msg = ("Máy chủ phản hồi chậm (có thể đang khởi động), chờ một chút..." if r.get("timeout")
                       else "Mất kết nối máy chủ, đang thử lại...")
                self._deliver(job, False, ApiError(0, NETWORK_ERROR, msg))
        if self._retry:
            now = time.monotonic()
            due = [x for x in self._retry if x[0] <= now]
            self._retry = [x for x in self._retry if x[0] > now]
            for _, job, attempt in due:
                self._send(job, attempt)

    def close(self) -> None:
        self._stop = True


# ------------------------------------------------------------------ WebSocket
class WebWsClient(WsClient):
    """client/net/ws_client.py's WsClient over the browser's WebSocket: hello on open,
    heartbeat, reconnect with backoff, stop for good on the same fatal errors. All of it
    happens in poll(), once per frame."""

    OPEN_TIMEOUT = 10.0

    def __init__(self, http_url: str, token: str, version: int, heartbeat: float = 15.0,
                 start: bool = True):
        super().__init__(http_url, token, version, heartbeat, start=False)
        self._sock: int | None = None
        self._closed = False
        self._backoff = 1.0
        self._retry_at = 0.0
        self._opened_at = 0.0
        self._last_send = 0.0
        if start:
            self._connect()

    def _connect(self) -> None:
        self.state = CONNECTING
        self._opened_at = self._last_send = time.monotonic()
        self._sock = int(bridge().wsOpen(_url(self.url)))

    def _raw_send(self, msg: dict) -> bool:
        if self._sock is None or not bridge().wsSend(self._sock, _ascii(msg)):
            return False
        self._last_send = time.monotonic()
        self.sent += 1
        return True

    def send(self, msg: dict) -> bool:
        if self.state != ONLINE:
            return False
        return self._raw_send(msg)

    def poll(self) -> list[dict]:
        now = time.monotonic()
        if self._closed:
            return super().poll()
        if self._sock is None:
            if not self.stop_reason and now >= self._retry_at:
                self._connect()
            return super().poll()
        raw = bridge().wsTake(self._sock)
        for text in json.loads(str(raw)) if raw else []:
            try:
                m = json.loads(text)
            except ValueError:
                continue
            t = m.get("t") if isinstance(m, dict) else None
            if t == "_open":
                self._raw_send({"t": "hello", "v": self.version, "token": self.token})
            elif t == "_closed":
                self._lost()
                break
            elif t is not None:
                self._on_message(m)
        if self._sock is not None:
            if self.state == ONLINE and now - self._last_send >= self.heartbeat:
                self._raw_send({"t": "ping", "c": now})
            elif self.state == CONNECTING and now - self._opened_at > self.OPEN_TIMEOUT:
                self._lost()
        return super().poll()

    def _lost(self) -> None:
        was_online = self.state == ONLINE
        if self._sock is not None:
            bridge().wsClose(self._sock)
            self._sock = None
        if self._closed or self.stop_reason:
            self.state = STOPPED
            return
        if was_online:
            self._backoff = 1.0
        self.state = OFFLINE
        self.inbox.put({"t": "_offline"})
        self._retry_at = time.monotonic() + self._backoff
        self._backoff = min(30.0, self._backoff * 2)

    def close(self) -> None:
        self._closed = True
        if self._sock is not None:
            bridge().wsClose(self._sock)
            self._sock = None
        self.state = STOPPED
