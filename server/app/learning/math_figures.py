"""Figures of Tàng Thư Các: the diagrams a lesson card shows, laid out here on the server.

A document writes a figure as a small block of plain lines (one setting or one thing to
draw per line), and the server turns it into drawable primitives in base units, so the
client is one small generic drawer and a new kind of figure needs no client change:

    :::figure plane
    caption: u + v: đặt gốc của v vào ngọn của u
    x: -1 4
    y: -1 4
    vector 0 0 2 1 do "u"
    vector 2 1 3 3 xanh "v" dash
    :::

A line is either a setting (`key: value`) or a command followed by its arguments. An
argument is a number (2, -1.5, 1/2, pi/2), a colour (do xanh luc vang tim xam muc), a
word the command knows (dash, open, ...), `key=value`, or a "quoted label". Every problem
is raised as FigureError with one readable line.

The output, for the client (client/ui/figures.py):

    {"type": "figure", "kind", "w", "h", "caption", "prims": [...]}

`w` x `h` is the drawing in base units (the caption goes under it, drawn by the client).
Primitives, coordinates from the top-left corner of the figure:

    line      x1 y1 x2 y2 c [wd] [dash]
    arrow     x1 y1 x2 y2 c [wd] [dash]            head at (x2, y2)
    polyline  pts c [wd] [dash]
    poly      pts fill [a] [edge]                   a filled shape; a = how strong the tint is
    rect      x y w h [fill] [a] [edge] [r]
    circle    x y r [fill] [a] [edge] [wd]
    spans     y dy rows c [a]                       rows of [x1, x2, x3, x4 ...] intervals
    text      x y s size c anchor                   anchor as in ui.text (center, midleft ...)

Colours are Vietnamese names; the client maps them to the game palette. Label widths are
estimated (the pixel font VT323 is monospace); the client's screenshot check measures them
for real.

Pure Python, no pygame.
"""
from __future__ import annotations

import ast
import math
import re

from .math_path import text_problem

MAX_W = 400.0            # the widest figure the reader shows without shrinking it
MAX_H = 130.0            # the tallest (the caption is extra)
CHAR_W = 0.6             # VT323: base units per character per unit of size (measured 0.58)
LINE_K = 1.45            # VT323: line height per unit of size
LABEL = 7                # label size
SMALL = 6                # tick labels, values
MAX_LINES = 40           # lines in one figure block
COLOURS = ("do", "xanh", "luc", "vang", "tim", "xam", "muc")
KINDS = ("plane", "bars", "graph", "sets", "map", "grid", "numberline", "flow")
POSITIONS = ("n", "s", "e", "w", "ne", "nw", "se", "sw", "c")


class FigureError(ValueError):
    """One problem in a figure, said in one line."""


# ------------------------------------------------------------------ the safe evaluator
FUNCS = {"sin": math.sin, "cos": math.cos, "tan": math.tan, "exp": math.exp, "ln": math.log,
         "log": math.log10, "sqrt": math.sqrt, "abs": abs}
CONSTS = {"pi": math.pi, "e": math.e}
OPS = {ast.Add: lambda a, b: a + b, ast.Sub: lambda a, b: a - b, ast.Mult: lambda a, b: a * b,
       ast.Div: lambda a, b: a / b, ast.Pow: lambda a, b: a ** b}
MAX_EXPR = 80


class Expr:
    """A formula in one variable, checked once and then evaluated without eval():
    numbers, the variable, + - * / ^ (or **), unary minus, brackets, pi, e and the
    functions sin cos tan exp ln log sqrt abs. Anything else is refused."""

    def __init__(self, text: str, var: str = "x"):
        self.text, self.var = text, var
        if not text.strip():
            raise FigureError("an empty expression")
        if len(text) > MAX_EXPR:
            raise FigureError(f"the expression {text!r} is longer than {MAX_EXPR} characters")
        try:
            tree = ast.parse(text.replace("^", "**"), mode="eval")
        except SyntaxError:
            raise FigureError(f"{text!r} is not an expression (write 2*x, not 2x)") from None
        self._check(tree.body)
        self.tree = tree.body

    def _check(self, node: ast.AST) -> None:
        if isinstance(node, ast.BinOp) and type(node.op) in OPS:
            self._check(node.left)
            self._check(node.right)
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
            self._check(node.operand)
        elif isinstance(node, ast.Constant):
            if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
                raise FigureError(f"{self.text!r}: only numbers are allowed, not {node.value!r}")
        elif isinstance(node, ast.Name):
            if node.id != self.var and node.id not in CONSTS:
                raise FigureError(f"{self.text!r}: unknown name {node.id!r} (the variable is {self.var})")
        elif isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name) or node.func.id not in FUNCS:
                raise FigureError(f"{self.text!r}: only {', '.join(FUNCS)} can be called")
            if len(node.args) != 1 or node.keywords:
                raise FigureError(f"{self.text!r}: {node.func.id} takes exactly one argument")
            self._check(node.args[0])
        else:
            raise FigureError(f"{self.text!r}: {type(node).__name__} is not allowed in an expression")

    def __call__(self, value: float = 0.0) -> float | None:
        """The value, or None where it is not a real number (outside the domain, 1/0)."""
        try:
            out = self._eval(self.tree, float(value))
        except (ArithmeticError, ValueError):
            return None
        if isinstance(out, complex) or not math.isfinite(out):
            return None
        return float(out)

    def _eval(self, node, v: float):
        if isinstance(node, ast.BinOp):
            a, b = self._eval(node.left, v), self._eval(node.right, v)
            if isinstance(node.op, ast.Pow) and (abs(b) > 64 or abs(a) > 1e9):
                raise OverflowError
            return OPS[type(node.op)](a, b)
        if isinstance(node, ast.UnaryOp):
            x = self._eval(node.operand, v)
            return -x if isinstance(node.op, ast.USub) else x
        if isinstance(node, ast.Constant):
            return float(node.value)
        if isinstance(node, ast.Name):
            return v if node.id == self.var else CONSTS[node.id]
        x = self._eval(node.args[0], v)
        if isinstance(x, complex):
            raise ValueError
        return FUNCS[node.func.id](x)


def number(token: str) -> float:
    """A number written in a figure: 2, -1.5, 1/2, pi/2, sqrt(2)."""
    if len(token) > 24:
        raise FigureError(f"{token!r} is not a number")
    try:
        value = Expr(token, var="")()          # no variable at all: only numbers, pi and e
    except FigureError:
        raise FigureError(f"{token!r} is not a number") from None
    if value is None:
        raise FigureError(f"{token!r} is not a number")
    return value


# ------------------------------------------------------------------ reading a figure block
class Label(str):
    """A "quoted" argument."""


TOKEN = re.compile(r'"([^"]*)"|(\S+)')


def tokens(line: str) -> list[str]:
    out: list[str] = []
    for m in TOKEN.finditer(line):
        if m.group(1) is not None:
            out.append(Label(m.group(1)))
        elif m.group(2).startswith('"'):
            raise FigureError(f"a quote is never closed in {line!r}")
        else:
            out.append(m.group(2))
    return out


class Args:
    """The arguments of one command, sorted by what they are."""

    def __init__(self, cmd: str, toks: list[str], words: tuple[str, ...] = ()):
        self.cmd = cmd
        self.nums: list[float] = []
        self.labels: list[str] = []
        self.colour: str | None = None
        self.words: list[str] = []
        self.opts: dict[str, str] = {}
        for t in toks:
            if isinstance(t, Label):
                self.labels.append(str(t))
            elif t in COLOURS:
                if self.colour:
                    raise FigureError(f"{cmd}: two colours ({self.colour}, {t})")
                self.colour = t
            elif t in words:
                self.words.append(t)
            elif "=" in t and not t.startswith("="):
                k, _, v = t.partition("=")
                self.opts[k] = v.strip('"')
            else:
                try:
                    self.nums.append(number(t))
                except FigureError:
                    raise FigureError(f"{cmd}: {t!r} is not a number, a colour or a word it knows"
                                      + (f" ({', '.join(words)})" if words else "")
                                      + "; put a label in double quotes") from None

    def need(self, *counts: int) -> list[float]:
        if len(self.nums) not in counts:
            want = " or ".join(str(c) for c in counts)
            raise FigureError(f"{self.cmd}: needs {want} numbers, got {len(self.nums)}")
        return self.nums

    def label(self, required: bool = False) -> str:
        if len(self.labels) > 1:
            raise FigureError(f"{self.cmd}: only one \"label\"")
        if required and not self.labels:
            raise FigureError(f"{self.cmd}: needs a \"label\"")
        return self.labels[0] if self.labels else ""

    def pos(self, default: str) -> str:
        p = self.opts.get("pos", default)
        if p not in POSITIONS:
            raise FigureError(f"{self.cmd}: pos={p} must be one of {' '.join(POSITIONS)}")
        return p


def tw(text: str, size: float = LABEL) -> float:
    return len(text) * size * CHAR_W


def th(size: float = LABEL) -> float:
    return size * LINE_K


def r1(v: float) -> float:
    return round(v, 1)


def txt(x, y, s, size=LABEL, c="muc", anchor="center") -> dict:
    return {"t": "text", "x": r1(x), "y": r1(y), "s": s, "size": size, "c": c, "anchor": anchor}


def place(x: float, y: float, text: str, pos: str, gap: float = 3.0, size: float = LABEL) -> dict:
    """A label next to the point (x, y), on the side `pos` (a compass direction)."""
    dx = {"e": 1, "w": -1, "ne": 1, "nw": -1, "se": 1, "sw": -1}.get(pos, 0)
    dy = {"n": -1, "s": 1, "ne": -1, "nw": -1, "se": 1, "sw": 1}.get(pos, 0)
    anchor = {(0, 0): "center", (1, 0): "midleft", (-1, 0): "midright", (0, -1): "midbottom",
              (0, 1): "midtop", (1, -1): "bottomleft", (-1, -1): "bottomright",
              (1, 1): "topleft", (-1, 1): "topright"}[(dx, dy)]
    return txt(x + dx * gap, y + dy * gap, text, size, anchor=anchor)


def text_box(p: dict) -> tuple[float, float, float, float]:
    """(x0, y0, x1, y1) of a text primitive, estimated."""
    w, h = tw(p["s"], p["size"]), th(p["size"])
    a = p["anchor"]
    x0 = p["x"] - (w / 2 if a in ("center", "midtop", "midbottom") else w if a.endswith("right") else 0)
    y0 = p["y"] - (h / 2 if a in ("center", "midleft", "midright") else h if a.startswith("bottom") else 0)
    return x0, y0, x0 + w, y0 + h


def _boxes_meet(a, b, gap: float = 0.0) -> bool:
    return a[0] < b[2] + gap and b[0] < a[2] + gap and a[1] < b[3] + gap and b[1] < a[3] + gap


def spread_labels(prims: list[dict], w: float, h: float) -> None:
    """Moves a label that lands on an earlier one up or down (then left or right) to the
    nearest free place inside the figure. Labels come in drawing order: tick labels first,
    then the author's, so the author's labels move, never the axes."""
    placed: list[tuple] = []
    for p in prims:
        if p["t"] != "text":
            continue
        box = text_box(p)
        if any(_boxes_meet(box, q, 0.5) for q in placed):
            hh, ww = box[3] - box[1], box[2] - box[0]
            tries = [(0, d * hh * s) for d in (0.6, 1.0, 1.4) for s in (-1, 1)] + \
                    [(d * s, 0) for d in (ww * 0.6, ww) for s in (1, -1)]
            for dx, dy in tries:
                moved = (box[0] + dx, box[1] + dy, box[2] + dx, box[3] + dy)
                if moved[0] >= 0 and moved[1] >= 0 and moved[2] <= w and moved[3] <= h and \
                        not any(_boxes_meet(moved, q, 0.5) for q in placed):
                    p["x"], p["y"] = r1(p["x"] + dx), r1(p["y"] + dy)
                    box = moved
                    break
        placed.append(box)


def keep_inside(prims: list[dict], w: float, h: float) -> None:
    """Moves a text label that would stick out of the figure back inside it."""
    for p in prims:
        if p["t"] != "text":
            continue
        x0, y0, x1, y1 = text_box(p)
        dx = -x0 if x0 < 0 else (w - x1 if x1 > w else 0)
        dy = -y0 if y0 < 0 else (h - y1 if y1 > h else 0)
        p["x"], p["y"] = r1(p["x"] + dx), r1(p["y"] + dy)


def fmt(v: float) -> str:
    if abs(v - round(v)) < 1e-9:
        return str(int(round(v)))
    return f"{v:.2f}".rstrip("0").rstrip(".")


# ------------------------------------------------------------------ the figure block
def _uncomment(line: str) -> str:
    """The line without a # comment (a # inside a "quoted label" is kept)."""
    quoted = False
    for i, ch in enumerate(line):
        if ch == '"':
            quoted = not quoted
        elif ch == "#" and not quoted and (i == 0 or line[i - 1].isspace()):
            return line[:i].strip()
    return line.strip()


def parse_figure(kind: str, lines: list[str]) -> dict:
    """The figure of a `:::figure <kind>` block, ready to draw. Raises FigureError."""
    if kind not in KINDS:
        raise FigureError(f"unknown figure kind {kind!r} (kinds: {', '.join(KINDS)})")
    lines = [_uncomment(ln) for ln in lines]
    lines = [ln for ln in lines if ln]
    if len(lines) > MAX_LINES:
        raise FigureError(f"{len(lines)} lines, at most {MAX_LINES} in one figure")
    settings: dict[str, str] = {}
    commands: list[tuple[str, list[str], str]] = []
    for line in lines:
        head = line.split(None, 1)[0]
        if head.endswith(":"):
            key = head[:-1]
            if key in settings:
                raise FigureError(f"{key}: is set twice")
            settings[key] = line[len(head):].strip()
        else:
            toks = tokens(line)
            commands.append((toks[0], toks[1:], line))
    caption = settings.pop("caption", "").strip()
    if not caption:
        raise FigureError("needs a caption: line (one sentence under the figure)")
    layout = LAYOUTS[kind]
    allowed = layout.SETTINGS + ("size",)
    for key in settings:
        if key not in allowed:
            raise FigureError(f"unknown setting {key}: (a {kind} knows {', '.join(allowed)})")
    size = None
    if "size" in settings:
        parts = settings["size"].split()
        if len(parts) not in (1, 2):
            raise FigureError("size: needs a width, or a width and a height")
        size = [number(p) for p in parts]
        if not 20 <= size[0] <= MAX_W or (len(size) > 1 and not 20 <= size[1] <= MAX_H):
            raise FigureError(f"size: {settings['size']} is outside 20..{MAX_W:g} x 20..{MAX_H:g}")
    for cmd, toks, line in commands:
        if layout is Map and "->" in toks:
            continue
        if cmd not in layout.COMMANDS:
            raise FigureError(f"unknown command {cmd!r} in {line!r} (a {kind} knows "
                              f"{', '.join(layout.COMMANDS)})")
    w, h, prims = layout(settings, commands, size).build()
    for p in prims:
        if p["t"] == "text":
            problem = text_problem(p["s"])
            if problem:
                raise FigureError(f"the label {p['s']!r} {problem}")
    problem = text_problem(caption)
    if problem:
        raise FigureError(f"the caption {problem}")
    w, h = r1(w), r1(h)
    if w > MAX_W + 0.05 or h > MAX_H + 0.05:
        raise FigureError(f"is {w:g} x {h:g}, at most {MAX_W:g} x {MAX_H:g} fits the page "
                          "(fewer items, shorter labels or a smaller size:)")
    keep_inside(prims, w, h)
    spread_labels(prims, w, h)
    return {"type": "figure", "kind": kind, "w": w, "h": h, "caption": caption, "prims": prims}


def labels_of(fig: dict) -> list[str]:
    """Every piece of text a figure shows (for the text checks)."""
    return [fig["caption"]] + [p["s"] for p in fig["prims"] if p["t"] == "text"]


class Layout:
    SETTINGS: tuple[str, ...] = ()
    COMMANDS: tuple[str, ...] = ()
    WORDS: dict[str, tuple[str, ...]] = {}
    LIMIT = 24

    def __init__(self, settings: dict, commands: list, size):
        self.settings, self.size = settings, size
        if len(commands) > self.LIMIT:
            raise FigureError(f"{len(commands)} items, at most {self.LIMIT} in one figure of this kind")
        self.commands = commands

    def args(self, cmd: str, toks: list[str]) -> Args:
        return Args(cmd, toks, self.WORDS.get(cmd, ()))

    def setting_nums(self, key: str, counts: tuple[int, ...], default: list[float]) -> list[float]:
        if key not in self.settings:
            return default
        parts = self.settings[key].split()
        if len(parts) not in counts:
            raise FigureError(f"{key}: needs {' or '.join(map(str, counts))} numbers")
        return [number(p) for p in parts]

    def flag(self, key: str, default: bool) -> bool:
        v = self.settings.get(key)
        if v is None:
            return default
        if v not in ("on", "off", "yes", "no"):
            raise FigureError(f"{key}: must be on or off")
        return v in ("on", "yes")

    def build(self) -> tuple[float, float, list[dict]]:
        raise NotImplementedError


# ------------------------------------------------------------------ plane
class Plane(Layout):
    SETTINGS = ("x", "y", "axes", "grid", "aspect", "names")
    COMMANDS = ("point", "vector", "segment", "line", "curve", "param", "area", "tangent", "poly",
                "text", "drop")
    WORDS = {c: ("dash", "open") for c in COMMANDS}
    LIMIT = 20
    SAMPLES = 240

    def build(self):
        x0, x1, *xs = self.setting_nums("x", (2, 3), [-1, 4])
        y0, y1, *ys = self.setting_nums("y", (2, 3), [-1, 3])
        if x1 - x0 <= 0 or y1 - y0 <= 0:
            raise FigureError("x: and y: need a smaller number first")
        if x1 - x0 > 1000 or y1 - y0 > 1000:
            raise FigureError("x: or y: covers too wide a range")
        self.xr, self.yr = (x0, x1), (y0, y1)
        axes = self.flag("axes", True)
        self.xstep = xs[0] if xs else self.auto_step(x1 - x0)
        self.ystep = ys[0] if ys else self.auto_step(y1 - y0)
        if self.xstep <= 0 or self.ystep <= 0 or (x1 - x0) / self.xstep > 24 or (y1 - y0) / self.ystep > 24:
            raise FigureError("a tick step must be positive, at most 24 ticks per axis")
        ylab = max((len(fmt(v)) for v in self.ticks(y0, y1, self.ystep)), default=1)
        ml = (tw("0" * ylab, SMALL) + 6) if axes else 4
        mb, mt, mr = (10 if axes else 4), 6, (8 if axes else 4)
        maxw, maxh = (self.size or [220, 120]) + [120] * (2 - len(self.size or [220, 120]))
        # Arrows and shapes need the same unit on both axes, or their angles and lengths lie;
        # a graph of a function reads better filling its box.
        geometric = any(cmd in ("vector", "poly") for cmd, _, _ in self.commands)
        aspect = self.settings.get("aspect", "equal" if geometric else "free")
        if aspect not in ("equal", "free"):
            raise FigureError("aspect: must be equal or free")
        free = aspect == "free"
        ux = (maxw - ml - mr) / (x1 - x0)
        uy = (maxh - mt - mb) / (y1 - y0)
        if not free:
            ux = uy = min(ux, uy)
        if ux * (x1 - x0) < 20 or uy * (y1 - y0) < 20:
            raise FigureError("the plot would be too small: make size: bigger or the ranges more even")
        self.ux, self.uy, self.ml, self.mt = ux, uy, ml, mt
        self.w = ml + ux * (x1 - x0) + mr
        self.h = mt + uy * (y1 - y0) + mb
        prims: list[dict] = []
        back: list[dict] = []        # shading goes under the axes
        if self.flag("grid", False):
            for v in self.ticks(x0, x1, self.xstep):
                back.append(self.seg(v, y0, v, y1, "xam", 0.5) | {"a": 60})
            for v in self.ticks(y0, y1, self.ystep):
                back.append(self.seg(x0, v, x1, v, "xam", 0.5) | {"a": 60})
        if axes:
            prims += self.axes()
        front: list[dict] = []
        for cmd, toks, line in self.commands:
            try:
                getattr(self, "cmd_" + cmd)(cmd, toks, back, front)
            except FigureError as e:
                raise FigureError(f"{line!r}: {e}") from None
        return self.w, self.h, back + prims + front

    @staticmethod
    def auto_step(span: float) -> float:
        for step in (0.25, 0.5, 1, 2, 5, 10, 20, 50, 100):
            if span / step <= 8:
                return step
        return 200

    @staticmethod
    def ticks(a: float, b: float, step: float) -> list[float]:
        first = math.ceil(a / step - 1e-9)
        out = []
        n = first
        while n * step <= b + 1e-9:
            out.append(round(n * step, 9))
            n += 1
        return out

    def px(self, x: float) -> float:
        return self.ml + (x - self.xr[0]) * self.ux

    def py(self, y: float) -> float:
        return self.mt + (self.yr[1] - y) * self.uy

    def seg(self, xa, ya, xb, yb, c, wd=1.0, t="line") -> dict:
        return {"t": t, "x1": r1(self.px(xa)), "y1": r1(self.py(ya)), "x2": r1(self.px(xb)),
                "y2": r1(self.py(yb)), "c": c, "wd": wd}

    def inside(self, x, y, slack=1e-9) -> bool:
        return (self.xr[0] - slack <= x <= self.xr[1] + slack) and (self.yr[0] - slack <= y <= self.yr[1] + slack)

    def axes(self) -> list[dict]:
        (x0, x1), (y0, y1) = self.xr, self.yr
        ax = 0.0 if y0 <= 0 <= y1 else y0          # the x axis sits at y = 0 when it is shown
        ay = 0.0 if x0 <= 0 <= x1 else x0
        out = [{"t": "arrow", "x1": r1(self.px(x0)), "y1": r1(self.py(ax)), "x2": r1(self.px(x1) + 5),
                "y2": r1(self.py(ax)), "c": "muc", "wd": 0.5, "head": 3},
               {"t": "arrow", "x1": r1(self.px(ay)), "y1": r1(self.py(y0)), "x2": r1(self.px(ay)),
                "y2": r1(self.py(y1) - 5), "c": "muc", "wd": 0.5, "head": 3}]
        names = self.settings.get("names", "x y").split()
        if len(names) != 2:
            raise FigureError("names: needs two axis names, like names: t s")
        taken: list[tuple] = []

        def label(p: dict) -> None:
            """A tick label, left out when it would touch one already placed."""
            box = text_box(p)
            if not any(_boxes_meet(box, t, 1.0) for t in taken):
                taken.append(box)
                out.append(p)
        if x0 <= 0 <= x1 and y0 <= 0 <= y1:
            label(txt(self.px(0) - 2.5, self.py(0) + 2.5, "O", SMALL, "xam", "topright"))
        label(txt(self.px(x1) + 6, self.py(ax) - 2, names[0], SMALL, "xam", "bottomright"))
        label(txt(self.px(ay) + 3, self.py(y1) - 4, names[1], SMALL, "xam", "topleft"))
        for v in self.ticks(x0, x1, self.xstep):
            if abs(v - ay) < 1e-9:
                continue
            out.append({"t": "line", "x1": r1(self.px(v)), "y1": r1(self.py(ax) - 1.5), "x2": r1(self.px(v)),
                        "y2": r1(self.py(ax) + 1.5), "c": "muc", "wd": 0.5})
            label(txt(self.px(v), self.py(ax) + 2.5, fmt(v), SMALL, "xam", "midtop"))
        for v in self.ticks(y0, y1, self.ystep):
            if abs(v - ax) < 1e-9:
                continue
            out.append({"t": "line", "x1": r1(self.px(ay) - 1.5), "y1": r1(self.py(v)), "x2": r1(self.px(ay) + 1.5),
                        "y2": r1(self.py(v)), "c": "muc", "wd": 0.5})
            label(txt(self.px(ay) - 3, self.py(v), fmt(v), SMALL, "xam", "midright"))
        return out

    def clip(self, xa, ya, xb, yb):
        """The part of a segment inside the plot (Liang-Barsky), or None."""
        (x0, x1), (y0, y1) = self.xr, self.yr
        t0, t1, dx, dy = 0.0, 1.0, xb - xa, yb - ya
        for p, q in ((-dx, xa - x0), (dx, x1 - xa), (-dy, ya - y0), (dy, y1 - ya)):
            if p == 0:
                if q < 0:
                    return None
            else:
                t = q / p
                if p < 0:
                    t0 = max(t0, t)
                else:
                    t1 = min(t1, t)
        if t0 > t1:
            return None
        return xa + t0 * dx, ya + t0 * dy, xa + t1 * dx, ya + t1 * dy

    def colour(self, a: Args, default: str) -> str:
        return a.colour or default

    def check_in(self, *pts) -> None:
        for x, y in pts:
            if not self.inside(x, y, 1e-6):
                raise FigureError(f"({fmt(x)}, {fmt(y)}) is outside x: and y:")

    # -- commands
    def cmd_point(self, cmd, toks, back, front):
        a = self.args(cmd, toks)
        x, y = a.need(2)
        self.check_in((x, y))
        c = self.colour(a, "muc")
        if "open" in a.words:
            front.append({"t": "circle", "x": r1(self.px(x)), "y": r1(self.py(y)), "r": 2.2, "fill": "giay",
                          "a": 255, "edge": c, "wd": 0.7})
        else:
            front.append({"t": "circle", "x": r1(self.px(x)), "y": r1(self.py(y)), "r": 2.2, "fill": c, "a": 255})
        if a.label():
            front.append(place(self.px(x), self.py(y), a.label(), a.pos("ne")))

    def cmd_drop(self, cmd, toks, back, front):
        a = self.args(cmd, toks)
        x, y = a.need(2)
        self.check_in((x, y))
        c = self.colour(a, "xam")
        ax = 0.0 if self.yr[0] <= 0 <= self.yr[1] else self.yr[0]
        ay = 0.0 if self.xr[0] <= 0 <= self.xr[1] else self.xr[0]
        back.append(self.seg(x, y, x, ax, c, 0.5) | {"dash": True})
        back.append(self.seg(x, y, ay, y, c, 0.5) | {"dash": True})

    def _segment(self, cmd, toks, front, t):
        a = self.args(cmd, toks)
        nums = a.need(2, 4) if t == "arrow" else a.need(4)
        xa, ya, xb, yb = (0.0, 0.0, *nums) if len(nums) == 2 else nums
        self.check_in((xa, ya), (xb, yb))
        if (xa, ya) == (xb, yb):
            raise FigureError("the two ends are the same point")
        c = self.colour(a, "do" if t == "arrow" else "muc")
        p = self.seg(xa, ya, xb, yb, c, 1.0, t)
        if "dash" in a.words:
            p["dash"] = True
        front.append(p)
        label = a.label()
        if label:
            mx, my = self.px((xa + xb) / 2), self.py((ya + yb) / 2)
            if "pos" in a.opts:
                front.append(place(mx, my, label, a.pos("n")))
            else:   # beside the middle, on the left of the direction of travel
                dx, dy = self.px(xb) - self.px(xa), self.py(yb) - self.py(ya)
                n = math.hypot(dx, dy)
                nx, ny = dy / n, -dx / n
                pos = ("n" if ny < -0.7 else "s" if ny > 0.7 else "e" if nx > 0 else "w") if abs(nx) < 0.7 or abs(ny) > 0.7 \
                    else ("ne" if nx > 0 and ny < 0 else "nw" if ny < 0 else "se" if nx > 0 else "sw")
                front.append(place(mx + nx * 1.5, my + ny * 1.5, label, pos, 2.5))

    def cmd_vector(self, cmd, toks, back, front):
        self._segment(cmd, toks, front, "arrow")

    def cmd_segment(self, cmd, toks, back, front):
        self._segment(cmd, toks, front, "line")

    def cmd_line(self, cmd, toks, back, front):
        a = self.args(cmd, toks)
        xa, ya, xb, yb = a.need(4)
        if (xa, ya) == (xb, yb):
            raise FigureError("the two points are the same")
        self._infinite(a, xa, ya, xb - xa, yb - ya, front, "muc")

    def _infinite(self, a: Args, xa, ya, dx, dy, front, default):
        big = 4 * (self.xr[1] - self.xr[0] + self.yr[1] - self.yr[0]) / math.hypot(dx, dy)
        seg = self.clip(xa - big * dx, ya - big * dy, xa + big * dx, ya + big * dy)
        if seg is None:
            raise FigureError("the line does not cross the plot")
        p = self.seg(*seg, self.colour(a, default), 1.0)
        if "dash" in a.words:
            p["dash"] = True
        front.append(p)
        if a.label():
            front.append(place(self.px(seg[2]), self.py(seg[3]), a.label(), a.pos("nw" if dy > 0 else "sw")))

    def sample(self, f: Expr, lo: float, hi: float) -> list[list[tuple[float, float]]]:
        """The curve y = f(x) as polylines inside the plot, cut where it jumps or leaves."""
        span = self.yr[1] - self.yr[0]
        runs: list[list[tuple[float, float]]] = []
        cur: list[tuple[float, float]] = []

        def close() -> None:
            nonlocal cur
            if len(cur) > 1:
                runs.append(cur)
            cur = []
        prev = None
        for i in range(self.SAMPLES + 1):
            x = lo + (hi - lo) * i / self.SAMPLES
            y = f(x)
            if y is None:
                close()
                prev = None
                continue
            if prev is not None:
                if abs(y - prev[1]) > span * 0.6:          # a jump (an asymptote): never join it
                    close()
                else:
                    piece = self.clip(prev[0], prev[1], x, y)
                    if piece is None:
                        close()
                    else:
                        start, end = (piece[0], piece[1]), (piece[2], piece[3])
                        if not cur or math.dist(cur[-1], start) > 1e-9:
                            close()
                            cur = [start]
                        cur.append(end)
                        if math.dist(end, (x, y)) > 1e-9:    # it left the plot here
                            close()
            prev = (x, y)
        close()
        return [self.thin(run) for run in runs]

    def thin(self, run: list[tuple[float, float]], eps: float = 0.08) -> list[tuple[float, float]]:
        """Drops the points the drawing does not need: every point removed lies within `eps`
        base units of the polyline that is kept (Ramer-Douglas-Peucker)."""
        pts = [(self.px(x), self.py(y)) for x, y in run]
        keep = [False] * len(pts)
        keep[0] = keep[-1] = True
        stack = [(0, len(pts) - 1)]
        while stack:
            a, b = stack.pop()
            if b - a < 2:
                continue
            (ax, ay), (bx, by) = pts[a], pts[b]
            d = math.hypot(bx - ax, by - ay)
            far, at = -1.0, a
            for i in range(a + 1, b):
                px, py = pts[i]
                off = abs((bx - ax) * (ay - py) - (ax - px) * (by - ay)) / d if d else math.hypot(px - ax, py - ay)
                if off > far:
                    far, at = off, i
            if far > eps:
                keep[at] = True
                stack += [(a, at), (at, b)]
        return [p for p, k in zip(run, keep) if k]

    def polyline(self, run, c, wd=1.0) -> dict:
        return {"t": "polyline", "pts": [[r1(self.px(x)), r1(self.py(y))] for x, y in run], "c": c, "wd": wd}

    def expr(self, toks, cmd, var="x") -> tuple[Expr, list[str]]:
        if not toks:
            raise FigureError(f"{cmd}: needs an expression in {var}")
        return Expr(str(toks[0]), var), toks[1:]

    def domain(self, a: Args, n_extra: int = 0) -> tuple[float, float]:
        nums = a.need(0 + n_extra, 2 + n_extra)
        lo, hi = (nums[n_extra:] if len(nums) == 2 + n_extra else self.xr)
        if lo >= hi:
            raise FigureError("the domain needs a smaller number first")
        return lo, hi

    def cmd_curve(self, cmd, toks, back, front):
        f, rest = self.expr(toks, cmd)
        a = self.args(cmd, rest)
        lo, hi = self.domain(a)
        runs = self.sample(f, lo, hi)
        if not runs:
            raise FigureError(f"y = {f.text} is never inside the plot")
        c = self.colour(a, "xanh")
        for run in runs:
            p = self.polyline(run, c)
            if "dash" in a.words:
                p["dash"] = True
            front.append(p)
        if a.label():
            x, y = runs[-1][-1]
            front.append(place(self.px(x), self.py(y), a.label(), a.pos("nw" if x >= self.xr[1] - 1e-6 else "ne")))

    def cmd_param(self, cmd, toks, back, front):
        if len(toks) < 2:
            raise FigureError("param: needs x(t) and y(t)")
        fx, fy = Expr(str(toks[0]), "t"), Expr(str(toks[1]), "t")
        a = self.args(cmd, toks[2:])
        t0, t1 = a.need(2)
        if t0 >= t1:
            raise FigureError("the range of t needs a smaller number first")
        runs, cur = [], []
        for i in range(self.SAMPLES + 1):
            t = t0 + (t1 - t0) * i / self.SAMPLES
            x, y = fx(t), fy(t)
            if x is None or y is None or not self.inside(x, y, 1e-9):
                if len(cur) > 1:
                    runs.append(cur)
                cur = []
            else:
                cur.append((x, y))
        if len(cur) > 1:
            runs.append(cur)
        if not runs:
            raise FigureError("the curve is never inside the plot")
        for run in runs:
            front.append(self.polyline(run, self.colour(a, "xanh")))
        if a.label():
            x, y = runs[-1][-1]
            front.append(place(self.px(x), self.py(y), a.label(), a.pos("ne")))

    def cmd_area(self, cmd, toks, back, front):
        f, rest = self.expr(toks, cmd)
        a = self.args(cmd, rest)
        lo, hi = a.need(2)
        if lo >= hi:
            raise FigureError("area: needs a < b")
        self.check_in((lo, max(self.yr[0], 0)), (hi, max(self.yr[0], 0)))
        base = min(max(0.0, self.yr[0]), self.yr[1])
        pts = []
        n = 120
        for i in range(n + 1):
            x = lo + (hi - lo) * i / n
            y = f(x)
            if y is None:
                raise FigureError(f"y = {f.text} is not defined everywhere on [{fmt(lo)}, {fmt(hi)}]")
            pts.append((x, min(max(y, self.yr[0]), self.yr[1])))
        poly = [(lo, base)] + pts + [(hi, base)]
        c = self.colour(a, "vang")
        back.append({"t": "poly", "pts": [[r1(self.px(x)), r1(self.py(y))] for x, y in poly], "fill": c, "a": 90})
        if a.label():
            mid = pts[len(pts) // 2]
            front.append(txt(self.px(mid[0]), self.py((mid[1] + base) / 2), a.label(), LABEL, "muc"))

    def cmd_tangent(self, cmd, toks, back, front):
        f, rest = self.expr(toks, cmd)
        a = self.args(cmd, rest)
        (x0,) = a.need(1)
        y0 = f(x0)
        h = 1e-5
        ya, yb = f(x0 - h), f(x0 + h)
        if y0 is None or ya is None or yb is None:
            raise FigureError(f"y = {f.text} has no tangent at x = {fmt(x0)}")
        slope = (yb - ya) / (2 * h)
        self.check_in((x0, y0))
        if "len" not in a.opts:
            self._infinite(a, x0, y0, 1.0, slope, front, "do")
            return
        # a short piece of the tangent, len= base units each side of the point (as drawn)
        half = number(a.opts["len"])
        if not 4 <= half <= 200:
            raise FigureError("tangent: len= must be between 4 and 200 (base units)")
        dx, dy = self.ux, -slope * self.uy
        n = math.hypot(dx, dy)
        sx, sy = half * dx / n / self.ux, -half * dy / n / self.uy      # back to plot units
        seg = self.clip(x0 - sx, y0 - sy, x0 + sx, y0 + sy)
        p = self.seg(*seg, a.colour or "do", 1.0)
        if "dash" in a.words:
            p["dash"] = True
        front.append(p)
        if a.label():
            front.append(place(self.px(seg[2]), self.py(seg[3]), a.label(), a.pos("e")))

    def cmd_poly(self, cmd, toks, back, front):
        a = self.args(cmd, toks)
        if len(a.nums) < 6 or len(a.nums) % 2 or len(a.nums) > 24:
            raise FigureError("poly: needs 3 to 12 corners, x y for each")
        pts = list(zip(a.nums[::2], a.nums[1::2]))
        self.check_in(*pts)
        c = self.colour(a, "vang")
        back.append({"t": "poly", "pts": [[r1(self.px(x)), r1(self.py(y))] for x, y in pts], "fill": c, "a": 80,
                     "edge": c})
        if a.label():
            cx = sum(x for x, _ in pts) / len(pts)
            cy = sum(y for _, y in pts) / len(pts)
            front.append(txt(self.px(cx), self.py(cy), a.label(), LABEL, "muc"))

    def cmd_text(self, cmd, toks, back, front):
        a = self.args(cmd, toks)
        x, y = a.need(2)
        self.check_in((x, y))
        front.append(txt(self.px(x), self.py(y), a.label(True), LABEL, a.colour or "muc",
                         {"c": "center", "n": "midbottom", "s": "midtop", "e": "midleft", "w": "midright",
                          "ne": "bottomleft", "nw": "bottomright", "se": "topleft", "sw": "topright"}[a.pos("c")]))


# ------------------------------------------------------------------ bars
class Bars(Layout):
    SETTINGS = ("max", "min", "values")
    COMMANDS = ("bar", "mark")
    LIMIT = 14

    def build(self):
        bars, marks = [], []
        for cmd, toks, line in self.commands:
            if cmd == "bar":
                if not toks:
                    raise FigureError(f"{line!r}: bar needs a label and a value")
                a = self.args(cmd, toks[1:])
                (v,) = a.need(1)
                raw = next(t for t in toks[1:] if not isinstance(t, Label) and t not in COLOURS)
                bars.append((str(toks[0]), v, a.colour or "xanh", raw))
            else:
                a = self.args(cmd, toks)
                (pos,) = a.need(1)
                marks.append((pos, a.colour or "do", a.label()))
        if not bars or len(bars) > 12:
            raise FigureError("a bar chart needs 1 to 12 bars")
        vals = [b[1] for b in bars]
        top = self.setting_nums("max", (1,), [max(0.0, max(vals))])[0]
        bot = self.setting_nums("min", (1,), [min(0.0, min(vals))])[0]
        if top <= bot or max(vals) > top + 1e-9 or min(vals) < bot - 1e-9:
            raise FigureError("max: and min: must hold every value")
        values = self.flag("values", True)
        n = len(bars)
        slot = max(max(tw(b[0]) for b in bars) + 6, max(tw(b[3], SMALL) for b in bars) + 6, 28)
        w = self.size[0] if self.size else min(MAX_W, n * slot + 8)
        h = self.size[1] if self.size and len(self.size) > 1 else 90
        slot = (w - 8) / n
        if slot < max(max(tw(b[0]) for b in bars), max(tw(b[3], SMALL) for b in bars)) + 2:
            raise FigureError("the bar labels do not fit: shorter labels or a wider size:")
        mark_h = th() + 1 if any(m[2] for m in marks) else 0
        mt = 3 + mark_h + (th(SMALL) if values else 0)
        mb = th() + 3 + (th(SMALL) if values and bot < 0 else 0)
        ph = h - mt - mb
        if ph < 20:
            raise FigureError("the figure is too short for its bars")
        k = ph / (top - bot)
        y_of = lambda v: mt + (top - v) * k      # noqa: E731
        base = y_of(0.0) if bot <= 0 <= top else y_of(bot)
        prims: list[dict] = []
        bw = min(slot * 0.62, 26)
        for i, (lbl, v, c, raw) in enumerate(bars):
            cx = 4 + slot * (i + 0.5)
            yv = y_of(v)
            y0, y1 = min(yv, base), max(yv, base)
            prims.append({"t": "rect", "x": r1(cx - bw / 2), "y": r1(y0), "w": r1(bw), "h": r1(max(0.6, y1 - y0)),
                          "fill": c, "a": 170, "edge": c})
            if values:      # the value as the author wrote it: 3/8 stays 3/8
                prims.append(txt(cx, yv - 1 if v >= 0 else yv + 1, raw, SMALL, "muc",
                                 "midbottom" if v >= 0 else "midtop"))
            prims.append(txt(cx, h - th() - 1, lbl, LABEL, "muc", "midtop"))
        prims.append({"t": "line", "x1": 2, "y1": r1(base), "x2": r1(w - 2), "y2": r1(base), "c": "muc", "wd": 0.7})
        for pos, c, lbl in marks:
            if not -0.5 <= pos <= n - 0.5:
                raise FigureError(f"mark {fmt(pos)}: outside the bars (the first bar is 0, the last {n - 1})")
            mx = 4 + slot * (pos + 0.5)
            prims.append({"t": "line", "x1": r1(mx), "y1": r1(2 + mark_h), "x2": r1(mx), "y2": r1(base), "c": c,
                          "wd": 1.0, "dash": True})
            if lbl:
                prims.append(txt(mx, 1, lbl, LABEL, c, "midtop"))
        return w, h, prims


# ------------------------------------------------------------------ graph
class Graph(Layout):
    SETTINGS = ("layout", "directed")
    COMMANDS = ("node", "edge")
    WORDS = {"edge": ("dash",)}
    LIMIT = 40

    def build(self):
        nodes: dict[str, dict] = {}
        edges: list[dict] = []
        for cmd, toks, line in self.commands:
            if not toks or isinstance(toks[0], Label):
                raise FigureError(f"{line!r}: {cmd} needs a node name first (no quotes)")
            try:
                if cmd == "node":
                    name = toks[0]
                    if name in nodes:
                        raise FigureError(f"node {name} twice")
                    a = self.args(cmd, toks[1:])
                    xy = a.need(0, 2)
                    nodes[name] = {"label": a.label() or name, "xy": xy or None, "c": a.colour}
                else:
                    if len(toks) < 2:
                        raise FigureError("edge needs two node names")
                    u, v = toks[0], toks[1]
                    a = self.args(cmd, toks[2:])
                    nums = a.need(0, 1)
                    weight = a.label() or (fmt(nums[0]) if nums else "")
                    edges.append({"u": u, "v": v, "w": weight, "c": a.colour, "dash": "dash" in a.words})
            except FigureError as e:
                raise FigureError(f"{line!r}: {e}") from None
        if not nodes or len(nodes) > 16:
            raise FigureError("a graph needs 1 to 16 nodes")
        for e in edges:
            for end in (e["u"], e["v"]):
                if end not in nodes:
                    raise FigureError(f"edge {e['u']} {e['v']}: no node {end}")
            if e["u"] == e["v"]:
                raise FigureError(f"edge {e['u']} {e['v']}: a loop cannot be drawn")
        directed = self.flag("directed", False)
        layout = self.settings.get("layout", "free" if all(n["xy"] for n in nodes.values()) else "circle")
        if layout not in ("free", "circle", "tree", "ltr"):
            raise FigureError("layout: must be free, circle, tree or ltr")
        w = self.size[0] if self.size else 200
        h = self.size[1] if self.size and len(self.size) > 1 else 110
        for n in nodes.values():
            lw = tw(n["label"])
            n["shape"] = ("circle", max(6.0, lw / 2 + 2.5)) if lw <= 11 else ("rect", lw + 7, 12.0)
        pad_x = max(n["shape"][1] if n["shape"][0] == "circle" else n["shape"][1] / 2 for n in nodes.values()) + 2
        pad_y = max(n["shape"][1] if n["shape"][0] == "circle" else 6.0 for n in nodes.values()) + 2
        names = list(nodes)
        if layout == "free":
            if not all(n["xy"] for n in nodes.values()):
                raise FigureError("layout: free needs x y on every node")
            xs = [nodes[k]["xy"][0] for k in names]
            ys = [nodes[k]["xy"][1] for k in names]
            sx = (w - 2 * pad_x) / ((max(xs) - min(xs)) or 1)
            sy = (h - 2 * pad_y) / ((max(ys) - min(ys)) or 1)
            for k in names:
                x, y = nodes[k]["xy"]
                nodes[k]["p"] = (pad_x + (x - min(xs)) * sx if max(xs) > min(xs) else w / 2,
                                 pad_y + (max(ys) - y) * sy if max(ys) > min(ys) else h / 2)
        elif layout == "circle":
            rx, ry = w / 2 - pad_x, h / 2 - pad_y
            for i, k in enumerate(names):
                t = -math.pi / 2 + 2 * math.pi * i / len(names)
                nodes[k]["p"] = (w / 2 + rx * math.cos(t), h / 2 + ry * math.sin(t)) if len(names) > 1 else (w / 2, h / 2)
        else:
            self.tree(nodes, edges, names[0], layout == "ltr", w, h, pad_x, pad_y)
        prims: list[dict] = []
        labels: list[dict] = []
        for e in edges:
            a, b = nodes[e["u"]], nodes[e["v"]]
            (xa, ya), (xb, yb) = a["p"], b["p"]
            d = math.hypot(xb - xa, yb - ya)
            if d < 1:
                raise FigureError(f"edge {e['u']} {e['v']}: the two nodes are on top of each other")
            ux, uy = (xb - xa) / d, (yb - ya) / d
            sa, sb = self.edge_cut(a, ux, uy), self.edge_cut(b, -ux, -uy)
            p = {"t": "arrow" if directed else "line", "x1": r1(xa + ux * sa), "y1": r1(ya + uy * sa),
                 "x2": r1(xb - ux * (sb + 0.5)), "y2": r1(yb - uy * (sb + 0.5)), "c": e["c"] or "xam",
                 "wd": 1.4 if e["c"] else 0.8}
            if e["dash"]:
                p["dash"] = True
            prims.append(p)
            if e["w"]:
                mx, my = (xa + xb) / 2, (ya + yb) / 2
                nx, ny = -uy, ux
                if ny > 0 or (abs(ny) < 1e-9 and nx < 0):
                    nx, ny = -nx, -ny
                lx, ly = mx + nx * 6, my + ny * 6
                lw_, lh_ = tw(e["w"], SMALL) + 2, th(SMALL)
                labels.append({"t": "rect", "x": r1(lx - lw_ / 2), "y": r1(ly - lh_ / 2), "w": r1(lw_), "h": r1(lh_),
                               "fill": "giay", "a": 255})
                labels.append(txt(lx, ly, e["w"], SMALL, e["c"] or "muc"))
        for k in names:
            n = nodes[k]
            x, y = n["p"]
            c = n["c"]
            fill, a = (c, 90) if c else ("giay", 255)
            edge = c or "muc"
            if n["shape"][0] == "circle":
                prims.append({"t": "circle", "x": r1(x), "y": r1(y), "r": r1(n["shape"][1]), "fill": fill, "a": a,
                              "edge": edge, "wd": 1.0 if c else 0.7})
            else:
                bw, bh = n["shape"][1], n["shape"][2]
                prims.append({"t": "rect", "x": r1(x - bw / 2), "y": r1(y - bh / 2), "w": r1(bw), "h": r1(bh),
                              "fill": fill, "a": a, "edge": edge, "r": 3})
            prims.append(txt(x, y, n["label"], LABEL, "muc"))
        return w, h, prims + labels

    @staticmethod
    def edge_cut(n: dict, ux: float, uy: float) -> float:
        """How far from the centre of a node an edge in direction (ux, uy) leaves it."""
        if n["shape"][0] == "circle":
            return n["shape"][1]
        bw, bh = n["shape"][1] / 2, n["shape"][2] / 2
        return min(bw / abs(ux) if abs(ux) > 1e-9 else 1e9, bh / abs(uy) if abs(uy) > 1e-9 else 1e9)

    @staticmethod
    def tree(nodes, edges, root, ltr, w, h, pad_x, pad_y) -> None:
        children: dict[str, list[str]] = {k: [] for k in nodes}
        seen = {root}
        order = [root]
        depth = {root: 0}
        i = 0
        while i < len(order):
            u = order[i]
            i += 1
            for e in edges:
                for a, b in ((e["u"], e["v"]), (e["v"], e["u"])):
                    if a == u and b not in seen:
                        seen.add(b)
                        children[u].append(b)
                        depth[b] = depth[u] + 1
                        order.append(b)
        if len(seen) != len(nodes):
            missing = [k for k in nodes if k not in seen]
            raise FigureError(f"layout: tree needs every node joined to {root} (not {', '.join(missing)})")
        leaves: list[str] = []

        def walk(u):
            if not children[u]:
                leaves.append(u)
            for c in children[u]:
                walk(c)
        walk(root)
        levels = max(depth.values()) + 1
        across = (h if ltr else w) - 2 * (pad_y if ltr else pad_x)
        along = (w if ltr else h) - 2 * (pad_x if ltr else pad_y)
        slot: dict[str, float] = {}
        for j, leaf in enumerate(leaves):
            slot[leaf] = (j + 0.5) / len(leaves) * across

        def centre(u):
            if children[u]:
                vals = [centre(c) for c in children[u]]
                slot[u] = (vals[0] + vals[-1]) / 2
            return slot[u]
        centre(root)
        for k in nodes:
            d = depth[k] / (levels - 1) * along if levels > 1 else along / 2
            if ltr:
                nodes[k]["p"] = (pad_x + d, pad_y + slot[k])
            else:
                nodes[k]["p"] = (pad_x + slot[k], pad_y + d)


# ------------------------------------------------------------------ sets
class Sets(Layout):
    SETTINGS = ("universe",)
    COMMANDS = ("set", "shade", "in")
    LIMIT = 16
    TOKEN = re.compile(r"\s*([A-Za-z]\w*|[&|\-~()])")

    def build(self):
        sets: list[tuple[str, str, str]] = []
        shades, texts = [], []
        for cmd, toks, line in self.commands:
            try:
                if cmd == "set":
                    if not toks or isinstance(toks[0], Label):
                        raise FigureError("set needs a name first, like set A \"Nhãn\" xanh")
                    a = self.args(cmd, toks[1:])
                    a.need(0)
                    sets.append((toks[0], a.label() or toks[0], a.colour))
                else:
                    if not toks:
                        raise FigureError(f"{cmd} needs a region, like A&B or A-B")
                    a = self.args(cmd, toks[1:])
                    a.need(0)
                    (shades if cmd == "shade" else texts).append((str(toks[0]), a.colour, a.label(cmd == "in")))
            except FigureError as e:
                raise FigureError(f"{line!r}: {e}") from None
        if len(sets) not in (2, 3):
            raise FigureError("a Venn diagram needs 2 or 3 sets")
        names = [s[0] for s in sets]
        if len(set(names)) != len(names):
            raise FigureError("two sets have the same name")
        w = self.size[0] if self.size else 190
        h = self.size[1] if self.size and len(self.size) > 1 else 105
        universe = self.settings.get("universe", "").strip().strip('"')
        top = th() + 2 if universe else 0
        default = ("xanh", "do", "luc")
        if len(sets) == 2:
            r = min((h - top - 6) / 2, (w - 12) / 3.3)
            cy = top + (h - top) / 2
            circles = [(w / 2 - r * 0.62, cy, r), (w / 2 + r * 0.62, cy, r)]
        else:
            r = min((h - top - 6) / 3.6, (w - 12) / 3.8)
            cy = top + (h - top) / 2
            circles = [(w / 2 - r * 0.6, cy - r * 0.42, r), (w / 2 + r * 0.6, cy - r * 0.42, r),
                       (w / 2, cy + r * 0.62, r)]
        self.circles = circles
        self.names = names
        self.w, self.h, self.top = w, h, top
        prims: list[dict] = []
        if universe or any("~" in s[0] for s in shades + texts):
            prims.append({"t": "rect", "x": 1, "y": r1(top), "w": r1(w - 2), "h": r1(h - top - 1), "edge": "muc",
                          "wd": 0.7})
            if universe:
                prims.append(txt(3, 0, universe, LABEL, "muc", "topleft"))
        for (name, label, c), (x, y, rr) in zip(sets, circles):
            prims.append({"t": "circle", "x": r1(x), "y": r1(y), "r": r1(rr), "fill": c or "giay", "a": 50 if c else 0})
        for region, c, _ in shades:
            test = self.region(region)
            prims.append(self.spans(test, c or "vang"))
        for i, ((name, label, c), (x, y, rr)) in enumerate(zip(sets, circles)):
            prims.append({"t": "circle", "x": r1(x), "y": r1(y), "r": r1(rr), "edge": c or default[i], "wd": 1.0})
            if len(sets) == 2:
                lx = x - rr * 0.75 if i == 0 else x + rr * 0.75
                prims.append(txt(lx, y - rr * 0.78, label, LABEL, c or default[i], "bottomright" if i == 0 else "bottomleft"))
            else:
                lx, ly, anchor = [(x - rr * 0.72, y - rr * 0.72, "bottomright"), (x + rr * 0.72, y - rr * 0.72, "bottomleft"),
                                  (x + rr * 0.8, y + rr * 0.7, "topleft")][i]
                prims.append(txt(lx, ly, label, LABEL, c or default[i], anchor))
        for region, c, label in texts:
            cx, cy = self.centre(self.region(region), region)
            prims.append(txt(cx, cy, label, LABEL, c or "muc"))
        return w, h, prims

    def region(self, text: str):
        """A test (x, y) -> bool for a region like A&B, A-B, A|B, ~(A|B)."""
        toks, pos = [], 0
        while pos < len(text):
            m = self.TOKEN.match(text, pos)
            if not m:
                raise FigureError(f"region {text!r}: use set names with & | - ~ and brackets")
            toks.append(m.group(1))
            pos = m.end()
        i = 0

        def atom():
            nonlocal i
            if i >= len(toks):
                raise FigureError(f"region {text!r} ends too early")
            t = toks[i]
            i += 1
            if t == "~":
                inner = atom()
                return lambda p: not inner(p)
            if t == "(":
                inner = expr()
                if i >= len(toks) or toks[i] != ")":
                    raise FigureError(f"region {text!r}: a ( is never closed")
                i += 1
                return inner
            if t not in self.names:
                raise FigureError(f"region {text!r}: no set {t}")
            k = self.names.index(t)
            cx, cy, r = self.circles[k]
            return lambda p: (p[0] - cx) ** 2 + (p[1] - cy) ** 2 <= r * r

        def expr():
            nonlocal i
            left = atom()
            while i < len(toks) and toks[i] in "&|-":
                op = toks[i]
                i += 1
                right = atom()
                left = {"&": lambda a, b: lambda p: a(p) and b(p), "|": lambda a, b: lambda p: a(p) or b(p),
                        "-": lambda a, b: lambda p: a(p) and not b(p)}[op](left, right)
            return left
        test = expr()
        if i != len(toks):
            raise FigureError(f"region {text!r}: something is left over at {toks[i]!r}")
        return test

    def inside_box(self, p) -> bool:
        return 1 < p[0] < self.w - 1 and self.top < p[1] < self.h - 1

    def spans(self, test, c: str) -> dict:
        """The region as rows of x intervals, one row per base unit."""
        rows = []
        y0, dy = self.top + 1.0, 1.0
        y = y0
        while y < self.h - 1:
            yc = y + dy / 2
            cuts = {1.0, self.w - 1.0}
            for cx, cy, r in self.circles:
                if abs(yc - cy) < r:
                    half = math.sqrt(r * r - (yc - cy) ** 2)
                    cuts.update((cx - half, cx + half))
            cuts = sorted(v for v in cuts if 1.0 <= v <= self.w - 1.0)
            row: list[float] = []
            for a, b in zip(cuts, cuts[1:]):
                if b - a > 1e-6 and test(((a + b) / 2, yc)):
                    if row and abs(row[-1] - a) < 1e-6:
                        row[-1] = r1(b)
                    else:
                        row += [r1(a), r1(b)]
            rows.append(row)
            y += dy
        if not any(rows):
            raise FigureError("a shaded region is empty")
        return {"t": "spans", "y": r1(y0), "dy": dy, "rows": rows, "c": c, "a": 110}

    def centre(self, test, region: str) -> tuple[float, float]:
        pts = [(x + 0.5, y + 0.5) for x in range(int(self.w)) for y in range(int(self.top), int(self.h))
               if self.inside_box((x + 0.5, y + 0.5)) and test((x + 0.5, y + 0.5))]
        if not pts:
            raise FigureError(f"region {region!r} is empty")

        def room(p) -> float:
            """How far the point is from the nearest edge (a circle or the frame); a
            label is wider than tall, so sideways room counts a little less."""
            d = min(abs(math.hypot(p[0] - cx, p[1] - cy) - r) for cx, cy, r in self.circles)
            return min(d, (p[0] - 1) * 0.6, (self.w - 1 - p[0]) * 0.6, p[1] - self.top, self.h - 1 - p[1])
        mx = sum(p[0] for p in pts) / len(pts)
        my = sum(p[1] for p in pts) / len(pts)
        # the point with the most room around it; between equals, the one nearest the middle
        return max(pts, key=lambda p: (round(room(p), 0), -math.hypot(p[0] - mx, p[1] - my)))


# ------------------------------------------------------------------ map (ánh xạ)
class Map(Layout):
    SETTINGS = ()
    COMMANDS = ("col", "gap")
    LIMIT = 30
    ROW = 13

    def build(self):
        cols: list[dict] = []
        gaps: dict[int, str] = {}
        arrows = []
        for cmd, toks, line in self.commands:
            if cmd == "col":
                if not toks:
                    raise FigureError(f"{line!r}: col needs a title, then its elements")
                title, elems = str(toks[0]), [str(t) for t in toks[1:]]
                colour = None
                if elems and elems[-1] in COLOURS and not isinstance(toks[-1], Label):
                    colour = elems.pop()
                if not 1 <= len(elems) <= 7:
                    raise FigureError(f"{line!r}: a column holds 1 to 7 elements")
                if len(set(elems)) != len(elems):
                    raise FigureError(f"{line!r}: an element is written twice")
                cols.append({"title": title, "elems": elems, "c": colour})
            elif cmd == "gap":
                a = self.args(cmd, toks)
                (k,) = a.need(1)
                gaps[int(k)] = a.label(True)
        if len(cols) not in (2, 3):
            raise FigureError("a mapping diagram needs 2 or 3 columns (col lines)")
        for line in self._arrow_lines:
            parts = tokens(line)
            if len(parts) < 3 or parts[1] != "->":
                raise FigureError(f"{line!r}: write an arrow as  1 -> a")
            src, dst = str(parts[0]), str(parts[2])
            colour = parts[3] if len(parts) > 3 else None
            if colour is not None and colour not in COLOURS or len(parts) > 4:
                raise FigureError(f"{line!r}: after the arrow only a colour may follow")
            hit = [k for k in range(len(cols) - 1) if src in cols[k]["elems"] and dst in cols[k + 1]["elems"]]
            if not hit:
                raise FigureError(f"{line!r}: {src} and {dst} are not in two columns side by side")
            if len(hit) > 1:
                raise FigureError(f"{line!r}: {src} -> {dst} could be between two pairs of columns")
            arrows.append((hit[0], src, dst, colour))
        for k in gaps:
            if not 1 <= k <= len(cols) - 1:
                raise FigureError(f"gap {k}: there are {len(cols) - 1} gaps between the columns")
        gap_w = max([44.0] + [tw(t) + 12 for t in gaps.values()])
        for c in cols:
            c["w"] = max(26.0, max(tw(e) for e in c["elems"]) + 14, tw(c["title"]) + 4)
        total = sum(c["w"] for c in cols) + gap_w * (len(cols) - 1)
        if self.size:
            gap_w = max(gap_w, (self.size[0] - sum(c["w"] for c in cols)) / (len(cols) - 1))
            total = sum(c["w"] for c in cols) + gap_w * (len(cols) - 1)
        rows = max(len(c["elems"]) for c in cols)
        top = th() + 2
        body = rows * self.ROW + 8
        h = top + body + 1
        prims: list[dict] = []
        x = 0.0
        pos: list[dict[str, tuple[float, float]]] = []
        for i, c in enumerate(cols):
            colour = c["c"] or ("xanh", "luc", "tim")[i]
            cx = x + c["w"] / 2
            prims.append({"t": "rect", "x": r1(x), "y": r1(top), "w": r1(c["w"]), "h": r1(body), "fill": colour,
                          "a": 40, "edge": colour, "r": 8})
            prims.append(txt(cx, 0, c["title"], LABEL, colour, "midtop"))
            here = {}
            n = len(c["elems"])
            y0 = top + 4 + (rows - n) * self.ROW / 2
            for j, e in enumerate(c["elems"]):
                ey = y0 + self.ROW * (j + 0.5)
                prims.append(txt(cx, ey, e, LABEL, "muc"))
                here[e] = (cx, ey, tw(e) / 2)
            pos.append(here)
            if i < len(cols) - 1 and (i + 1) in gaps:
                prims.append(txt(x + c["w"] + gap_w / 2, 0, gaps[i + 1], LABEL, "muc", "midtop"))
            x += c["w"] + gap_w
        for k, src, dst, colour in arrows:
            (xa, ya, ha), (xb, yb, hb) = pos[k][src], pos[k + 1][dst]
            prims.append({"t": "arrow", "x1": r1(xa + ha + 2), "y1": r1(ya), "x2": r1(xb - hb - 2.5), "y2": r1(yb),
                          "c": colour or "muc", "wd": 1.2 if colour else 0.8, "head": 3.5})
        return total, h, prims

    def __init__(self, settings, commands, size):
        self._arrow_lines = [line for cmd, toks, line in commands if "->" in toks]
        super().__init__(settings, [c for c in commands if "->" not in c[1]], size)
        if len(self._arrow_lines) > 30:
            raise FigureError("at most 30 arrows")


# ------------------------------------------------------------------ grid (tables, matrices)
class Grid(Layout):
    SETTINGS = ("style",)
    COMMANDS = ("table", "head", "side", "row", "mark", "op")
    LIMIT = 40
    ROW = 12

    def build(self):
        style = self.settings.get("style", "table")
        if style not in ("table", "matrix"):
            raise FigureError("style: must be table or matrix")
        parts: list[dict] = []
        cur = None

        def table(title=""):
            t = {"kind": "table", "title": title, "head": [], "side": [], "rows": [], "marks": []}
            parts.append(t)
            return t
        for cmd, toks, line in self.commands:
            try:
                if cmd == "table":
                    a = self.args(cmd, toks)
                    a.need(0)
                    cur = table(a.label())
                    continue
                if cmd == "op":
                    a = self.args(cmd, toks)
                    a.need(0)
                    parts.append({"kind": "op", "s": a.label(True)})
                    cur = None
                    continue
                if cur is None:
                    cur = table()
                if cmd in ("head", "side", "row"):
                    cells = [str(t) for t in toks]
                    if not cells:
                        raise FigureError(f"{cmd} needs cells")
                    if cmd == "row":
                        cur["rows"].append(cells)
                    elif cur[cmd]:
                        raise FigureError(f"{cmd} twice in one table")
                    else:
                        cur[cmd] = cells
                else:   # mark row I / mark col J / mark cell I J / mark diag
                    if not toks or toks[0] not in ("row", "col", "cell", "diag"):
                        raise FigureError("write mark row 1, mark col 2, mark cell 1 2 or mark diag")
                    a = self.args(cmd, toks[1:])
                    want = {"row": 1, "col": 1, "cell": 2, "diag": 0}[toks[0]]
                    nums = [int(v) for v in a.need(want)]
                    cur["marks"].append((toks[0], nums, a.colour or "vang"))
            except FigureError as e:
                raise FigureError(f"{line!r}: {e}") from None
        tables = [p for p in parts if p["kind"] == "table"]
        if not tables or len(tables) > 4:
            raise FigureError("a grid needs 1 to 4 tables")
        for t in tables:
            rows = t["rows"]
            if not rows:
                raise FigureError(f"table {t['title']!r} has no row")
            if len({len(r) for r in rows}) != 1:
                raise FigureError(f"table {t['title']!r}: every row needs the same number of cells")
            if len(rows) > 8 or len(rows[0]) > 8:
                raise FigureError(f"table {t['title']!r}: at most 8 rows and 8 columns")
            if t["head"] and len(t["head"]) != len(rows[0]):
                raise FigureError(f"table {t['title']!r}: head has {len(t['head'])} cells for {len(rows[0])} columns")
            if t["side"] and len(t["side"]) != len(rows):
                raise FigureError(f"table {t['title']!r}: side has {len(t['side'])} cells for {len(rows)} rows")
            for kind, nums, _ in t["marks"]:
                if kind == "row" and not 1 <= nums[0] <= len(rows) or \
                        kind == "col" and not 1 <= nums[0] <= len(rows[0]) or \
                        kind == "cell" and not (1 <= nums[0] <= len(rows) and 1 <= nums[1] <= len(rows[0])):
                    raise FigureError(f"table {t['title']!r}: mark {kind} {' '.join(map(str, nums))} is outside it")
                if kind == "diag" and len(rows) != len(rows[0]):
                    raise FigureError(f"table {t['title']!r}: mark diag needs a square table")
        prims: list[dict] = []
        sizes = []
        for p in parts:
            if p["kind"] == "op":
                sizes.append((tw(p["s"], 9) + 8, 0.0))
                continue
            ncol = len(p["rows"][0])
            cws = [max(12.0, max(tw(r[j]) for r in p["rows"] + ([p["head"]] if p["head"] else [])) + 6)
                   for j in range(ncol)]
            sw = (max(tw(s, SMALL) for s in p["side"]) + 5) if p["side"] else 0.0
            p["cws"], p["sw"] = cws, sw
            # a table's head is a shaded first row; a matrix's is small grey labels above it
            p["hh"] = (self.ROW if style == "table" else th(SMALL) + 3) if p["head"] else 0.0
            p["th"] = (th() + (5 if p["head"] else 2)) if p["title"] else 0.0
            width = sw + sum(cws) + (8 if style == "matrix" else 0)
            p["width"] = max(width, tw(p["title"]) if p["title"] else 0)
            sizes.append((p["width"], p["th"] + p["hh"] + self.ROW * len(p["rows"])))
        h = max(s[1] for s in sizes)
        w = sum(s[0] for s in sizes) + 6 * (len(parts) - 1)
        mids = [(h - ph) / 2 + p["th"] + p["hh"] + self.ROW * len(p["rows"]) / 2
                for p, (_, ph) in zip(parts, sizes) if p["kind"] == "table"]
        mid = sum(mids) / len(mids)          # an operator sits level with the middle of the cells
        x = 0.0
        for p, (pw, ph) in zip(parts, sizes):
            if p["kind"] == "op":
                prims.append(txt(x + pw / 2, mid, p["s"], 9, "muc"))
                x += pw + 6
                continue
            y0 = (h - ph) / 2
            gx = x + (pw - (p["sw"] + sum(p["cws"]) + (8 if style == "matrix" else 0))) / 2
            if p["title"]:
                prims.append(txt(x + pw / 2, y0, p["title"], LABEL, "do", "midtop"))
            top = y0 + p["th"] + p["hh"]
            left = gx + p["sw"] + (4 if style == "matrix" else 0)
            nrow, ncol = len(p["rows"]), len(p["cws"])
            colx = [left + sum(p["cws"][:j]) for j in range(ncol + 1)]
            tint: dict[tuple[int, int], tuple[str, int]] = {}
            edges = []
            for kind, nums, c in p["marks"]:
                if kind == "row":
                    cells = [(nums[0] - 1, j) for j in range(ncol)]
                elif kind == "col":
                    cells = [(i, nums[0] - 1) for i in range(nrow)]
                elif kind == "cell":
                    cells = [(nums[0] - 1, nums[1] - 1)]
                else:
                    cells = [(i, i) for i in range(nrow)]
                for cell in cells:
                    tint[cell] = (c, 200 if kind == "cell" else 110)
                if kind == "cell":
                    edges.append((cells[0], c))
            for (i, j), (c, a) in sorted(tint.items(), key=lambda kv: kv[1][1]):
                prims.append({"t": "rect", "x": r1(colx[j]), "y": r1(top + i * self.ROW), "w": r1(p["cws"][j]),
                              "h": self.ROW, "fill": c, "a": a})
            if style == "table":
                first = top - p["hh"]
                if p["head"]:
                    prims.append({"t": "rect", "x": r1(left), "y": r1(first), "w": r1(colx[-1] - left), "h": self.ROW,
                                  "fill": "xam", "a": 70})
                for i in range(-1 if p["head"] else 0, nrow + 1):
                    prims.append({"t": "line", "x1": r1(left), "y1": r1(top + i * self.ROW), "x2": r1(colx[-1]),
                                  "y2": r1(top + i * self.ROW), "c": "xam", "wd": 0.5})
                for j in range(ncol + 1):
                    prims.append({"t": "line", "x1": r1(colx[j]), "y1": r1(first), "x2": r1(colx[j]),
                                  "y2": r1(top + nrow * self.ROW), "c": "xam", "wd": 0.5})
            else:
                yb = top + nrow * self.ROW
                for bx, tick in ((left - 3, 3), (colx[-1] + 3, -3)):
                    prims.append({"t": "polyline", "pts": [[r1(bx + tick), r1(top)], [r1(bx), r1(top)], [r1(bx), r1(yb)],
                                                           [r1(bx + tick), r1(yb)]], "c": "muc", "wd": 0.8})
            for (i, j), c in edges:
                prims.append({"t": "rect", "x": r1(colx[j]), "y": r1(top + i * self.ROW), "w": r1(p["cws"][j]),
                              "h": self.ROW, "edge": c, "wd": 1.0})
            for i, row in enumerate(p["rows"]):
                for j, v in enumerate(row):
                    prims.append(txt(colx[j] + p["cws"][j] / 2, top + i * self.ROW + self.ROW / 2, v, LABEL, "muc"))
            for j, v in enumerate(p["head"]):
                if style == "table":
                    prims.append(txt(colx[j] + p["cws"][j] / 2, top - self.ROW / 2, v, LABEL, "muc"))
                else:
                    prims.append(txt(colx[j] + p["cws"][j] / 2, top - 2, v, SMALL, "xam", "midbottom"))
            for i, v in enumerate(p["side"]):
                prims.append(txt(gx + p["sw"] - 3, top + i * self.ROW + self.ROW / 2, v, SMALL, "xam", "midright"))
            x += pw + 6
        return w, h, prims


# ------------------------------------------------------------------ number line
class NumberLine(Layout):
    SETTINGS = ("range",)
    COMMANDS = ("point", "interval", "nbhd", "seq")
    WORDS = {"point": ("open",), "interval": ("[", "(", "]", ")", "-inf", "inf")}
    LIMIT = 16

    def build(self):
        lo, hi, *st = self.setting_nums("range", (2, 3), [-1, 5])
        if lo >= hi:
            raise FigureError("range: needs a smaller number first")
        step = st[0] if st else Plane.auto_step(hi - lo)
        if step <= 0 or (hi - lo) / step > 24:
            raise FigureError("range: at most 24 ticks")
        w = self.size[0] if self.size else 300
        ml = mr = 10
        k = (w - ml - mr) / (hi - lo)
        xof = lambda v: ml + (v - lo) * k     # noqa: E731
        items = []
        for cmd, toks, line in self.commands:
            try:
                if cmd == "seq":
                    if not toks:
                        raise FigureError("seq needs an expression in n")
                    f = Expr(str(toks[0]), "n")
                    a = self.args(cmd, toks[1:])
                    n0, n1 = (int(v) for v in a.need(2))
                    if not 0 <= n0 < n1 <= n0 + 60:
                        raise FigureError("seq: n goes from a to b, at most 60 terms")
                    vals = [f(n) for n in range(n0, n1 + 1)]
                    if any(v is None or not lo <= v <= hi for v in vals):
                        raise FigureError(f"seq: a term of {f.text} is outside range:")
                    items.append(("seq", vals, a.colour or "xanh", a.label()))
                elif cmd == "point":
                    a = self.args(cmd, toks)
                    (v,) = a.need(1)
                    if not lo <= v <= hi:
                        raise FigureError(f"point {fmt(v)} is outside range:")
                    items.append(("point", v, a.colour or "do", a.label(), "open" in a.words))
                elif cmd == "interval":
                    a = self.args(cmd, toks)
                    nums = list(a.nums)
                    if "-inf" in a.words:
                        nums.insert(0, lo)
                    if "inf" in a.words:
                        nums.append(hi)
                    if len(nums) != 2 or nums[0] >= nums[1]:
                        raise FigureError("interval needs a < b (or -inf / inf)")
                    if nums[0] < lo or nums[1] > hi:
                        raise FigureError("interval is outside range:")
                    left_open = "(" in a.words or "-inf" in a.words
                    right_open = ")" in a.words or "inf" in a.words
                    items.append(("interval", nums, a.colour or "xanh", a.label(), left_open, right_open,
                                  "-inf" in a.words, "inf" in a.words))
                else:
                    a = self.args(cmd, toks)
                    c, r = a.need(2)
                    if r <= 0 or c - r < lo or c + r > hi:
                        raise FigureError("nbhd needs a centre and a radius > 0 inside range:")
                    items.append(("nbhd", (c, r), a.colour or "luc", a.label()))
            except FigureError as e:
                raise FigureError(f"{line!r}: {e}") from None
        levels = sum(1 for it in items if it[0] in ("interval", "nbhd"))
        band = 11.0
        top = 3 + levels * band + (th() if any(it[0] == "point" and it[3] for it in items) else 0)
        base = top + 4
        h = base + 4 + th(SMALL) + 2
        prims = [{"t": "arrow", "x1": 2, "y1": r1(base), "x2": r1(w - 2), "y2": r1(base), "c": "muc", "wd": 0.7,
                  "head": 3}]
        for v in Plane.ticks(lo, hi, step):
            prims.append({"t": "line", "x1": r1(xof(v)), "y1": r1(base - 2), "x2": r1(xof(v)), "y2": r1(base + 2),
                          "c": "muc", "wd": 0.5})
            prims.append(txt(xof(v), base + 3.5, fmt(v), SMALL, "xam", "midtop"))
        level = 0
        for it in items:
            if it[0] in ("interval", "nbhd"):
                yb = top - level * band
                level += 1
                if it[0] == "interval":
                    (a_, b_), c, lbl, lo_open, hi_open, linf, rinf = it[1], it[2], it[3], it[4], it[5], it[6], it[7]
                else:
                    (cc, rr), c, lbl = it[1], it[2], it[3]
                    a_, b_, lo_open, hi_open, linf, rinf = cc - rr, cc + rr, True, True, False, False
                    prims.append({"t": "circle", "x": r1(xof(cc)), "y": r1(base), "r": 1.8, "fill": c, "a": 255})
                xa, xb = xof(a_), xof(b_)
                prims.append({"t": "rect", "x": r1(xa), "y": r1(base - 1.5), "w": r1(xb - xa), "h": 3, "fill": c,
                              "a": 150})
                prims.append({"t": "line", "x1": r1(xa), "y1": r1(yb), "x2": r1(xb), "y2": r1(yb), "c": c, "wd": 0.6,
                              "dash": True})
                for xe, open_, inf in ((xa, lo_open, linf), (xb, hi_open, rinf)):
                    if inf:
                        continue
                    prims.append({"t": "line", "x1": r1(xe), "y1": r1(yb), "x2": r1(xe), "y2": r1(base), "c": c,
                                  "wd": 0.6, "dash": True})
                    prims.append({"t": "circle", "x": r1(xe), "y": r1(base), "r": 2.2, "fill": "giay" if open_ else c,
                                  "a": 255, "edge": c, "wd": 0.8})
                if lbl:
                    prims.append({"t": "rect", "x": r1((xa + xb) / 2 - tw(lbl) / 2 - 1), "y": r1(yb - th() / 2),
                                  "w": r1(tw(lbl) + 2), "h": r1(th()), "fill": "giay", "a": 255})
                    prims.append(txt((xa + xb) / 2, yb, lbl, LABEL, c))
            elif it[0] == "point":
                _, v, c, lbl, open_ = it
                prims.append({"t": "circle", "x": r1(xof(v)), "y": r1(base), "r": 2.4, "fill": "giay" if open_ else c,
                              "a": 255, "edge": c, "wd": 0.8})
                if lbl:
                    prims.append(txt(xof(v), base - 4, lbl, LABEL, c, "midbottom"))
            else:
                _, vals, c, lbl = it
                for i, v in enumerate(vals):
                    prims.append({"t": "circle", "x": r1(xof(v)), "y": r1(base), "r": 1.6 if i else 2.0, "fill": c,
                                  "a": 255})
                if lbl:
                    prims.append(txt(xof(vals[0]), base - 4, lbl, LABEL, c, "midbottom"))
        return w, h, prims


# ------------------------------------------------------------------ flow
class Flow(Layout):
    SETTINGS = ()
    COMMANDS = ("box", "link")
    LIMIT = 18
    BOX_H = 16
    ROW_GAP = 14

    def build(self):
        boxes: list[dict] = []
        pending = ""
        for cmd, toks, line in self.commands:
            a = self.args(cmd, toks)
            try:
                a.need(0)
                if cmd == "box":
                    boxes.append({"s": a.label(True), "c": a.colour, "link": pending})
                    pending = ""
                else:
                    if not boxes:
                        raise FigureError("link goes between two boxes: write it after the first box")
                    pending = a.label(True)
            except FigureError as e:
                raise FigureError(f"{line!r}: {e}") from None
        if pending:
            raise FigureError("the last link has no box after it")
        if not 2 <= len(boxes) <= 9:
            raise FigureError("a flow needs 2 to 9 boxes")
        maxw = self.size[0] if self.size else MAX_W
        for b in boxes:
            b["w"] = tw(b["s"]) + 10
            b["gap"] = max(18.0, tw(b["link"], SMALL) + 8) if b["link"] else 18.0
        rows: list[list[dict]] = [[]]
        x = 0.0
        for b in boxes:
            need = (b["gap"] if rows[-1] else 0) + b["w"]
            if rows[-1] and x + need > maxw:
                rows.append([])
                x = 0.0
                need = b["w"]
            if b["w"] > maxw:
                raise FigureError(f"the box {b['s']!r} is wider than the figure")
            rows[-1].append(b)
            x += need
        if len(rows) > 3:
            raise FigureError("the flow needs more than three rows: fewer or shorter boxes")
        label_h = th(SMALL) + 1
        row_h = label_h + self.BOX_H
        prims: list[dict] = []
        width = 0.0
        prev = None
        for r, row in enumerate(rows):
            y = r * (row_h + self.ROW_GAP) + label_h
            x = 0.0
            for i, b in enumerate(row):
                if i:
                    x += b["gap"]
                b["x"], b["y"] = x, y
                colour = b["c"] or "muc"
                prims.append({"t": "rect", "x": r1(x), "y": r1(y), "w": r1(b["w"]), "h": self.BOX_H,
                              "fill": b["c"] or "giay", "a": 60 if b["c"] else 255, "edge": colour, "r": 3})
                prims.append(txt(x + b["w"] / 2, y + self.BOX_H / 2, b["s"], LABEL, "muc"))
                if prev is not None:
                    if i:      # same row: a straight arrow, its label above it
                        xa, xb = prev["x"] + prev["w"], x
                        prims.append({"t": "arrow", "x1": r1(xa + 1), "y1": r1(y + self.BOX_H / 2), "x2": r1(xb - 1.5),
                                      "y2": r1(y + self.BOX_H / 2), "c": "muc", "wd": 0.9, "head": 3.5})
                        if b["link"]:
                            prims.append(txt((xa + xb) / 2, y + self.BOX_H / 2 - 2.5, b["link"], SMALL, "do",
                                             "midbottom"))
                    else:      # a new row: down from the last box, back to the left, into this one
                        sx = prev["x"] + prev["w"] / 2
                        sy = prev["y"] + self.BOX_H
                        mid = sy + (self.ROW_GAP + label_h) / 2
                        ex = x + b["w"] / 2
                        prims.append({"t": "polyline", "pts": [[r1(sx), r1(sy)], [r1(sx), r1(mid)], [r1(ex), r1(mid)]],
                                      "c": "muc", "wd": 0.9})
                        prims.append({"t": "arrow", "x1": r1(ex), "y1": r1(mid), "x2": r1(ex), "y2": r1(y - 1.5),
                                      "c": "muc", "wd": 0.9, "head": 3.5})
                        if b["link"]:
                            prims.append(txt((sx + ex) / 2, mid - 1.5, b["link"], SMALL, "do", "midbottom"))
                x += b["w"]
                prev = b
            width = max(width, x)
        h = len(rows) * row_h + (len(rows) - 1) * self.ROW_GAP
        return width, h, prims


LAYOUTS = {"plane": Plane, "bars": Bars, "graph": Graph, "sets": Sets, "map": Map, "grid": Grid,
           "numberline": NumberLine, "flow": Flow}


def prim_box(p: dict) -> tuple[float, float, float, float]:
    """(x0, y0, x1, y1) a primitive covers, estimated (text) or exact (shapes)."""
    t = p["t"]
    if t == "text":
        return text_box(p)
    if t in ("line", "arrow"):
        return min(p["x1"], p["x2"]), min(p["y1"], p["y2"]), max(p["x1"], p["x2"]), max(p["y1"], p["y2"])
    if t in ("polyline", "poly"):
        xs, ys = [q[0] for q in p["pts"]], [q[1] for q in p["pts"]]
        return min(xs), min(ys), max(xs), max(ys)
    if t == "rect":
        return p["x"], p["y"], p["x"] + p["w"], p["y"] + p["h"]
    if t == "circle":
        return p["x"] - p["r"], p["y"] - p["r"], p["x"] + p["r"], p["y"] + p["r"]
    if t == "spans":
        xs = [v for row in p["rows"] for v in row] or [0]
        return min(xs), p["y"], max(xs), p["y"] + p["dy"] * len(p["rows"])
    raise FigureError(f"unknown primitive {t}")


def figure_problems(fig: dict) -> list[str]:
    """Primitives that leave the figure's own box (the parser should never make one)."""
    out = []
    for p in fig["prims"]:
        x0, y0, x1, y1 = prim_box(p)
        slack = 6.5 if p["t"] == "arrow" else 1.0      # an axis arrow head may poke out a little
        if x0 < -slack or y0 < -slack or x1 > fig["w"] + slack or y1 > fig["h"] + slack:
            what = repr(p["s"]) if p["t"] == "text" else p["t"]
            out.append(f"the {what} leaves the figure ({x0:.0f},{y0:.0f})-({x1:.0f},{y1:.0f}) "
                       f"of {fig['w']:g} x {fig['h']:g}")
    return out
