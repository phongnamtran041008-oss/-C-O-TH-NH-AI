"""Layout audit: what went wrong on a frame, from what the kit recorded while drawing it.

Usage, from a test or a tool (no window needed: SDL_VIDEODRIVER=dummy):

    ui.audit = []                 # client/ui/kit.py records from now on
    ui.begin([], 0.016)
    scene.draw_ui(ui)
    found = audit.problems(ui.audit, panel=(x, y, w, h))
    ui.audit = None

Records (dicts, base units 480x270, one per drawing call) - see kit.UI:
    {"kind": "text", "rect": (x, y, w, h), "ink": (x, y, w, h) | None, "text": str, "size": float,
     "owner": button id | None, "clip": (x, y, w, h) | None, "lines": int}
    {"kind": "button" | "input", "rect": ..., "id": str, "clip": ...}
    {"kind": "panel", "rect": ...}
    {"kind": "cut" | "dropped", "text": str}      # a layout shortened or left out a text

Problems (`Problem.kind`):
    offscreen      a text's ink is not entirely on the 480x270 screen
    outside_panel  a text's ink leaves the panel rectangle given to `problems`
    clipped        a text's ink is partly (or entirely) outside the clip rectangle in force
    overlap        the inks of two texts overlap (a 1-px shadow of the same text excepted)
    over_button    a text's ink overlaps a button / input box it does not belong to (a text
                   belongs to a button when it is its label, or lies entirely inside it)
    widget_overlap two buttons / input boxes overlap (one hides part of the other)
    widget_outside a button / input box leaves the screen or the given panel
    cut            a layout cut a text short (an ellipsis) or left it out

The ink box is the bounding box of the pixels actually drawn, so the empty leading of a font
never counts as an overlap. Everything here is plain data: the same check serves the question
card, the code editor, the hub or any other scene."""
from __future__ import annotations

from dataclasses import dataclass

SCREEN = (0.0, 0.0, 480.0, 270.0)
TOL = 0.5                 # base px: touching is not overlapping

HARD = ("offscreen", "outside_panel", "clipped", "overlap", "over_button", "widget_overlap", "widget_outside",
        "cut")


@dataclass
class Problem:
    kind: str
    text: str
    rect: tuple | None = None
    other: str = ""

    def describe(self) -> str:
        where = "" if self.rect is None else " @ (%.0f, %.0f, %.0f, %.0f)" % tuple(self.rect)
        with_ = f" <-> {self.other!r}" if self.other else ""
        return f"{self.kind}: {self.text!r}{with_}{where}"


def _inside(a, b, tol: float = TOL) -> bool:
    return (a[0] >= b[0] - tol and a[1] >= b[1] - tol and a[0] + a[2] <= b[0] + b[2] + tol
            and a[1] + a[3] <= b[1] + b[3] + tol)


def _meets(a, b, tol: float = TOL) -> bool:
    return (min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0]) > tol
            and min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1]) > tol)


def texts(records) -> list[dict]:
    """The text records that drew something."""
    return [r for r in records if r.get("kind") == "text" and r.get("ink")]


def widgets(records) -> list[dict]:
    return [r for r in records if r.get("kind") in ("button", "input")]


def problems(records, panel=None, screen=SCREEN, ignore_overlap=()) -> list[Problem]:
    """Every problem of one frame. `panel`: the rectangle every text and widget must stay in
    (None: the screen only). `ignore_overlap`: widget ids whose overlap with each other is
    meant (none by default)."""
    out: list[Problem] = []
    ts = texts(records)
    ws = widgets(records)
    for r in records:
        if r.get("kind") in ("cut", "dropped"):
            out.append(Problem("cut", r.get("text", "")))
    for t in ts:
        ink, label = t["ink"], t["text"]
        if not _inside(ink, screen):
            out.append(Problem("offscreen", label, ink))
        elif panel is not None and not _inside(ink, panel):
            out.append(Problem("outside_panel", label, ink))
        clip = t.get("clip")
        if clip is not None and not _inside(ink, clip):
            out.append(Problem("clipped", label, ink))
        for w in ws:
            if t.get("owner") == w["id"] or not _meets(ink, w["rect"]):
                continue
            if _inside(ink, w["rect"]):
                continue                     # a label drawn over its own (blank) button
            out.append(Problem("over_button", label, ink, w["id"]))
    for i, a in enumerate(ts):
        for b in ts[i + 1:]:
            if not _meets(a["ink"], b["ink"]):
                continue
            if a["text"] == b["text"] and abs(a["rect"][0] - b["rect"][0]) <= 1.5 and \
                    abs(a["rect"][1] - b["rect"][1]) <= 1.5:
                continue                     # a shadow: the same text drawn twice, a pixel apart
            out.append(Problem("overlap", a["text"], a["ink"], b["text"]))
    for i, a in enumerate(ws):
        box = a["rect"]
        if not _inside(box, screen) or (panel is not None and not _inside(box, panel)):
            out.append(Problem("widget_outside", a["id"], box))
        for b in ws[i + 1:]:
            if a["id"] in ignore_overlap and b["id"] in ignore_overlap:
                continue
            if _meets(box, b["rect"]):
                out.append(Problem("widget_overlap", a["id"], box, b["id"]))
    return out


def summary(found: list[Problem]) -> dict[str, int]:
    """How many problems of each kind."""
    out: dict[str, int] = {}
    for p in found:
        out[p.kind] = out.get(p.kind, 0) + 1
    return out
