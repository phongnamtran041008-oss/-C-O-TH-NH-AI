"""Non-blocking REST client (spec 15.5): requests run on a worker thread; results come
back through a queue and their callbacks run on the game thread in `poll()`.
Timeout 10 s, two retries on network errors, JSON errors become (code, message_vi)."""
from __future__ import annotations

import json
import queue
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass

NETWORK_ERROR = "network"
SLEEPING = "server_starting"


@dataclass
class ApiError:
    status: int
    code: str
    message_vi: str


@dataclass
class _Job:
    method: str
    path: str
    body: dict | None
    on_ok: Callable | None
    on_err: Callable | None
    raw: bool
    retries: int
    timeout: float


class Api:
    def __init__(self, base_url: str, token: str | None = None):
        from ..config import normalize_url
        self.base_url = normalize_url(base_url)
        self.token = token
        self._jobs: queue.Queue = queue.Queue()
        self._results: queue.Queue = queue.Queue()
        self.pending = 0
        self.offline = False
        self.on_unauthorized: Callable[[], None] | None = None
        self._stop = False
        self._start_worker()

    def _start_worker(self) -> None:
        self._thread = threading.Thread(target=self._worker, daemon=True, name="rest")
        self._thread.start()

    # ------------------------------------------------------------ public
    def request(self, method: str, path: str, body: dict | None = None, on_ok=None, on_err=None,
                raw: bool = False, retries: int = 2, timeout: float = 10.0) -> None:
        self.pending += 1
        self._jobs.put(_Job(method.upper(), path, body, on_ok, on_err, raw, retries, timeout))

    def get(self, path, on_ok=None, on_err=None, **kw):
        self.request("GET", path, None, on_ok, on_err, **kw)

    def post(self, path, body=None, on_ok=None, on_err=None, **kw):
        self.request("POST", path, body or {}, on_ok, on_err, **kw)

    def poll(self) -> None:
        """Run finished callbacks; call once per frame from the game loop."""
        while True:
            try:
                job, ok, payload = self._results.get_nowait()
            except queue.Empty:
                return
            self._deliver(job, ok, payload)

    def _deliver(self, job: _Job, ok: bool, payload) -> None:
        """Run one finished job's callback (game thread)."""
        self.pending -= 1
        if ok:
            self.offline = False
            if job.on_ok:
                job.on_ok(payload)
        else:
            err: ApiError = payload
            self.offline = err.code == NETWORK_ERROR
            if err.status == 401 and self.on_unauthorized and job.path not in ("/auth/login", "/auth/reset_password"):
                self.on_unauthorized()
            if job.on_err:
                job.on_err(err)

    def close(self) -> None:
        self._stop = True
        self._jobs.put(None)

    def set_base_url(self, url: str) -> None:
        from ..config import normalize_url
        self.base_url = normalize_url(url)

    # ------------------------------------------------------------ worker
    def _worker(self) -> None:
        import httpx    # here, not at the top: the browser build has no httpx (client/net/web.py)
        client = httpx.Client(timeout=10.0)
        while not self._stop:
            job = self._jobs.get()
            if job is None:
                break
            self._results.put(self._run(client, job))
        client.close()

    def _run(self, client: httpx.Client, job: _Job):
        import httpx
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        last_exc = None
        for attempt in range(job.retries + 1):
            try:
                url = job.path if job.path.startswith("http") else self.base_url + job.path
                r = client.request(job.method, url, json=job.body,
                                   headers=headers if not job.path.startswith("http") else {},
                                   timeout=job.timeout)
            except (httpx.TransportError, OSError) as e:
                last_exc = e
                time.sleep(0.4 * (attempt + 1))
                continue
            return (job, *response_result(r.status_code, r.content, job.raw))
        msg = "Mất kết nối máy chủ, đang thử lại..."
        if isinstance(last_exc, httpx.TimeoutException):
            msg = "Máy chủ phản hồi chậm (có thể đang khởi động), chờ một chút..."
        return job, False, ApiError(0, NETWORK_ERROR, msg)


def response_result(status: int, content: bytes, raw: bool = False) -> tuple[bool, object]:
    """(ok, payload) for an answer that arrived: its JSON (bytes when `raw`), or an ApiError.
    Shared by the desktop worker above and the browser transport (client/net/web.py)."""
    if status < 400:
        return True, (content if raw else (json.loads(content) if content else {}))
    try:
        e = json.loads(content).get("error", {})
        code = e.get("code", "error")
        if not isinstance(code, str):   # Google APIs (Firebase): {"code": 400, "message": "EMAIL_EXISTS"}
            code = str(e.get("message", "error")).split(" ")[0]
        return False, ApiError(status, code, e.get("message_vi", "Có lỗi xảy ra."))
    except ValueError:
        if status in (502, 503, 504):
            return False, ApiError(status, SLEEPING, "Máy chủ đang khởi động, chờ khoảng 1 phút...")
        return False, ApiError(status, "error", f"Lỗi máy chủ ({status}).")
