"""M12: what the server does for the browser build (docs/WEB_BUILD.md): CORS for a page served
from another address, and the build itself at /web/ when it has been built."""
import httpx
import pytest

from app.config import settings
from app.main import create_app


async def _get(app, method: str, url: str, **kw) -> httpx.Response:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        return await c.request(method, url, **kw)


@pytest.mark.asyncio
async def test_cors_preflight_allows_the_web_page_with_a_bearer_token():
    app = create_app(use_lifespan=False)
    r = await _get(app, "OPTIONS", "/server/info", headers={
        "Origin": "http://192.168.1.5:8080", "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "authorization,content-type"})
    assert r.status_code == 200
    assert r.headers["access-control-allow-origin"] == "*"
    assert "authorization" in r.headers["access-control-allow-headers"].lower()
    assert "access-control-allow-credentials" not in r.headers   # tokens travel in a header, never a cookie


@pytest.mark.asyncio
async def test_cors_answers_carry_the_header():
    r = await _get(create_app(use_lifespan=False), "GET", "/server/info",
                   headers={"Origin": "http://192.168.1.5:8080", "Accept": "application/json"})
    assert r.status_code == 200 and r.headers["access-control-allow-origin"] == "*"


@pytest.mark.asyncio
async def test_cors_can_be_limited(monkeypatch):
    monkeypatch.setattr(settings, "cors_origins", ["http://good.example"])
    app = create_app(use_lifespan=False)
    bad = await _get(app, "GET", "/server/info", headers={"Origin": "http://evil.example"})
    good = await _get(app, "GET", "/server/info", headers={"Origin": "http://good.example"})
    assert "access-control-allow-origin" not in bad.headers
    assert good.headers["access-control-allow-origin"] == "http://good.example"


@pytest.mark.asyncio
async def test_the_web_build_is_served_at_web_when_it_exists(tmp_path, monkeypatch):
    (tmp_path / "index.html").write_text("<html>Toan Tu Tien</html>", "utf-8")
    (tmp_path / "toantutien.tar.gz").write_bytes(b"\x1f\x8b fake")
    monkeypatch.setattr(settings, "web_build_dir", tmp_path)
    app = create_app(use_lifespan=False)
    page = await _get(app, "GET", "/web/")
    assert page.status_code == 200 and "Toan Tu Tien" in page.text
    pack = await _get(app, "GET", "/web/toantutien.tar.gz")
    assert pack.status_code == 200 and pack.content.startswith(b"\x1f\x8b")
    assert "content-encoding" not in pack.headers     # the browser must not unzip it: pygbag does
    assert (await _get(app, "GET", "/server/info", headers={"Accept": "application/json"})).status_code == 200


@pytest.mark.asyncio
async def test_no_build_no_web_route(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "web_build_dir", tmp_path / "missing")
    r = await _get(create_app(use_lifespan=False), "GET", "/web/")
    assert r.status_code == 404
