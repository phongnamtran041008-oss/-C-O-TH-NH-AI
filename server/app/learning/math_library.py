"""Tàng Thư Các of the math game: the documents a player reads next to the questions.

One document per floor, at data/math/library/<subject>/<file>.md: a small Markdown file
with front matter, split into one `##` section per micro-skill of that floor. The server
parses it into blocks and the client draws them; nothing is rendered as raw Markdown.

    ---
    id: dstt_t1_tap_hop_anh_xa
    title_vi: Tập hợp và ánh xạ
    subject: dai_so_tuyen_tinh
    floor: 1
    skills: [dstt_t1_tap_hop, dstt_t1_phep_toan_tap_hop]
    ---
    ## Tập hợp và phần tử            <- the first skill of `skills`
    Một tập hợp là ...                <- paragraph
    $$ A \\cap B = \\{x : x \\in A\\} $$   <- a formula: a picture built before release
    :::matrix                         <- a matrix figure the game draws itself
    A = 1 2 ; 3 -4
    :::
    - gạch đầu dòng                   <- bullets
    1. bước giải                      <- numbered steps
    > Lỗi thường gặp: ...             <- a note from Trúc Lão

Text is Vietnamese and ASCII-safe outside formulas (A^T, !=), like every other string of
the game. A formula is TeX, written in ASCII only; `tools/build_formulas.py` turns each
one into a PNG that ships with the game, and `alt` here is the plain-text fallback shown
when that picture is missing.

Pure data and rules: no database, no pygame. `validate_all()` returns one readable line
per problem, and tools/check_all.py fails the build when that list is not empty.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from . import math_path
from .math_items import MATRIX_ENTRY_RE, MATRIX_NAME_RE, MAX_MATRICES, MAX_MATRIX_SIDE
from .math_path import MATH_DIR, text_problem

LIBRARY_DIR = MATH_DIR / "library"
MANIFEST = MATH_DIR / "formulas.json"
KEY_LEN = 16
MAX_FORMULA_WIDTH = 380.0        # base units: the widest a picture may be in the reader
MAX_FORMULA_HEIGHT = 90.0
FRONT_KEYS = {"id", "title_vi", "subject", "floor", "skills", "summary_vi"}
BLOCK_TYPES = ("section", "heading", "text", "bullets", "steps", "formula", "matrices", "note")


# ------------------------------------------------------------------ TeX in plain text
# What every TeX command in the documents looks like when the picture cannot be shown.
SYMBOLS = {
    r"\cap": "giao", r"\cup": "hop", r"\setminus": "\\", r"\in": "thuoc", r"\notin": "khong thuoc",
    r"\subset": "con cua", r"\subseteq": "con cua", r"\varnothing": "{}", r"\emptyset": "{}",
    r"\times": "x", r"\cdot": ".", r"\neq": "!=", r"\ne": "!=", r"\pm": "+-",
    r"\le": "<=", r"\leq": "<=", r"\ge": ">=", r"\geq": ">=", r"\lt": "<", r"\gt": ">",
    r"\approx": "xap xi", r"\equiv": "=", r"\lor": "hoac", r"\land": "va",
    r"\to": "->", r"\mapsto": "->", r"\Rightarrow": "=>", r"\implies": "=>",
    r"\Leftrightarrow": "<=>", r"\iff": "<=>",
    r"\ldots": "...", r"\dots": "...", r"\cdots": "...", r"\vdots": "...", r"\ddots": "...",
    r"\mathbb{R}": "R", r"\mathbb{C}": "C", r"\mathbb{N}": "N", r"\mathbb{Z}": "Z", r"\mathbb{Q}": "Q",
    r"\forall": "voi moi", r"\exists": "ton tai", r"\mid": "|", r"\circ": "o",
    r"\alpha": "alpha", r"\beta": "beta", r"\lambda": "lambda", r"\theta": "theta", r"\varphi": "phi",
    r"\Omega": "Omega",                                              # (M11 xác suất: the sample space)
    r"\sum": "tong", r"\prod": "tich", r"\infty": "vo cung", r"\deg": "deg", r"\sin": "sin",
    r"\cos": "cos", r"\tan": "tan", r"\ln": "ln", r"\log": "log", r"\exp": "exp",
    r"\overline": "", r"\bar": "", r"\vec": "", r"\hat": "",
    r"\neg": "khong", r"\lceil": "tran(", r"\rceil": ")",
    r"\lim": "lim", r"\sim": "~", r"\pi": "pi", r"\arcsin": "arcsin",       # (M11 giải tích)
    r"\arccos": "arccos", r"\arctan": "arctan", r"\varepsilon": "epsilon",
    r"\max": "max",                                                          # (M11 giải tích tầng 4-6)
    r"\mu": "mu", r"\sigma": "sigma", r"\Phi": "Phi", r"\int": "tich phan",   # (M11 xác suất tầng 4-6)
    r"\|": "||", r"\Sigma": "Sigma",                                         # (M11 đại số tuyến tính tầng 7-9)
    r"\partial": "d", r"\nabla": "grad",                                     # (M11 giải tích tầng 7-9)
    r"\min": "min", r"\eta": "eta",                                          # (M11 tối ưu tầng 7-9)
    r"\rho": "rho",                                                         # (floor 10 xác suất: hệ số tương quan)
}
# Dropped: they only change spacing or size.
IGNORED = (r"\left", r"\right", r"\displaystyle", r"\limits", r"\,", r"\;", r"\!", r"\:",
           r"\quad", r"\qquad", r"\ ", r"\big", r"\Big", r"\bigg", r"\Bigg")
MATRIX_ENV = re.compile(r"\\begin\{([pbv]?matrix)\}(.*?)\\end\{\1\}", re.S)
COMMAND = re.compile(r"\\[a-zA-Z]+|\\.")
SIMPLE = re.compile(r"^[A-Za-z0-9.]+$")     # a part that needs no brackets around it in a/b


class TexError(ValueError):
    """A formula that cannot be written in plain text, so it has no fallback."""


def _braced(text: str, start: int) -> tuple[str, int]:
    """The {...} group that starts at `start`, and the index just after it."""
    if start >= len(text) or text[start] != "{":
        raise TexError(f"expected {{ at position {start}")
    depth, i = 0, start
    while i < len(text):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[start + 1:i], i + 1
        i += 1
    raise TexError("a { is never closed")


def _args(text: str, i: int, n: int) -> tuple[list[str], int]:
    out = []
    for _ in range(n):
        while i < len(text) and text[i] == " ":
            i += 1
        arg, i = _braced(text, i)
        out.append(arg)
    return out, i


def tex_to_ascii(tex: str) -> str:
    """The formula written the way the rest of the game writes math: (a + b)/2, A^T, [1, 2; 3, 4].

    Raises TexError for anything with no plain-text form, so a formula never ships with a
    fallback nobody can read."""
    plain = _to_ascii(tex)
    problem = text_problem(plain)
    if problem:
        raise TexError(f"its plain-text form {problem}")
    return plain


def _wrap(part: str) -> str:
    """A part of a fraction, with brackets only where they are needed: 1/2, (a+b)/2."""
    return part if SIMPLE.match(part) else f"({part})"


def _to_ascii(tex: str) -> str:
    def matrix(m: re.Match) -> str:
        rows = [r.strip() for r in m.group(2).split(r"\\") if r.strip()]
        return "[" + "; ".join(", ".join(_to_ascii(c) for c in row.split("&")) for row in rows) + "]"

    text = MATRIX_ENV.sub(matrix, tex)
    for junk in IGNORED:
        text = text.replace(junk, " ")
    out, i = [], 0
    while i < len(text):
        ch = text[i]
        if ch == "\\":
            m = COMMAND.match(text, i)
            if not m:
                raise TexError("a stray \\")
            cmd = m.group(0)
            i = m.end()
            if cmd in (r"\frac", r"\dfrac", r"\tfrac"):
                (num, den), i = _args(text, i, 2)
                out.append(f"{_wrap(_to_ascii(num))}/{_wrap(_to_ascii(den))}")
            elif cmd == r"\sqrt":
                (arg,), i = _args(text, i, 1)
                out.append(f"can({_to_ascii(arg)})")
            elif cmd in (r"\text", r"\mathrm", r"\operatorname"):
                (arg,), i = _args(text, i, 1)
                out.append(arg)
            elif cmd in (r"\{", r"\}", r"\%", r"\&", r"\_", r"\#", r"\$"):
                out.append(cmd[1])
            elif text[i:i + 1] == "{" and cmd + text[i:i + 3] in SYMBOLS:   # \mathbb{R}
                out.append(SYMBOLS[cmd + text[i:i + 3]])
                i += 3
            elif cmd in SYMBOLS:
                out.append(SYMBOLS[cmd])
            else:
                raise TexError(f"{cmd} has no plain-text form (add it to math_library.SYMBOLS)")
        elif ch in "^_":
            i += 1
            while i < len(text) and text[i] == " ":
                i += 1
            if i < len(text) and text[i] == "{":
                arg, i = _braced(text, i)
                inner = _to_ascii(arg)
                out.append(ch + (inner if len(inner) <= 1 else f"({inner})"))
            elif i < len(text):
                out.append(ch + text[i])
                i += 1
        elif ch in "{}":
            i += 1
        elif ch == "&":
            out.append(", ")
            i += 1
        else:
            out.append(ch)
            i += 1
    plain = " ".join("".join(out).split())
    return plain.replace(" ,", ",").replace("( ", "(").replace(" )", ")")


def formula_key(tex: str) -> str:
    """The name of this formula's picture. The same TeX always gives the same name, so the
    pictures of unchanged formulas are never rebuilt."""
    return hashlib.sha1(" ".join(tex.split()).encode()).hexdigest()[:KEY_LEN]


# ------------------------------------------------------------------ documents
@dataclass(frozen=True)
class Document:
    id: str
    title_vi: str
    subject: str
    floor: int
    skills: tuple[str, ...]
    summary_vi: str
    blocks: tuple[dict, ...] = field(default_factory=tuple)

    def view(self, formulas: dict | None = None) -> dict:
        """What the server sends: the blocks, with each formula's size filled in."""
        sizes = load_manifest() if formulas is None else formulas
        blocks = []
        for b in self.blocks:
            if b["type"] == "formula":
                size = sizes.get(b["key"], {})
                b = {**b, "w": size.get("w", 0.0), "h": size.get("h", 0.0)}
            blocks.append(b)
        return {"id": self.id, "title_vi": self.title_vi, "subject": self.subject, "floor": self.floor,
                "skills": list(self.skills), "summary_vi": self.summary_vi, "blocks": blocks}

    @property
    def formulas(self) -> list[dict]:
        return [b for b in self.blocks if b["type"] == "formula"]

    def section_of(self, skill_id: str) -> int:
        """Which block starts the part about this micro-skill (0 when it has none)."""
        for n, b in enumerate(self.blocks):
            if b["type"] == "section" and b.get("skill") == skill_id:
                return n
        return 0


def split_front_matter(text: str) -> tuple[dict, str, list[str]]:
    """({front matter}, body, problems). Values are plain text; [a, b] is a list."""
    lines = text.replace("\r\n", "\n").split("\n")
    if not lines or lines[0].strip() != "---":
        return {}, text, ["the file must start with a --- front matter block"]
    try:
        end = lines.index("---", 1)
    except ValueError:
        return {}, text, ["the front matter is never closed by ---"]
    front: dict = {}
    problems = []
    for n, line in enumerate(lines[1:end], 2):
        if not line.strip():
            continue
        key, sep, value = line.partition(":")
        if not sep:
            problems.append(f"line {n}: front matter needs 'key: value'")
            continue
        key, value = key.strip(), value.strip()
        if value.startswith("[") and value.endswith("]"):
            front[key] = [v.strip() for v in value[1:-1].split(",") if v.strip()]
        elif value.isdigit():
            front[key] = int(value)
        else:
            front[key] = value
    return front, "\n".join(lines[end + 1:]), problems


def parse_blocks(body: str, skills: list[str]) -> tuple[list[dict], list[str]]:
    """The body as blocks the client can draw, plus one line per problem."""
    blocks: list[dict] = []
    problems: list[str] = []
    lines = body.replace("\r\n", "\n").split("\n")
    paragraph: list[str] = []
    bullets: list[str] = []
    steps: list[str] = []
    sections = 0
    i = 0

    def flush() -> None:
        nonlocal paragraph, bullets, steps
        if paragraph:
            blocks.append({"type": "text", "text": " ".join(paragraph)})
            paragraph = []
        if bullets:
            blocks.append({"type": "bullets", "items": bullets})
            bullets = []
        if steps:
            blocks.append({"type": "steps", "items": steps})
            steps = []

    while i < len(lines):
        line = lines[i].rstrip()
        stripped = line.strip()
        i += 1
        if not stripped:
            flush()
        elif stripped.startswith("## "):
            flush()
            skill = skills[sections] if sections < len(skills) else None
            if skill is None:
                problems.append(f"section {sections + 1} ({stripped[3:]}) has no micro-skill in `skills`")
            blocks.append({"type": "section", "title_vi": stripped[3:].strip(), "skill": skill})
            sections += 1
        elif stripped.startswith("### "):
            flush()
            blocks.append({"type": "heading", "title_vi": stripped[4:].strip()})
        elif stripped.startswith("> "):
            flush()
            note = [stripped[2:].strip()]
            while i < len(lines) and lines[i].strip().startswith("> "):
                note.append(lines[i].strip()[2:].strip())
                i += 1
            blocks.append({"type": "note", "text": " ".join(note)})
        elif stripped.startswith("- "):
            if paragraph or steps:
                flush()
            bullets.append(stripped[2:].strip())
        elif re.match(r"^\d+\. ", stripped):
            if paragraph or bullets:
                flush()
            steps.append(stripped.split(". ", 1)[1].strip())
        elif stripped.startswith("$$"):
            flush()
            tex = stripped[2:]
            if tex.endswith("$$"):
                tex = tex[:-2]
            else:
                while i < len(lines) and not lines[i].strip().endswith("$$"):
                    tex += " " + lines[i].strip()
                    i += 1
                if i < len(lines):
                    tex += " " + lines[i].strip()[:-2]
                    i += 1
                else:
                    problems.append("a $$ formula is never closed")
            tex = " ".join(tex.split())
            try:
                alt = tex_to_ascii(tex)
            except TexError as e:
                problems.append(f"formula {tex!r}: {e}")
                alt = ""
            blocks.append({"type": "formula", "key": formula_key(tex), "tex": tex, "alt": alt})
        elif stripped == ":::matrix":
            flush()
            rows: list[str] = []
            while i < len(lines) and lines[i].strip() != ":::":
                rows.append(lines[i].strip())
                i += 1
            if i >= len(lines):
                problems.append("a :::matrix block is never closed by :::")
            i += 1
            matrices, bad = parse_matrices(rows)
            problems += bad
            blocks.append({"type": "matrices", "matrices": matrices})
        elif stripped.startswith(":::"):
            problems.append(f"unknown block {stripped!r}")
            flush()
        else:
            if bullets or steps:
                flush()
            paragraph.append(stripped)
    flush()
    if sections < len(skills):
        problems.append(f"only {sections} sections for {len(skills)} micro-skills in `skills`")
    return blocks, problems


def parse_matrices(rows: list[str]) -> tuple[list[dict], list[str]]:
    """`A = 1 2 ; 3 -4` lines into the matrices the game draws."""
    out, problems = [], []
    for row in rows:
        if not row:
            continue
        name, sep, body = row.partition("=")
        name = name.strip()
        if not sep or not MATRIX_NAME_RE.match(name):
            problems.append(f"matrix line {row!r}: write it as 'A = 1 2 ; 3 4'")
            continue
        cells = [r.split() for r in body.split(";")]
        if not cells or not all(cells) or len({len(r) for r in cells}) != 1:
            problems.append(f"matrix {name}: every row needs the same number of entries")
            continue
        if len(cells) > MAX_MATRIX_SIDE or len(cells[0]) > MAX_MATRIX_SIDE:
            problems.append(f"matrix {name}: at most {MAX_MATRIX_SIDE} rows and columns")
            continue
        bad = [c for r in cells for c in r if not MATRIX_ENTRY_RE.match(c)]
        if bad:
            problems.append(f"matrix {name}: entry {bad[0]!r} must be a number, a fraction a/b "
                            "or one small letter")
            continue
        out.append({"name": name, "rows": cells})
    if not out and not problems:
        problems.append("a :::matrix block has no matrix in it")
    if len(out) > MAX_MATRICES:
        problems.append(f"a :::matrix block shows {len(out)} matrices, at most {MAX_MATRICES}")
    return out, problems


def parse_document(text: str, name: str = "") -> tuple[Document | None, list[str]]:
    front, body, problems = split_front_matter(text)
    if problems:
        return None, problems
    problems += [f"unknown front matter key {k!r}" for k in sorted(front) if k not in FRONT_KEYS]
    skills = front.get("skills") or []
    if not isinstance(skills, list) or not skills:
        problems.append("`skills` must list the micro-skills this document is about")
        skills = []
    blocks, bad = parse_blocks(body, skills)
    problems += bad
    doc = Document(id=str(front.get("id", "")), title_vi=str(front.get("title_vi", "")),
                   subject=str(front.get("subject", "")), floor=front.get("floor", 0),
                   skills=tuple(skills), summary_vi=str(front.get("summary_vi", "")),
                   blocks=tuple(blocks))
    return doc, problems


@lru_cache(maxsize=1)
def load_manifest(path: Path = MANIFEST) -> dict:
    """key -> {tex, alt, w, h}: the size of every formula picture, in base units.
    Written by tools/build_formulas.py; empty when no picture has been built yet."""
    if not path.is_file():
        return {}
    data = json.loads(path.read_text("utf-8"))
    return data.get("formulas", {})


@lru_cache(maxsize=1)
def documents() -> dict[str, Document]:
    """Every document that parses, by id, in reading order (subject, then floor)."""
    out: dict[str, Document] = {}
    for subject in math_path.subjects():
        for path in sorted((LIBRARY_DIR / subject.id).glob("*.md")) if (LIBRARY_DIR / subject.id).is_dir() else []:
            doc, problems = parse_document(path.read_text("utf-8"), path.name)
            if doc is not None and not problems and doc.id:
                out[doc.id] = doc
    return dict(sorted(out.items(), key=lambda kv: (kv[1].subject, kv[1].floor)))


def for_skill(skill_id: str) -> Document | None:
    return next((d for d in documents().values() if skill_id in d.skills), None)


def for_floor(subject_id: str, floor: int) -> list[Document]:
    return [d for d in documents().values() if d.subject == subject_id and d.floor == floor]


# ------------------------------------------------------------------ validation
def validate_document(doc: Document, problems: list[str], subject_id: str, manifest: dict) -> list[str]:
    """Problems in one document, given the problems its parsing already found."""
    errors = list(problems)
    if not math_path.ID_RE.match(doc.id):
        errors.append("id must be 3-40 lowercase letters, digits and _")
    if doc.subject != subject_id:
        errors.append(f"subject is {doc.subject!r} but the file is in the {subject_id} folder")
    for field_name, value in (("title_vi", doc.title_vi), ("summary_vi", doc.summary_vi)):
        problem = text_problem(value)
        if problem:
            errors.append(f"{field_name} {problem}")
    try:
        subject = math_path.subject(subject_id)
        floor = subject.floor(doc.floor)
    except KeyError:
        errors.append(f"floor {doc.floor} is not a floor of {subject_id}")
        return errors
    floor_skills = [s.id for s in floor.skills]
    if list(doc.skills) != floor_skills:
        errors.append(f"`skills` must be every micro-skill of floor {doc.floor} in order: "
                      f"{', '.join(floor_skills)}")
    for n, b in enumerate(doc.blocks, 1):
        where = f"block {n} ({b['type']})"
        if b["type"] not in BLOCK_TYPES:
            errors.append(f"{where}: unknown block type")
            continue
        for key in ("title_vi", "text"):
            if key in b and b[key] is not None:
                problem = text_problem(b[key])
                if problem:
                    errors.append(f"{where}: {key} {problem}")
        for item in b.get("items", []):
            problem = text_problem(item)
            if problem:
                errors.append(f"{where}: an item {problem}")
        if b["type"] == "formula":
            errors += _formula_problems(b, where, manifest)
    if not any(b["type"] == "section" for b in doc.blocks):
        errors.append("has no ## section")
    return errors


def _formula_problems(block: dict, where: str, manifest: dict) -> list[str]:
    errors = []
    tex = block["tex"]
    if not tex.strip():
        errors.append(f"{where}: the formula is empty")
    if not tex.isascii():
        errors.append(f"{where}: a formula must be written in ASCII only (Vietnamese goes in the text)")
    problem = text_problem(block["alt"]) if block["alt"] else "is missing"
    if problem:
        errors.append(f"{where}: its plain-text form {problem}")
    size = manifest.get(block["key"])
    if size is None:
        errors.append(f"{where}: no picture was built for {tex!r} (run python tools/build_formulas.py)")
    else:
        if size.get("tex") != tex:
            errors.append(f"{where}: the picture {block['key']} was built from another formula")
        if not 0 < size.get("w", 0) <= MAX_FORMULA_WIDTH:
            errors.append(f"{where}: the picture is {size.get('w')} wide, at most {MAX_FORMULA_WIDTH} fits "
                          "the reader (make the formula shorter or split it)")
        if not 0 < size.get("h", 0) <= MAX_FORMULA_HEIGHT:
            errors.append(f"{where}: the picture is {size.get('h')} tall, at most {MAX_FORMULA_HEIGHT} fits")
    return errors


def validate_all(library_dir: Path = LIBRARY_DIR, manifest: dict | None = None) -> list[str]:
    """Every problem in the library, each line starting with the file it is in."""
    manifest = load_manifest() if manifest is None else manifest
    errors: list[str] = []
    seen: dict[str, str] = {}
    skills_covered: dict[str, str] = {}
    for subject in math_path.subjects():
        folder = library_dir / subject.id
        for path in sorted(folder.glob("*.md")) if folder.is_dir() else []:
            name = f"math/library/{subject.id}/{path.name}"
            doc, problems = parse_document(path.read_text("utf-8"), path.name)
            if doc is None:
                errors += [f"{name}: {p}" for p in problems]
                continue
            errors += [f"{name}: {e}" for e in validate_document(doc, problems, subject.id, manifest)]
            if doc.id in seen:
                errors.append(f"{name}: id {doc.id} is already used by {seen[doc.id]}")
            seen[doc.id] = name
            for skill in doc.skills:
                if skill in skills_covered:
                    errors.append(f"{name}: {skill} is already explained in {skills_covered[skill]}")
                skills_covered[skill] = name
    for stray in sorted(p.name for p in library_dir.glob("*.md")) if library_dir.is_dir() else []:
        errors.append(f"math/library/{stray}: a document must be in a subject folder")
    errors += _coverage_problems(skills_covered)
    return errors


def _coverage_problems(skills_covered: dict[str, str]) -> list[str]:
    """A floor whose questions are written needs its document, and the other way round."""
    from . import math_items
    errors = []
    for subject in math_path.subjects():
        for floor in subject.floors:
            has_questions = bool(math_items.floor_templates(subject.id, floor.number, allow_unreviewed=True))
            covered = [s.id for s in floor.skills if s.id in skills_covered]
            if has_questions and not covered:
                errors.append(f"math/library/{subject.id}: floor {floor.number} has questions but no document")
            elif covered and len(covered) != len(floor.skills):
                missing = [s.id for s in floor.skills if s.id not in skills_covered]
                errors.append(f"math/library/{subject.id}: floor {floor.number} explains only part of its "
                              f"micro-skills (missing {', '.join(missing)})")
    return errors


def manifest_problems(manifest: dict | None = None, assets_dir: Path | None = None) -> list[str]:
    """Problems between the documents, the manifest and the pictures that ship with the game."""
    manifest = load_manifest() if manifest is None else manifest
    wanted = {b["key"]: b["tex"] for d in documents().values() for b in d.formulas}
    errors = []
    for key, tex in sorted(wanted.items()):
        if key not in manifest:
            errors.append(f"formulas.json: no entry for {tex!r}")
    for key in sorted(set(manifest) - set(wanted)):
        errors.append(f"formulas.json: {key} is not used by any document any more "
                      "(run python tools/build_formulas.py --prune)")
    if assets_dir is not None:
        for key in sorted(wanted):
            png = assets_dir / f"{key}.png"
            if not png.is_file():
                errors.append(f"client/assets/formulas/{key}.png is missing "
                              "(run python tools/build_formulas.py)")
            elif png.stat().st_size < 100:
                errors.append(f"client/assets/formulas/{key}.png is empty")
        for png in sorted(assets_dir.glob("*.png")) if assets_dir.is_dir() else []:
            if png.stem not in wanted:
                errors.append(f"client/assets/formulas/{png.name} belongs to no document any more")
    return errors
