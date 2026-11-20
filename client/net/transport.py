"""Picks the network transport: the desktop one (httpx + websockets on threads, rest.py and
ws_client.py) or the browser one (fetch + WebSocket, web.py) for the pygbag web build (M12).
This is the only place that asks which one is running."""
from __future__ import annotations

import sys

IN_BROWSER = sys.platform == "emscripten"


def make_api(base_url: str, token: str | None = None):
    if IN_BROWSER:
        from .web import WebApi
        return WebApi(base_url, token)
    from .rest import Api
    return Api(base_url, token)


def make_ws(http_url: str, token: str, version: int):
    if IN_BROWSER:
        from .web import WebWsClient
        return WebWsClient(http_url, token, version)
    from .ws_client import WsClient
    return WsClient(http_url, token, version)


def threads_work() -> bool:
    import _thread
    try:
        _thread.start_new_thread(lambda: None, ())
        return True
    except RuntimeError:
        return False


def run_threads_inline() -> None:
    """pygbag's CPython cannot start threads. The one place a scene still starts one is the
    programming exercise (client/scenes/math_code.py runs the player's program on a worker
    thread); in the browser that program runs in-process anyway (client/engine/coderun.py),
    so the 'thread' simply runs at once, on the spot, and the scene finds its result on the
    next frame as usual. Only called by the web build, and only when threads really fail."""
    import threading
    Thread = threading.Thread
    alive, join = Thread.is_alive, Thread.join

    def start(self):
        self._kvtt_inline = True
        self._started.set()
        self.run()

    Thread.start = start
    Thread.is_alive = lambda self: False if getattr(self, "_kvtt_inline", False) else alive(self)
    Thread.join = lambda self, timeout=None: None if getattr(self, "_kvtt_inline", False) else join(self, timeout)
