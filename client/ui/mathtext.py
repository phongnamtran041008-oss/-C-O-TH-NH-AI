"""Maths that reads like maths: `pretty(text)` turns the ASCII notation the question bank is
written in (x^2, a_ij, sqrt(x), <=, ->, pi ...) into what a textbook shows.

The result is the same string with two kinds of change:

  * real symbols in place of ASCII operators, only with glyphs one of the two shipped fonts
    really has (VT323 or the Noto subset; tests/test_mathtext.py checks every one):
        <=  ->  ≤        >=  ->  ≥        !=  ->  ≠        ->  ->  →        +-  ->  ±
        sqrt(x) / căn(x)  ->  √x, √(x + 1)        pi  ->  π      mu  ->  μ      Delta  ->  Δ
        2*x  ->  2·x                                a . b (a spaced dot)  ->  a · b
  * superscript and subscript runs wrapped in private-use marker characters:
        SUP + "2" + END        SUB + "ij" + END
    `client/engine/text.Fonts` draws a marked run at about 70% size, raised or lowered, and
    never breaks a line inside it, so every caller of `ui.text` just passes `pretty(s)`. The
    fonts lack most Unicode superscript glyphs (no ⁵-⁹, ⁿ, ᵀ, no subscripts), so the game
    does not rely on them.

The rules are conservative - when in doubt the text is left as it is:
  * x^2, x^(n-1), e^(2x), A^T, R^n, 2^10, (AB)^T: a caret right after a letter, digit or
    closing bracket, followed by a number, one letter, a Greek name or a bracket group. A
    lone caret, or one followed by anything else, stays.
  * a_ij, x_1, u_n, x_tb, x_(n+1), C_n^k, log_2(8), [x]_B: an underscore after ONE letter (or
    a Greek name, or "log", or "]") that is not part of a longer word, followed by up to three
    letters with an optional digit, a number, or a short bracket group. snake_case words
    (so_luong, max_len, ids) never match: their part before the underscore is a whole word.
  * => and <=> stay (the fonts have no ⇒ / ⇔), <- and <-> stay (no ←), ~ stays (it means
    both "about" and "is distributed as"), sigma / lambda / epsilon stay words (no glyph).
  * text that looks like program code (def, print(, ==, **, return, import) is left alone.
Nothing here is applied to what the player types, or to programming exercises."""
from __future__ import annotations

import re

SUP = ""          # the start of a superscript run
SUB = ""          # the start of a subscript run
END = ""          # the end of either
MARKERS = SUP + SUB + END

# every character pretty() may put into a string (besides what was already there)
SYMBOLS = "≤≥≠→±√π·μΔ²³"

GREEK_KEEP = ("lambda", "sigma", "epsilon", "theta", "alpha", "beta", "gamma", "delta", "rho", "chi", "phi",
              "omega", "tau", "eta", "nu", "xi", "Sigma", "Phi")
GREEK_GLYPH = {"mu": "μ", "Delta": "Δ", "pi": "π"}

_CODE = re.compile(r"\bdef |\bprint\(|==|\*\*|\breturn\b|\bimport\b|lambda \w+:")
_LETTER = "A-Za-zÀ-ÖØ-öø-ỹĐđ"          # Latin letters, Vietnamese ones included
_W = rf"[{_LETTER}0-9_]"
_GREEK_NAMES = "|".join(GREEK_KEEP)


def _word(name: str) -> re.Pattern:
    return re.compile(rf"(?<![{_LETTER}_]){name}(?![{_LETTER}])")


_GREEK_SUBS = [(_word(k), v) for k, v in GREEK_GLYPH.items()]
# sqrt(...) and căn(...) (the Vietnamese name, only when written as a function)
_SQRT = re.compile(rf"(?<![{_LETTER}_])(?:sqrt|căn)\(")
# a spaced dot between two operands is a multiplication: 0.5 . 10^s, u . v
_DOT = re.compile(r"(?<=[\w)\]|!'²³]) \. (?=[\w(\[|√-])")
# 2*x, 3*0, 2*(1): a star with no spaces after a digit (a * b with spaces is an operation of its own)
_STAR = re.compile(r"(?<=\d)\*(?=[A-Za-z0-9(])")


def looks_like_code(text: str) -> bool:
    return bool(_CODE.search(text))


def _group(text: str, i: int, limit: int) -> int:
    """The index just past the bracket group opening at text[i] == "(", or -1 when it does not
    close within `limit` characters (or nests more than twice)."""
    depth = 0
    for j in range(i, min(len(text), i + limit + 2)):
        c = text[j]
        if c == "(":
            depth += 1
            if depth > 2:
                return -1
        elif c == ")":
            depth -= 1
            if depth == 0:
                return j + 1
    return -1


def _sqrt(text: str) -> str:
    out, k = [], 0
    for m in _SQRT.finditer(text):
        if m.start() < k:
            continue
        open_at = m.end() - 1
        end = _group(text, open_at, 60)
        if end < 0:
            continue
        inner = text[open_at + 1:end - 1]
        out.append(text[k:m.start()])
        # √n, √2, √0.36: one token needs no bracket; anything longer keeps it
        out.append("√" + inner if re.fullmatch(r"[A-Za-z0-9.]+", inner) and inner.count(".") <= 1
                   else "√(" + inner + ")")
        k = end
    out.append(text[k:])
    return "".join(out)


def _inner_script(inner: str) -> str | None:
    """The content of a script run written in brackets, with a nested ^2 / ^3 as ²/³; None
    when it holds anything the run cannot show (another caret, an underscore)."""
    inner = re.sub(r"\^([23])(?![0-9])", lambda m: "²" if m.group(1) == "2" else "³", inner)
    if "^" in inner or "_" in inner or any(c in MARKERS for c in inner):
        return None
    return inner


_SUP_TOKEN = re.compile(rf"-?(?:\d+(?:\.\d+)?(?![0-9])|(?:{_GREEK_NAMES}|[A-Za-zμπΔ])(?![{_LETTER}0-9_(]))")
_SUB_BASE = re.compile(rf"(?:(?<![{_LETTER}_])(?:[{_LETTER}μΔπ]|{_GREEK_NAMES}|log)|[])])_")
_SUB_TOKEN = re.compile(rf"(?:\d{{1,3}}(?![0-9_])|[A-Za-z]{{1,3}}\d{{0,2}}(?![{_LETTER}0-9_]))")


def _subscripts(text: str) -> str:
    out, k = [], 0
    for m in _SUB_BASE.finditer(text):
        at = m.end()                      # just past the underscore
        if m.start() < k:
            continue
        if at < len(text) and text[at] == "(":
            end = _group(text, at, 12)
            inner = _inner_script(text[at + 1:end - 1]) if end > 0 else None
            if inner is None or not inner.strip():
                continue
            out += [text[k:at - 1], SUB, inner, END]
            k = end
            continue
        t = _SUB_TOKEN.match(text, at)
        if not t:
            continue
        out += [text[k:at - 1], SUB, t.group(0), END]
        k = t.end()
    out.append(text[k:])
    return "".join(out)


def _superscripts(text: str) -> str:
    out, k = [], 0
    for i, c in enumerate(text):
        if c != "^" or i < k or i == 0:
            continue
        before = text[i - 1]
        if not (before.isalnum() or before in ")]|'" + END + "πμΔ²³"):
            continue
        at = i + 1
        if at < len(text) and text[at] == "(":
            end = _group(text, at, 24)
            inner = _inner_script(text[at + 1:end - 1]) if end > 0 else None
            if inner is None or not inner.strip():
                continue
            out += [text[k:i], SUP, inner, END]
            k = end
            continue
        t = _SUP_TOKEN.match(text, at)
        if not t:
            continue
        out += [text[k:i], SUP, t.group(0), END]
        k = t.end()
    out.append(text[k:])
    return "".join(out)


def _operators(text: str) -> str:
    # protect what has no glyph and contains a pattern below: <=> and <-> (no ⇔ / ↔ in the fonts)
    keep = {"<=>": "", "<->": "", "=>": "", "<-": ""}
    for a, b in keep.items():
        text = text.replace(a, b)
    for a, b in (("<=", "≤"), (">=", "≥"), ("!=", "≠"), ("->", "→"), ("+-", "±")):
        text = text.replace(a, b)
    for a, b in keep.items():
        text = text.replace(b, a)
    return text


def pretty(text: str) -> str:
    """`text` with maths notation made readable (see the module doc). Idempotent."""
    if not text or not isinstance(text, str) or looks_like_code(text) or any(c in MARKERS for c in text):
        return text
    if not any(c in text for c in "^_<>!-+*.") and not re.search("pi|mu|Delta|sqrt|căn\\(", text):
        return text
    s = _operators(text)
    s = _sqrt(s)
    for pat, glyph in _GREEK_SUBS:
        s = pat.sub(glyph, s)
    s = _STAR.sub("·", s)
    s = _DOT.sub(" · ", s)
    s = _subscripts(s)
    s = _superscripts(s)
    return s


def plain(text: str) -> str:
    """The text without its markers (what a reader would copy)."""
    return "".join(c for c in text if c not in MARKERS)


def split_runs(text: str) -> list[tuple[str, str]]:
    """[(style, chunk)] with style "n" (normal), "sup" or "sub"; an unclosed run (a string cut
    by a caller) ends with the text."""
    runs: list[tuple[str, str]] = []
    style, cur = "n", ""
    for c in text:
        if c in (SUP, SUB, END):
            if cur:
                runs.append((style, cur))
            cur = ""
            style = "sup" if c == SUP else "sub" if c == SUB else "n"
        else:
            cur += c
    if cur:
        runs.append((style, cur))
    return runs
