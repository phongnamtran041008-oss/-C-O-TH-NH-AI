#!/usr/bin/env python3
"""Look through every rendered character before it goes into the game (M8, kế hoạch 7.1
bước 6).

    python tools/preview_sprites.py                  # a window: play the clips
    python tools/preview_sprites.py --contact out.png  # one picture of every frame

A window is the honest way to judge an animation - a sheet of stills cannot show a walk
that limps. The contact sheet is for the times when there is no window to open (a build
machine, or a conversation like this one), and for putting a picture in a report.

In the window:
    ← →   previous / next character        ↑ ↓   previous / next clip
    1-4   which way it faces               space pause          , .  step one frame
    g     grid and pivot on/off            esc   quit
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pygame  # noqa: E402

from client.engine import charsheet  # noqa: E402

BG = (28, 26, 24)
GRID = (52, 48, 44)
PIVOT = (220, 80, 80)
TEXT = (238, 232, 216)
ZOOM = 6


def contact(out: Path, zoom: int = 3) -> int:
    """One PNG with every frame of every character, labelled. Needs no window."""
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    pygame.init()
    pygame.display.set_mode((1, 1))
    ids = charsheet.available()
    if not ids:
        print("preview_sprites: no characters in client/assets/chars yet", file=sys.stderr)
        return 1
    font = pygame.font.SysFont("consolas,dejavusansmono,monospace", 11)
    rows: list[tuple[str, list[pygame.Surface]]] = []
    for cid in ids:
        cs = charsheet.load(cid)
        if cs is None:
            continue
        for clip_name, clip in sorted(cs.clips.items()):
            for d in charsheet.DIRS:
                ids_ = clip.frames.get(d) or []
                if ids_:
                    rows.append((f"{cid} {clip_name} {d}", [cs.frame(i) for i in ids_]))
    if not rows:
        print("preview_sprites: nothing to show", file=sys.stderr)
        return 1
    fw = max(f.get_width() for _, fs in rows for f in fs) * zoom
    fh = max(f.get_height() for _, fs in rows for f in fs) * zoom
    label_w = 190
    cols = max(len(fs) for _, fs in rows)
    sheet = pygame.Surface((label_w + cols * (fw + 4), len(rows) * (fh + 4)))
    sheet.fill(BG)
    for r, (label, frames) in enumerate(rows):
        y = r * (fh + 4)
        sheet.blit(font.render(label, True, TEXT), (6, y + fh // 2 - 6))
        for c, f in enumerate(frames):
            x = label_w + c * (fw + 4)
            pygame.draw.rect(sheet, GRID, (x, y, fw, fh), 1)
            sheet.blit(pygame.transform.scale(f, (f.get_width() * zoom, f.get_height() * zoom)),
                       (x, y))
    out.parent.mkdir(parents=True, exist_ok=True)
    pygame.image.save(sheet, str(out))
    print(f"wrote {out} ({len(rows)} rows, {sum(len(f) for _, f in rows)} frames)")
    return 0


def window() -> int:
    pygame.init()
    screen = pygame.display.set_mode((560, 420))
    pygame.display.set_caption("Toán Tu Tiên - xem trước sprite")
    font = pygame.font.SysFont("consolas,dejavusansmono,monospace", 14)
    clock = pygame.time.Clock()
    ids = charsheet.available()
    if not ids:
        print("preview_sprites: no characters in client/assets/chars yet", file=sys.stderr)
        return 1
    ci, clip_i, d_i, t, paused, grid = 0, 0, 0, 0.0, False, True
    while True:
        cs = charsheet.load(ids[ci])
        clips = sorted(cs.clips) if cs else []
        clip_name = clips[clip_i % len(clips)] if clips else ""
        direction = charsheet.DIRS[d_i % len(charsheet.DIRS)]
        dt = clock.tick(60) / 1000
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return 0
            if ev.type != pygame.KEYDOWN:
                continue
            k = ev.key
            if k == pygame.K_ESCAPE:
                return 0
            elif k in (pygame.K_LEFT, pygame.K_RIGHT):
                ci = (ci + (1 if k == pygame.K_RIGHT else -1)) % len(ids)
                clip_i, t = 0, 0.0
            elif k in (pygame.K_UP, pygame.K_DOWN) and clips:
                clip_i = (clip_i + (1 if k == pygame.K_DOWN else -1)) % len(clips)
                t = 0.0
            elif pygame.K_1 <= k <= pygame.K_4:
                d_i = k - pygame.K_1
            elif k == pygame.K_SPACE:
                paused = not paused
            elif k == pygame.K_g:
                grid = not grid
            elif k in (pygame.K_COMMA, pygame.K_PERIOD) and cs and clip_name:
                step = 1 / cs.clips[clip_name].fps
                t = max(0.0, t + (step if k == pygame.K_PERIOD else -step))
        if not paused:
            t += dt
        screen.fill(BG)
        if cs and clip_name:
            clip = cs.clips[clip_name]
            img = cs.at(clip_name, t, direction)
            big = pygame.transform.scale(img, (cs.fw * ZOOM, cs.fh * ZOOM))
            ox, oy = 160, 60
            if grid:
                pygame.draw.rect(screen, GRID, (ox, oy, cs.fw * ZOOM, cs.fh * ZOOM), 1)
            screen.blit(big, (ox, oy))
            if grid:
                px, py = ox + cs.pivot[0] * ZOOM, oy + cs.pivot[1] * ZOOM
                pygame.draw.line(screen, PIVOT, (px - 8, py), (px + 8, py))
                pygame.draw.line(screen, PIVOT, (px, py - 8), (px, py + 8))
            n = (int(t * clip.fps) % clip.count(direction)) if clip.loop else \
                min(int(t * clip.fps), clip.count(direction) - 1)
            lines = [f"{cs.id}  ({ci + 1}/{len(ids)})",
                     f"clip: {clip_name}  {clip.fps:g} fps  {'loop' if clip.loop else 'once'}",
                     f"hướng: {direction}   khung {n + 1}/{clip.count(direction)}",
                     f"khung {cs.fw}x{cs.fh}  neo {cs.pivot[0]:g},{cs.pivot[1]:g}",
                     "", "← → nhân vật   ↑ ↓ clip   1-4 hướng",
                     "space dừng   , . từng khung   g lưới   esc thoát"]
            for i, line in enumerate(lines):
                screen.blit(font.render(line, True, TEXT), (12, 12 + i * 18))
        pygame.display.flip()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--contact", default="", help="write a contact sheet instead of opening a window")
    ap.add_argument("--zoom", type=int, default=3)
    args = ap.parse_args(argv)
    return contact(Path(args.contact), args.zoom) if args.contact else window()


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main(sys.argv[1:]))
