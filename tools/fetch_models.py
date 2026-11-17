#!/usr/bin/env python3
"""Fetch the low-poly models the game's icons are rendered from (M8, kế hoạch 7.1 bước 7).

    python tools/fetch_models.py --list          # what would be fetched, nothing downloaded
    python tools/fetch_models.py                 # fetch everything missing
    python tools/fetch_models.py --kind vu_khi   # one group
    python tools/fetch_models.py --cc0-only      # refuse anything that needs crediting

Models come from **Poly Pizza** (https://poly.pizza), which hosts free low-poly models. The
style is the reason: a realistic sword is one pixel wide once a sprite is 32 px tall, while
a stylised one keeps a readable blade, guard and grip - that is what the author's reference
sheets are drawn like.

**Licences are not optional.** Every model's page says CC0 or CC-BY; both are recorded in
`art/models/manifest.json`, and CC-BY ones *must* keep their credit (creator and link) in
CREDITS.md. `--cc0-only` skips everything that would need a credit line. Nothing here is
scraped around a paywall: these are the files the site's own 3D viewer loads.

What is downloaded is a .glb (glTF binary) - geometry and materials, no code - and it goes
to its own folder under art/models/, which the renderer reads and the game never does.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "art" / "models"
MANIFEST = OUT / "manifest.json"
UA = {"User-Agent": "Mozilla/5.0 (compatible; khu-vuon-tu-tien asset fetcher)"}
SITE = "https://poly.pizza"

# what the game needs, read off the author's reference sheets
# kind -> [(our id, search words, how many of the results to take)]
WANTED: dict[str, list[tuple[str, str, int]]] = {
    "vu_khi": [            # tám loại vũ khí trong ảnh mẫu
        ("kiem", "sword", 3), ("dao", "katana", 2), ("thuong", "spear", 2),
        ("bua", "mace", 2), ("truong", "magic staff", 2), ("cung", "bow", 2),
        # quạt and hồ lô are left out on purpose: the library has no folding fan and no
        # calabash gourd - "fan" returns ceiling fans and "gourd" returns onions. Better an
        # honest gap than a vegetable in the weapon rack.
    ],
    "trang_bi": [
        # ("ao_giap", ...) also left out: every armour query comes back with crates and shields
        ("mu", "wizard hat", 2), ("gang", "glove", 1),
        ("giay", "boots", 1), ("khien", "shield", 2), ("nhan", "ring", 1),
        ("day_chuyen", "amulet necklace", 1),
    ],
    "dan_duoc": [
        ("dan", "potion bottle", 3), ("linh_thao", "herb plant", 2),
        ("lo_dan", "cauldron", 1),
    ],
    "cong_phap": [
        ("sach", "book", 2), ("cuon_thu", "scroll", 2),
    ],
}


def get(url: str, retries: int = 3) -> str:
    for n in range(retries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=45) as r:
                return r.read().decode("utf-8", "replace")
        except (urllib.error.URLError, TimeoutError) as e:
            if n == retries - 1:
                raise
            time.sleep(1.5 * (n + 1))
            _ = e
    return ""


def search(words: str, limit: int) -> list[str]:
    """The model ids the site returns for these words, in its own order."""
    html = get(f"{SITE}/search/{urllib.request.quote(words)}")
    ids = list(dict.fromkeys(re.findall(r"/m/([A-Za-z0-9_-]+)", html)))
    return ids[:limit]


def model_info(model_id: str) -> dict | None:
    """Title, creator, licence and the .glb the site's own viewer loads."""
    html = get(f"{SITE}/m/{model_id}")
    glb = re.search(r"https://static\.poly\.pizza/[0-9a-fA-F-]+\.glb", html)
    if not glb:
        return None
    title = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    creator = re.findall(r"/u/([A-Za-z0-9_.-]+)", html)
    licence_url = re.search(r"creativecommons\.org/[^\"']+", html)
    licence = "CC0" if "publicdomain/zero" in (licence_url.group(0) if licence_url else "") else None
    if licence is None:
        licence = "CC-BY" if re.search(r"CC-?\s?BY", html) else "unknown"
    return {
        "id": model_id,
        "title": re.sub(r"<[^>]+>", "", title.group(1)).strip() if title else model_id,
        "creator": creator[0] if creator else "unknown",
        "licence": licence,
        "licence_url": ("https://" + licence_url.group(0)) if licence_url else "",
        "page": f"{SITE}/m/{model_id}",
        "glb": glb.group(0),
    }


def fetch_one(kind: str, slug: str, info: dict, n: int) -> dict:
    folder = OUT / kind
    folder.mkdir(parents=True, exist_ok=True)
    name = f"{slug}_{n}.glb" if n else f"{slug}.glb"
    path = folder / name
    if not path.exists():
        with urllib.request.urlopen(urllib.request.Request(info["glb"], headers=UA), timeout=90) as r:
            data = r.read()
        if data[:4] != b"glTF":
            raise ValueError(f"{info['page']} did not return a glb")
        path.write_bytes(data)
    return {**info, "kind": kind, "slug": slug, "file": str(path.relative_to(ROOT)).replace("\\", "/"),
            "bytes": path.stat().st_size}


def credits_block(rows: list[dict]) -> str:
    lines = ["", "## Model 3D cho icon (M8)", "",
             "Model low-poly tải từ Poly Pizza (https://poly.pizza) bằng "
             "`tools/fetch_models.py`; icon trong game là ảnh render từ chúng.",
             "CC0 thì không bắt buộc ghi công, nhưng vẫn ghi ở đây cho đủ dấu vết; "
             "CC-BY thì **bắt buộc** giữ dòng ghi công.", ""]
    for r in sorted(rows, key=lambda r: (r["kind"], r["slug"])):
        lines.append(f"- {r['kind']}/{r['slug']}: \"{r['title']}\" — {r['creator']} "
                     f"({r['licence']}) — {r['page']}")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--kind", default="", help=f"one of {', '.join(WANTED)}")
    ap.add_argument("--cc0-only", action="store_true", help="skip anything that needs crediting")
    ap.add_argument("--list", action="store_true", help="say what would be fetched, download nothing")
    args = ap.parse_args(argv)

    kinds = [args.kind] if args.kind else list(WANTED)
    rows: list[dict] = []
    skipped: list[str] = []
    for kind in kinds:
        for slug, words, count in WANTED[kind]:
            ids = search(words, count)
            if not ids:
                print(f"  {kind}/{slug}: nothing found for {words!r}", file=sys.stderr)
                continue
            for n, model_id in enumerate(ids):
                info = model_info(model_id)
                if info is None:
                    continue
                if args.cc0_only and info["licence"] != "CC0":
                    skipped.append(f"{kind}/{slug}: {info['title']} ({info['licence']})")
                    continue
                if args.list:
                    print(f"  {kind}/{slug}[{n}] {info['title']} by {info['creator']} "
                          f"({info['licence']}) {info['page']}")
                    rows.append({**info, "kind": kind, "slug": slug})
                    continue
                row = fetch_one(kind, slug, info, n)
                rows.append(row)
                print(f"  {kind}/{slug}[{n}] {row['title']} by {row['creator']} "
                      f"({row['licence']}) {row['bytes'] // 1024} KB")
    if args.list:
        print(f"\n{len(rows)} model(s) would be fetched")
        return 0
    OUT.mkdir(parents=True, exist_ok=True)
    # Models built by hand in Blender (tools/blender/build_items.py) share this manifest and
    # must survive a re-fetch: nothing here downloaded them, so nothing here may drop them.
    keep = []
    if MANIFEST.exists():
        try:
            old_rows = json.loads(MANIFEST.read_text("utf-8"))["models"]
        except (ValueError, KeyError):
            old_rows = []
        fetched = {(r["kind"], r["slug"], r.get("id")) for r in rows}
        for m in old_rows:
            # keep the hand-built items, and - when only one group was asked for - every
            # other group, so `--kind vu_khi` cannot quietly wipe the rest of the manifest
            if m.get("handmade") or (args.kind and m.get("kind") != args.kind):
                if (m.get("kind"), m.get("slug"), m.get("id")) not in fetched:
                    keep.append(m)
    rows = rows + keep
    MANIFEST.write_text(json.dumps({"source": SITE, "models": rows}, ensure_ascii=False, indent=1) + "\n",
                        "utf-8", newline="\n")
    credits = ROOT / "CREDITS.md"
    text = credits.read_text("utf-8") if credits.exists() else "# CREDITS\n"
    marker = "## Model 3D cho icon (M8)"
    if marker in text:
        text = text[:text.index(marker)].rstrip("\n") + "\n"
    credits.write_text(text + credits_block(rows), "utf-8", newline="\n")
    by = sum(1 for r in rows if r["licence"] != "CC0")
    print(f"\n{len(rows)} model(s) in {OUT.relative_to(ROOT)}; {by} need crediting; "
          f"manifest + CREDITS.md updated")
    for s in skipped:
        print(f"  skipped (not CC0): {s}")
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main(sys.argv[1:]))
