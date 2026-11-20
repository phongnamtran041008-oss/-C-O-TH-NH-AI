"""M12, the browser build (docs/WEB_BUILD.md), tested headlessly on the desktop: the fetch and
WebSocket transport through a fake JavaScript bridge, the in-process runner for programming
exercises, config/session kept in localStorage, the thread shim, and the build's staging."""
from __future__ import annotations

import json
import sys
import threading
import types
from pathlib import Path

import pytest

from client import config as cfgmod
from client.engine import coderun
from client.net import rest, transport, web
from client.net.ws_client import CONNECTING, OFFLINE, ONLINE, STOPPED

ROOT = Path(__file__).resolve().parents[2]


class FakeBridge:
    """window.kvtt as the JS in client/net/web.py builds it."""

    def __init__(self):
        self.reqs: list[dict] = []
        self.done: list[dict] = []
        self.socks: dict[int, dict] = {}
        self.n = 0
        self.store: dict[str, str] = {}

    # fetch
    def req(self, rid, method, url, headers, body, timeout_ms):
        for s in (url, headers, body):
            assert s.isascii(), s          # pygbag's bridge mangles non-ASCII on the way to JS
        self.reqs.append({"id": rid, "method": method, "url": url, "headers": json.loads(headers),
                          "body": json.loads(body) if body else None, "timeout": timeout_ms})

    def answer(self, rid, status, data=None, text=None, timeout=False):
        self.done.append({"id": rid, "status": status, "timeout": timeout,
                          "text": text if text is not None else ("" if data is None else json.dumps(data))})

    def take(self):
        out, self.done = self.done, []
        return json.dumps(out) if out else ""

    # WebSocket
    def wsOpen(self, url):
        assert url.isascii()
        self.n += 1
        self.socks[self.n] = {"url": url, "q": [], "sent": [], "open": False, "closed": False}
        return self.n

    def wsSend(self, sid, text):
        s = self.socks.get(sid)
        assert text.isascii()
        if not s or not s["open"]:
            return 0
        s["sent"].append(json.loads(text))
        return 1

    def wsTake(self, sid):
        s = self.socks.get(sid)
        if not s or not s["q"]:
            return ""
        out, s["q"] = s["q"], []
        return json.dumps(out)

    def wsClose(self, sid):
        if sid in self.socks:
            self.socks[sid]["closed"] = True

    # server side helpers
    def opened(self, sid):
        self.socks[sid]["open"] = True
        self.socks[sid]["q"].append('{"t":"_open"}')

    def push(self, sid, msg):
        self.socks[sid]["q"].append(json.dumps(msg, ensure_ascii=False))

    def drop(self, sid):
        self.socks[sid]["open"] = False
        self.socks[sid]["q"].append('{"t":"_closed","code":1006}')

    # localStorage
    def get(self, key):
        return self.store.get(key, "")

    def set(self, key, value):
        assert value.isascii()
        self.store[key] = value


@pytest.fixture
def bridge(monkeypatch):
    b = FakeBridge()
    monkeypatch.setattr(web, "_bridge", b)
    return b


class Clock:
    def __init__(self):
        self.t = 1000.0

    def __call__(self):
        return self.t


@pytest.fixture
def clock(monkeypatch):
    c = Clock()
    monkeypatch.setattr(web.time, "monotonic", c)
    return c


# ------------------------------------------------------------------ shared answer parsing
def test_response_result_matches_the_desktop_rules():
    assert rest.response_result(200, b'{"a": 1}') == (True, {"a": 1})
    assert rest.response_result(204, b"") == (True, {})
    assert rest.response_result(200, b"raw", raw=True) == (True, b"raw")
    ok, err = rest.response_result(409, json.dumps({"error": {"code": "taken", "message_vi": "Đã có"}}).encode())
    assert not ok and (err.status, err.code, err.message_vi) == (409, "taken", "Đã có")
    ok, err = rest.response_result(400, b'{"error": {"code": 400, "message": "EMAIL_EXISTS : x"}}')
    assert err.code == "EMAIL_EXISTS"                    # Firebase's numeric codes
    assert rest.response_result(503, b"<html>")[1].code == rest.SLEEPING
    assert rest.response_result(500, b"<html>")[1].code == "error"


# ------------------------------------------------------------------ REST over fetch
def test_web_api_sends_ascii_json_with_the_token_and_runs_callbacks_in_poll(bridge):
    api = web.WebApi("192.168.1.5:8000", "tok")
    got = []
    api.post("/character/create", {"display_name": "Tiêu Dao"}, got.append)
    r = bridge.reqs[-1]
    assert r["url"] == "http://192.168.1.5:8000/character/create" and r["method"] == "POST"
    assert r["headers"] == {"Authorization": "Bearer tok", "Content-Type": "application/json"}
    assert r["body"] == {"display_name": "Tiêu Dao"} and r["timeout"] == 10000
    assert api.pending == 1 and not got
    bridge.answer(r["id"], 200, {"ok": True, "tên": "Tiêu Dao"})
    api.poll()
    assert got == [{"ok": True, "tên": "Tiêu Dao"}] and api.pending == 0


def test_web_api_external_urls_get_no_token(bridge):
    api = web.WebApi("http://x:8000", "tok")
    api.get("https://example.com/list.json")
    assert bridge.reqs[-1]["headers"] == {} and bridge.reqs[-1]["body"] is None


def test_web_api_retries_network_errors_then_reports_offline(bridge, clock):
    api = web.WebApi("http://x:8000")
    errs = []
    api.get("/me", None, errs.append, retries=1)
    bridge.answer(bridge.reqs[-1]["id"], 0)
    api.poll()
    assert len(bridge.reqs) == 1 and not errs          # waits before trying again
    clock.t += 1
    api.poll()
    assert len(bridge.reqs) == 2
    bridge.answer(bridge.reqs[-1]["id"], 0, timeout=True)
    api.poll()
    assert errs[0].code == rest.NETWORK_ERROR and "chậm" in errs[0].message_vi
    assert api.offline and api.pending == 0
    api.get("/me")
    bridge.answer(bridge.reqs[-1]["id"], 200, {})
    api.poll()
    assert not api.offline


def test_web_api_401_logs_out_except_on_the_login_itself(bridge):
    api = web.WebApi("http://x:8000", "old")
    hits = []
    api.on_unauthorized = lambda: hits.append(1)
    api.post("/auth/login", {"username": "a", "password": "b"}, None, lambda e: None)
    bridge.answer(bridge.reqs[-1]["id"], 401, {"error": {"code": "bad_login", "message_vi": "Sai"}})
    api.poll()
    assert hits == []
    api.get("/me", None, lambda e: None)
    bridge.answer(bridge.reqs[-1]["id"], 401, {"error": {"code": "bad_token"}})
    api.poll()
    assert hits == [1]


def test_web_api_percent_encodes_urls(bridge):
    web.WebApi("http://x:8000").get("/math/search?q=tập hợp")
    assert bridge.reqs[-1]["url"] == "http://x:8000/math/search?q=t%E1%BA%ADp%20h%E1%BB%A3p"


# ------------------------------------------------------------------ WebSocket
def test_web_ws_says_hello_goes_online_and_sends(bridge, clock):
    ws = web.WebWsClient("http://192.168.1.5:8000", "tok", 5)
    sid = 1
    assert bridge.socks[sid]["url"] == "ws://192.168.1.5:8000/ws" and ws.state == CONNECTING
    assert ws.send({"t": "chat", "text": "x"}) is False          # not online yet
    bridge.opened(sid)
    ws.poll()
    assert bridge.socks[sid]["sent"] == [{"t": "hello", "v": 5, "token": "tok"}]
    bridge.push(sid, {"t": "welcome", "you": {"uid": 7}})
    bridge.push(sid, {"t": "chat", "text": "Chào đạo hữu"})
    msgs = ws.poll()
    assert [m["t"] for m in msgs] == ["welcome", "chat"] and msgs[1]["text"] == "Chào đạo hữu"
    assert ws.online and ws.connected_once
    assert ws.send({"t": "chat", "text": "Xin chào"}) is True
    assert bridge.socks[sid]["sent"][-1] == {"t": "chat", "text": "Xin chào"}


def test_web_ws_heartbeat_and_pong(bridge, clock):
    ws = web.WebWsClient("http://x:8000", "tok", 5, heartbeat=15)
    bridge.opened(1)
    bridge.push(1, {"t": "welcome"})
    ws.poll()
    clock.t += 16
    ws.poll()
    ping = bridge.socks[1]["sent"][-1]
    assert ping["t"] == "ping"
    clock.t += 0.05
    bridge.push(1, {"t": "pong", "c": ping["c"]})
    ws.poll()
    assert ws.rtt == pytest.approx(0.05)


def test_web_ws_reconnects_with_backoff_after_a_drop(bridge, clock):
    ws = web.WebWsClient("http://x:8000", "tok", 5)
    bridge.opened(1)
    bridge.push(1, {"t": "welcome"})
    ws.poll()
    bridge.drop(1)
    msgs = ws.poll()
    assert ws.state == OFFLINE and {"t": "_offline"} in msgs and bridge.socks[1]["closed"]
    ws.poll()
    assert bridge.n == 1                       # waits a second first
    clock.t += 1.1
    ws.poll()
    assert bridge.n == 2 and ws.state == CONNECTING


def test_web_ws_open_timeout_counts_as_a_drop(bridge, clock):
    ws = web.WebWsClient("http://x:8000", "tok", 5)
    clock.t += web.WebWsClient.OPEN_TIMEOUT + 1
    ws.poll()
    assert ws.state == OFFLINE and bridge.socks[1]["closed"]


def test_web_ws_stops_for_good_on_a_fatal_error(bridge, clock):
    ws = web.WebWsClient("http://x:8000", "bad", 5)
    bridge.opened(1)
    bridge.push(1, {"t": "error", "code": "bad_token"})
    bridge.drop(1)
    ws.poll()
    assert ws.state == STOPPED and ws.stop_reason == "bad_token"
    clock.t += 100
    ws.poll()
    assert bridge.n == 1                       # never again


def test_web_ws_close(bridge, clock):
    ws = web.WebWsClient("http://x:8000", "tok", 5)
    ws.close()
    assert ws.state == STOPPED and bridge.socks[1]["closed"]
    clock.t += 100
    ws.poll()
    assert bridge.n == 1


# ------------------------------------------------------------------ which transport
def test_transport_picks_the_desktop_one_here():
    assert transport.IN_BROWSER is False
    api = transport.make_api("http://127.0.0.1:9")
    try:
        assert type(api) is rest.Api
    finally:
        api.close()


def test_transport_picks_the_browser_one_in_a_browser(bridge, monkeypatch):
    monkeypatch.setattr(transport, "IN_BROWSER", True)
    assert type(transport.make_api("http://x:8000")) is web.WebApi
    assert type(transport.make_ws("http://x:8000", "t", 5)) is web.WebWsClient


def test_threads_inline_shim_runs_the_target_at_once():
    T = threading.Thread
    original = T.start, T.is_alive, T.join
    try:
        transport.run_threads_inline()
        seen = []
        t = threading.Thread(target=lambda: seen.append(threading.current_thread().name), name="coderun")
        t.start()
        assert seen and not t.is_alive()
        t.join()                                   # a finished "thread" can be joined
    finally:
        T.start, T.is_alive, T.join = original


# ------------------------------------------------------------------ the page: config and session
class FakeLocation:
    def __init__(self, path="/", search="", host="192.168.1.5", port="8080"):
        self.protocol, self.hostname, self.pathname, self.search = "http:", host, path, search
        self.origin = f"http://{host}:{port}"


def test_default_server_is_the_page_origin_under_web_else_port_8000(monkeypatch):
    monkeypatch.setattr(web, "location", lambda: FakeLocation("/web/", port="8000"))
    assert web.default_server() == "http://192.168.1.5:8000"
    monkeypatch.setattr(web, "location", lambda: FakeLocation("/", port="8080"))
    assert web.default_server() == "http://192.168.1.5:8000"


def test_page_query(monkeypatch):
    monkeypatch.setattr(web, "location", lambda: FakeLocation(search="?server=http%3A%2F%2Fpc%3A8000&pad=1"))
    assert web.page_query("server") == "http://pc:8000" and web.page_query("pad") == "1"
    assert web.page_query("nope") == ""


def test_config_and_session_live_in_local_storage_in_a_browser(bridge, monkeypatch, tmp_path):
    monkeypatch.setattr(cfgmod, "IN_BROWSER", True)
    monkeypatch.setattr(web, "location", lambda: FakeLocation("/web/", port="8000"))
    shipped = tmp_path / "config.json"
    shipped.write_text(json.dumps({"server_url": "", "firebase_api_key": ""}), "utf-8")
    cfg = cfgmod.Config.load(shipped)
    assert cfg.server_url == "http://192.168.1.5:8000"      # nothing saved: the page's own server
    cfg.sfx_volume = 0.3
    cfg.server_url = "http://other:8000"
    cfg.save()
    again = cfgmod.Config.load(shipped)
    assert (again.sfx_volume, again.server_url) == (0.3, "http://other:8000")

    monkeypatch.setattr(cfgmod, "data_dir", lambda: tmp_path / "gone")   # the page's files vanish
    s = cfgmod.Session()
    assert s.web and s.data == {}
    s.save(token="abc", username="Tiêu Dao")
    assert json.loads(bridge.store[cfgmod.WEB_SESSION_KEY])["username"] == "Tiêu Dao"
    assert cfgmod.Session().token == "abc"                  # a reload logs straight back in


def test_desktop_session_never_touches_local_storage(tmp_path):
    s = cfgmod.Session(tmp_path / "s.json")
    assert not s.web
    s.save(token="x")
    assert json.loads((tmp_path / "s.json").read_text("utf-8"))["token"] == "x"


def test_js_goes_over_as_ascii():
    for src in (web.JS, web.TOUCH_JS):
        out = web.js_source(src)
        assert out.isascii()
    assert "\\u0110\\xe1nh" in web.js_source(web.TOUCH_JS) or "\\u0110" in web.js_source(web.TOUCH_JS)


# ------------------------------------------------------------------ programming exercises in-process
def test_in_process_run_reads_stdin_and_catches_prints():
    src = "n = int(input())\nxs = list(map(int, input().split()))\nprint(sum(xs[:n]))\nprint('xong')\n"
    r = coderun.run_in_process(src, "3\n1 2 3 4\n")
    assert r.status == coderun.OK and r.output == "6\nxong\n"
    assert sys.stdin is sys.__stdin__ or not isinstance(sys.stdin, type(None))


def test_in_process_run_reads_sys_stdin_too():
    r = coderun.run_in_process("import sys\nprint(sys.stdin.read().upper(), end='')", "abc")
    assert r.output == "ABC"


def test_in_process_runtime_error_gives_the_traceback_tail():
    r = coderun.run_in_process("print('a')\nx = 1 // 0\n", "")
    assert r.status == coderun.RE and r.output == "a\n" and "ZeroDivisionError" in r.error


def test_in_process_eof_is_a_runtime_error():
    r = coderun.run_in_process("input()\ninput()\n", "one line\n")
    assert r.status == coderun.RE and "EOFError" in r.error


def test_in_process_time_limit():
    r = coderun.run_in_process("while True:\n    pass\n", "", time_limit_ms=50)
    assert r.status == coderun.TLE and r.ms == 50


def test_in_process_exit_codes():
    assert coderun.run_in_process("import sys\nprint(1)\nsys.exit(0)\n", "").status == coderun.OK
    assert coderun.run_in_process("exit()\n", "").status == coderun.OK
    r = coderun.run_in_process("import sys\nsys.exit('hong')\n", "")
    assert r.status == coderun.RE and "hong" in r.error


def test_in_process_restores_the_interpreter():
    before = sys.stdin, sys.stdout, sys.stderr, sys.gettrace(), sys.getrecursionlimit()
    coderun.run_in_process("import sys\nsys.setrecursionlimit(50)\nraise SystemExit(2)\n", "")
    coderun.run_in_process("while True: pass\n", "", time_limit_ms=20)
    assert (sys.stdin, sys.stdout, sys.stderr, sys.gettrace(), sys.getrecursionlimit()) == before


def test_in_process_output_limit():
    r = coderun.run_in_process("print('x' * 1000)", "", max_output_chars=10)
    assert r.output == "x" * 10


def test_run_tests_uses_the_in_process_runner_in_a_browser(monkeypatch, tmp_path):
    monkeypatch.setattr(coderun, "IN_BROWSER", True)
    monkeypatch.setattr(coderun, "interpreter", lambda *a: pytest.fail("no subprocess in a browser"))
    path = coderun.write_solution(tmp_path / "bai.py", "a, b = map(int, input().split())\nprint(a + b)\n")
    att = coderun.run_tests(path, ["1 2\n", "5 5\n"])
    assert att.status == coderun.OK and att.outputs == ["3\n", "10\n"]
    assert coderun.run_tests(path, ["x\n"]).status == coderun.RE
    bad = coderun.write_solution(tmp_path / "bad.py", "def f(:\n")
    assert coderun.run_tests(bad, ["1\n"]).status == coderun.CE


# ------------------------------------------------------------------ the build
def test_build_stages_the_client_without_tests_or_player_files(tmp_path, monkeypatch):
    sys.path.insert(0, str(ROOT / "tools"))
    try:
        import build_web
    finally:
        sys.path.pop(0)
    monkeypatch.setattr(build_web, "STAGE", tmp_path / "toantutien")
    build_web.stage()
    st = tmp_path / "toantutien"
    assert (st / "main.py").read_text("utf-8") == (ROOT / "web" / "main.py").read_text("utf-8")
    assert (st / "client" / "main.py").exists() and (st / "client" / "net" / "web.py").exists()
    assert (st / "client" / "assets").is_dir()
    assert not (st / "client" / "tests").exists()
    assert not list(st.rglob("__pycache__")) and not list(st.rglob("session.json"))
    shipped = json.loads((st / "client" / "config.json").read_text("utf-8"))
    assert shipped["server_url"] == "" and shipped["firebase_api_key"] == ""


def test_web_main_entry_is_async():
    import inspect

    from client import main
    assert inspect.iscoroutinefunction(main.web_main)
    assert inspect.iscoroutinefunction(main.Game.run_async)
