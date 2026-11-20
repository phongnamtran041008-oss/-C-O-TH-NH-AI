"""M12: build and serve the browser version of the game (pygbag). See docs/WEB_BUILD.md.

    python tools/build_web.py                 # build into build/web/
    python tools/build_web.py serve           # build, then start the game server for the whole
                                              # Wi-Fi; it hands the game out at /web/ (port 8000)
    python tools/build_web.py serve --no-build
    python tools/build_web.py static --port 8080   # only the page, for a game server elsewhere

`serve` is the way to play on a phone: the page and the API come from the same address, so the
browser has nothing to block. A page served from another port has to call the server
cross-origin; that works on the PC itself, but a recent Chrome refuses it from a Wi-Fi address
(its "Local Network Access" rule), see docs/WEB_BUILD.md.

pygbag goes into its own virtual environment, .venv-web/ at the repository root (git-ignored),
created on the first build with the Python that runs this script; nothing is installed into
the game's own environment. The build needs the Internet once (pygbag and its page template);
the browser that opens the game needs it too, for pygbag's Python runtime (its CDN).

The build is: a copy of client/ (without tests or player files) plus web/main.py, packed by
pygbag; the copy gets a config.json with no server address, so the page talks to port 8000 of
the machine that served it (or to ?server=... in the page address).
"""
from __future__ import annotations

import argparse
import functools
import http.server
import json
import os
import shutil
import socket
import subprocess
import sys
import venv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENV = ROOT / ".venv-web"
STAGE = ROOT / "build" / "web_src" / "toantutien"      # the folder name becomes the package name
OUT = ROOT / "build" / "web"
PYGBAG = "pygbag==0.9.3"
APP_NAME = "toantutien"

# never shipped: tests, the player's own files, caches
SKIP_DIRS = {"tests", "__pycache__", "bai_lam", "worlds", ".pytest_cache"}
SKIP_FILES = {"config.json", "session.json", "toantutien_loi.txt", "toantutien_smoke.txt"}
SKIP_SUFFIX = {".pyc", ".pyo", ".bak", ".log", ".md"}

# what the page starts with; whatever the player changes in Cài đặt is kept in the browser
WEB_CONFIG = {
    "server_url": "",          # "" = http://<the machine that served the page>:8000
    "server_list_url": "",
    "firebase_api_key": "",    # LAN worlds cannot be opened from a web page
    "update_repo": "",
    "window_scale": 0,
    "fullscreen": False,
    "sfx_volume": 0.8,
}


def venv_python() -> Path:
    return VENV / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def ensure_pygbag() -> Path:
    py = venv_python()
    if not py.exists():
        print(f"[web] tạo môi trường riêng cho pygbag: {VENV}")
        venv.create(VENV, with_pip=True)
    ok = subprocess.run([str(py), "-c", "import pygbag"], capture_output=True).returncode == 0
    if not ok:
        print(f"[web] cài {PYGBAG} vào {VENV.name} ...")
        subprocess.run([str(py), "-m", "pip", "install", "-q", PYGBAG], check=True)
    return py


def _copy_client(dst: Path) -> tuple[int, int]:
    files = size = 0
    src = ROOT / "client"
    for folder, dirs, names in os.walk(src):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith("."))
        rel = Path(folder).relative_to(src)
        for name in names:
            p = Path(folder) / name
            if name in SKIP_FILES or p.suffix in SKIP_SUFFIX:
                continue
            target = dst / rel / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, target)
            files += 1
            size += p.stat().st_size
    return files, size


def stage() -> None:
    if STAGE.exists():
        shutil.rmtree(STAGE)
    STAGE.mkdir(parents=True)
    shutil.copy2(ROOT / "web" / "main.py", STAGE / "main.py")
    files, size = _copy_client(STAGE / "client")
    (STAGE / "client" / "config.json").write_text(json.dumps(WEB_CONFIG, indent=2), "utf-8")
    favicon = ROOT / "web" / "favicon.png"
    if favicon.exists():
        shutil.copy2(favicon, STAGE / "favicon.png")
    print(f"[web] đã chép {files} tệp của client ({size / 1e6:.1f} MB) vào {STAGE}")


def build() -> None:
    py = ensure_pygbag()
    stage()
    args = [str(py), "-m", "pygbag", "--build", "--app_name", APP_NAME, "--title", "Toan Tu Tien",
            "--ume_block", "1"]
    template = ROOT / "web" / "index.tmpl"
    if template.exists():
        args += ["--template", str(template)]
    if (STAGE / "favicon.png").exists():
        args += ["--icon", "favicon.png"]
    args.append(str(STAGE))
    print("[web] " + " ".join(args[1:]))
    r = subprocess.run(args, cwd=str(STAGE.parent), capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    if r.returncode != 0 or not (STAGE / "build" / "web" / "index.html").exists():
        print(r.stdout[-4000:], r.stderr[-4000:], sep="\n")
        sys.exit("[web] pygbag không đóng gói được, xem lỗi ở trên.")
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(STAGE / "build" / "web", OUT)
    for p in sorted(OUT.iterdir()):
        print(f"[web]   {p.name:<24} {p.stat().st_size / 1e6:6.2f} MB")
    print(f"[web] xong: {OUT}")


def lan_addresses() -> list[str]:
    found = []
    try:  # the address this PC would use to reach the Internet = its Wi-Fi address (nothing is sent)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        found.append(s.getsockname()[0])
        s.close()
    except OSError:
        pass
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET):
            ip = info[4][0]
            if ip not in found and not ip.startswith("127."):
                found.append(ip)
    except OSError:
        pass
    return found


class _Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map,
                      ".apk": "application/octet-stream", ".gz": "application/gzip",
                      ".js": "text/javascript", ".wasm": "application/wasm"}

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")    # a new build shows up on the next reload
        super().end_headers()


def _need_build() -> None:
    if not (OUT / "index.html").exists():
        sys.exit("[web] chưa có bản web: chạy  python tools/build_web.py  trước.")


def serve_game(port: int) -> int:
    """The game server on every address of this PC; it hands the build out at /web/."""
    _need_build()
    server = ROOT / "server"
    env_file, example = server / ".env", server / ".env.example"
    if not env_file.exists() and example.exists():
        shutil.copy2(example, env_file)          # what chay_server*.bat do too
    env = dict(os.environ, WEB_BUILD_DIR=str(OUT))
    print("=" * 66)
    print(" Máy chủ Toán Tu Tiên + bản web đang mở. Mở trình duyệt:")
    print(f"   Trên máy này:         http://127.0.0.1:{port}/web/")
    for ip in lan_addresses():
        print(f"   Điện thoại cùng Wi-Fi: http://{ip}:{port}/web/")
    print(" Windows hỏi tường lửa thì bấm \"Allow\" (Cho phép). Tắt: Ctrl+C")
    print("=" * 66)
    try:
        return subprocess.call([sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0",
                                "--port", str(port), "--proxy-headers"], cwd=str(server), env=env)
    except KeyboardInterrupt:
        return 0


def serve_static(port: int) -> None:
    """Only the page (a plain file server), for a game server that runs somewhere else."""
    _need_build()
    handler = functools.partial(_Handler, directory=str(OUT))
    httpd = http.server.ThreadingHTTPServer(("0.0.0.0", port), handler)
    print("=" * 66)
    print(" Chỉ có trang web, không có máy chủ game. Trang sẽ gọi máy chủ ở cổng 8000")
    print(" của máy đã mở trang, hoặc ở ?server=http://dia-chi:8000 thêm vào sau địa chỉ.")
    print(f"   Trên máy này:         http://127.0.0.1:{port}/")
    for ip in lan_addresses():
        print(f"   Cùng Wi-Fi:           http://{ip}:{port}/")
    print(" Điện thoại nên dùng  python tools/build_web.py serve  (cùng một địa chỉ với máy chủ).")
    print(" Tắt: Ctrl+C")
    print("=" * 66)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description="Bản web (pygbag) của Toán Tu Tiên")
    ap.add_argument("cmd", nargs="?", default="build", choices=["build", "serve", "static"])
    ap.add_argument("--port", type=int, help="serve: 8000, static: 8080")
    ap.add_argument("--no-build", action="store_true", help="serve/static: dùng bản đã build")
    a = ap.parse_args(argv)
    if a.cmd == "build" or not a.no_build:
        build()
    if a.cmd == "serve":
        sys.exit(serve_game(a.port or 8000))
    if a.cmd == "static":
        serve_static(a.port or 8080)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
