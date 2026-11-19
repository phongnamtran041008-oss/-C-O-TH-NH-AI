"""Where things live. No bpy, no numpy: importable from the venv and from Blender."""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]          # the repository
KIT_DIR = Path(__file__).resolve().parent
BLENDER_EXE = os.environ.get(
    "KIT_BLENDER", "C:/Program Files/Blender Foundation/Blender 5.3/blender.exe")
VENV_PY = os.environ.get("KIT_VENV_PY", "E:/TU TIÊN AI/.venv/Scripts/python.exe")
ASSETS_V2 = ROOT / "client" / "assets" / "v2"
RENDER_DIR = ROOT / "art" / "render"
PREVIEW_DIR = ROOT / "art" / "preview"


def batch_name() -> str:
    return os.environ.get("KIT_BATCH", "default")


def render_dir(batch: str | None = None) -> Path:
    """art/render/<batch>/ - intermediate files of one batch (git-ignored)."""
    d = RENDER_DIR / (batch or batch_name())
    d.mkdir(parents=True, exist_ok=True)
    return d


def tmp_dir(batch: str | None = None) -> Path:
    """A folder only this process writes to, so batches (and several Blenders of one batch)
    can render at the same time."""
    d = render_dir(batch) / f"_tmp_{os.getpid()}"
    d.mkdir(parents=True, exist_ok=True)
    return d
