#!/usr/bin/env python3
"""Recompute the answer of every generated math question with sympy.

A generator (server/app/learning/math_gen) does its own arithmetic to build the answer.
Here the answer is worked out a second time from the numbers that were drawn
(`Draw.params`), with sympy and by a different route where there is one (sets, complex
numbers and matrices as sympy objects, equations solved instead of rearranged by hand).
A generator whose two answers ever differ has a bug.

    python tools/math_verify.py            # 200 draws of every generator

Needs sympy (server/requirements-dev.txt). tools/check_all.py runs the same check.
"""
from __future__ import annotations

import json
import random
import sys
from fractions import Fraction
from pathlib import Path

import sympy as sp
from sympy import FiniteSet, I, Matrix, Symbol

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "server") not in sys.path:
    sys.path.insert(0, str(ROOT / "server"))

from app.learning import math_items  # noqa: E402

DRAWS = 200
x, y = Symbol("x", real=True), Symbol("y", real=True)
z = Symbol("z")


def frac(v) -> Fraction:
    v = sp.nsimplify(sp.simplify(v))
    if not v.is_rational:
        raise ValueError(f"{v} is not a rational number")
    return Fraction(int(v.p), int(v.q))


def cplx(pair) -> sp.Expr:
    return sp.Integer(pair[0]) + sp.Integer(pair[1]) * I


def re_im(v) -> list[Fraction]:
    v = sp.expand(sp.simplify(v))
    return [frac(sp.re(v)), frac(sp.im(v))]


def flat(m: Matrix) -> list[Fraction]:
    return [frac(v) for v in m.T]          # (iterating a Matrix goes row by row; .T twice would too)


def by_rows(m: Matrix) -> list[Fraction]:
    return [frac(m[r, c]) for r in range(m.rows) for c in range(m.cols)]


def _function(p: dict) -> sp.Expr:
    kind = p["kind"]
    if kind == "linear":
        return p["a"] * x + p["c"]
    return {"square": x ** 2, "cube": x ** 3, "abs": sp.Abs(x)}[kind] + p["c"]


def _injective(p: dict) -> bool:
    """No two points of a grid share an image (enough to tell these four families apart)."""
    f = _function(p)
    grid = [sp.Rational(k, 2) for k in range(-20, 21)]
    images = [f.subs(x, v) for v in grid]
    return len(set(images)) == len(images)


def _square_root(p: dict) -> list[Fraction]:
    w = cplx(p["w"])
    sols = sp.solve([sp.Eq(x ** 2 - y ** 2, sp.re(w)), sp.Eq(2 * x * y, sp.im(w))], [x, y], dict=True)
    sol = next(s for s in sols if s[x] > 0)
    return [frac(sol[x]), frac(sol[y])]


def _symmetric_unknowns(p: dict) -> list[Fraction]:
    m = Matrix([[{"x": x, "y": y}.get(v, v) for v in row] for row in p["rows"]])
    sol = sp.solve(list(m - m.T), [x, y], dict=True)[0]
    return [frac(sol[x]), frac(sol[y])]


# generator id -> the answer worked out from the drawn numbers: a bool for true_false,
# a list of Fractions for numeric (in the order the question asks for; a set is compared sorted)
EXPECTED = {
    # ---- floor 1
    "dstt_g1_thuoc": lambda p: sp.Integer(p["k"]) in FiniteSet(*p["elements"]),
    "dstt_g1_so_tap_con": lambda p: [Fraction(len(FiniteSet(*p["elements"]).powerset()))],
    "dstt_g1_giao": lambda p: [frac(v) for v in FiniteSet(*p["a"]) & FiniteSet(*p["b"])],
    "dstt_g1_hop_dem": lambda p: [Fraction(len(FiniteSet(*p["a"]) | FiniteSet(*p["b"])))],
    "dstt_g1_hieu": lambda p: [frac(v) for v in FiniteSet(*p["a"]) - FiniteSet(*p["b"])],
    "dstt_g1_tich_dem": lambda p: [Fraction(len(list(
        FiniteSet(*p["a"]) * FiniteSet(*[Symbol(s) for s in p["b"]]))))],
    "dstt_g1_tich_nguoc": lambda p: [frac(sp.solve(sp.Eq(p["a_size"] * x, p["pairs"]), x)[0])],
    "dstt_g1_anh_bac_nhat": lambda p: [frac((p["a"] * x + p["b"]).subs(x, p["x"]))],
    "dstt_g1_anh_tap": lambda p: [frac(v) for v in sp.imageset(sp.Lambda(x, x ** 2 + p["c"]),
                                                               FiniteSet(*p["domain"]))],
    "dstt_g1_don_anh": _injective,
    "dstt_g1_dem_don_anh": lambda p: [frac(sp.ff(p["n"], p["m"]))],
    "dstt_g1_hop_thanh": lambda p: [frac((p["g"][0] * x + p["g"][1]).subs(
        x, (p["f"][0] * x + p["f"][1]).subs(x, p["x"])))],
    "dstt_g1_nguoc": lambda p: [frac(sp.solve(sp.Eq(p["a"] * x + p["b"], p["y"]), x)[0])],
    # ---- floor 2
    "dstt_g2_phan_thuc_ao": lambda p: [frac((sp.re if p["part"] == "re" else sp.im)(cplx([p["re"], p["im"]])))],
    "dstt_g2_luy_thua_i": lambda p: re_im(I ** p["n"]),
    "dstt_g2_cong_tru": lambda p: re_im(cplx(p["z"]) + cplx(p["w"]) if p["op"] == "+"
                                        else cplx(p["z"]) - cplx(p["w"])),
    "dstt_g2_nhan": lambda p: re_im(cplx(p["z"]) * cplx(p["w"])),
    "dstt_g2_modun": lambda p: [frac(sp.Abs(cplx([p["re"], p["im"]])))],
    "dstt_g2_lien_hop": lambda p: [frac(sp.expand(
        cplx([p["re"], p["im"]]) * sp.conjugate(cplx([p["re"], p["im"]])) if p["kind"] == "product"
        else cplx([p["re"], p["im"]]) + sp.conjugate(cplx([p["re"], p["im"]]))))],
    "dstt_g2_chia_i": lambda p: re_im(cplx(p["z"]) / I),
    "dstt_g2_chia": lambda p: re_im(cplx(p["z"]) / cplx(p["w"])),
    "dstt_g2_acgumen": lambda p: [frac(sp.Mod(sp.arg(cplx([p["re"], p["im"]])) * 180 / sp.pi, 360))],
    "dstt_g2_moivre": lambda p: re_im(sp.expand(cplx(p["base"]) ** p["n"])),
    "dstt_g2_so_nghiem": lambda p: [Fraction(len({(round(float(sp.re(r)), 8), round(float(sp.im(r)), 8))
                                                  for r in sp.Poly(z ** p["n"] - cplx(p["c"]), z).nroots()}))],
    "dstt_g2_can_bac_hai": _square_root,
    # ---- floor 3
    "dstt_g3_to_hop_vecto": lambda p: flat(p["a"] * Matrix(p["u"]) + p["b"] * Matrix(p["v"])),
    "dstt_g3_vecto_an": lambda p: flat((Matrix(p["v"]) - Matrix(p["u"])) / p["a"]),
    "dstt_g3_phan_tu": lambda p: [frac(Matrix(p["rows"])[p["i"] - 1, p["j"] - 1])],
    "dstt_g3_cong_thuc_hang": lambda p: [frac(sum(Matrix(
        p["m"], p["n"], lambda i, j: p["p"] * (i + 1) + p["q"] * (j + 1)).row(p["row"] - 1)))],
    "dstt_g3_cong_ma_tran": lambda p: by_rows(Matrix(p["a"]) + Matrix(p["b"]) if p["op"] == "+"
                                              else Matrix(p["a"]) - Matrix(p["b"])),
    "dstt_g3_to_hop_ma_tran": lambda p: [frac((p["p"] * Matrix(p["a"]) + p["q"] * Matrix(p["b"]))[
        p["i"] - 1, p["j"] - 1])],
    "dstt_g3_chuyen_vi_phan_tu": lambda p: [frac(Matrix(p["rows"]).T[p["i"] - 1, p["j"] - 1])],
    "dstt_g3_chuyen_vi_tong": lambda p: by_rows(Matrix(p["a"]).T + Matrix(p["b"]) if p["op"] == "+"
                                                else Matrix(p["a"]).T - Matrix(p["b"])),
    "dstt_g3_vet": lambda p: [frac(Matrix(p["rows"]).trace())],
    "dstt_g3_vet_to_hop": lambda p: [frac((p["p"] * Matrix(p["a"]) + p["q"] * Matrix(p["b"])).trace())],
    "dstt_g3_dac_biet": lambda p: {"symmetric": Matrix(p["rows"]).is_symmetric(),
                                   "upper": Matrix(p["rows"]).is_upper,
                                   "diagonal": Matrix(p["rows"]).is_diagonal()}[p["kind"]],
    "dstt_g3_doi_xung_dien": _symmetric_unknowns,
}


# M11: the recomputations of the other floors and subjects live in modules of their own,
# tools/math_verify_<prefix>[_t<first floor>].py, each with an EXPECTED dict; all are merged here
for _module in sorted(p.stem for p in (ROOT / "tools").glob("math_verify_*.py")):
    import importlib
    if str(ROOT / "tools") not in sys.path:
        sys.path.insert(0, str(ROOT / "tools"))
    _more = importlib.import_module(_module).EXPECTED
    _clash = set(_more) & set(EXPECTED)
    if _clash:
        raise ValueError(f"tools/{_module}.py: {sorted(_clash)} already has a recomputation")
    EXPECTED.update(_more)


def mismatch(item: math_items.MathItem) -> str | None:
    """Why this draw's answer is not what sympy gets from its numbers, or None."""
    if item.qtype not in ("true_false", "numeric"):
        # (multiple_choice, matching, ordering, find_mistake and tribulation are hand-written only
        # so far - math_items rejects a generator of the last four; a generator of one of them
        # needs its own comparison here before it can be trusted)
        return (f"is a {item.qtype} generator, which tools/math_verify.py cannot check yet (only "
                f"true_false and numeric generators can be verified)")
    fn = EXPECTED.get(item.id)
    if fn is None:
        return "has no recomputation in tools/math_verify.py"
    try:
        want = fn(json.loads(item.numbers))
    except Exception as e:                                   # noqa: BLE001  (any failure is a finding)
        return f"with {item.numbers}: the recomputation failed ({type(e).__name__}: {e})"
    if item.qtype == "true_false":
        ok, got = bool(want) == item.answer, item.answer
    else:
        got = math_items.parse_numbers(item.answer)
        ok = (sorted(got) == sorted(want)) if item.unordered else (got == list(want))
    if ok:
        return None
    shown = want if isinstance(want, bool) else ", ".join(math_items.number_text(v) for v in want)
    return f"with {item.numbers}: the generator answers {item.answer!r} but sympy gets {shown!r}"


def verify_all(draws: int = DRAWS) -> list[str]:
    errors = []
    for spec in math_items.generators().values():
        for seed in range(draws):
            problem = mismatch(math_items.draw(spec, random.Random(seed)))
            if problem:
                errors.append(f"{spec.id} {problem}")
                break                                       # one line per generator is enough
    return errors


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    problems = verify_all()
    for line in problems:
        print(" -", line)
    print(f"{len(math_items.generators())} generators x {DRAWS} draws: "
          f"{'all answers confirmed' if not problems else f'{len(problems)} with a wrong answer'}")
    sys.exit(1 if problems else 0)
