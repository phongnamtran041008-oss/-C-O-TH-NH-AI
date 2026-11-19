"""The sympy recomputation of the generators of Xác Suất và Thống Kê, floors 7-9 (M11 round 2):
generator id -> a function of the drawn numbers (`Draw.params`) giving a bool for a true_false
question, or a list of Fractions for a numeric one. Merged into tools/math_verify.py EXPECTED.
This module must not import math_verify (it is imported by it).

The generators use the closed formulas of the floors. Here every answer is found another way:
- floor 7: the sample variance from the pairwise differences sum_{i<j} (x_i - x_j)^2 / (n(n - 1))
  (never from sum x^2 - n x_tb^2), a frequency table expanded into its raw data first; the
  maximum likelihood estimate by writing ln L with sympy and solving d(ln L)/d(theta) = 0; the
  unbiasedness of a linear estimator with sympy.stats E on two-point variables of mean mu; the
  variance of the sample mean summed term by term, with the Laplace table rebuilt from erf;
- floor 8: a confidence interval by solving |x_tb - mu| = epsilon (or (f - p)^2 = z^2 f(1-f)/n)
  for the unknown, the smallest sample size by a search over n with exact square roots, the
  Chebyshev bound from the variance of a mean summed term by term, the mean and variance of the
  sum of the central limit theorem summed term by term; the critical values given in the prompts (z and Student t) are
  checked against erf and sympy.stats StudentT;
- floor 9: every statistic from the raw numbers with sympy square roots, and the decision by the
  p-value (from erf) instead of the critical value."""
from __future__ import annotations

import itertools
from fractions import Fraction

import sympy as sp
from sympy import Rational
from sympy.stats import E, FiniteRV, StudentT, cdf

LEVEL_TOL = Rational(1, 1000)       # a critical value given to 3-4 digits is within this of its level


def _frac(v) -> Fraction:
    v = sp.radsimp(sp.simplify(sp.sympify(v)))            # (exact: no float is ever involved)
    if not isinstance(v, sp.Rational):
        raise ValueError(f"{v} is not a rational number")
    return Fraction(int(v.p), int(v.q))


def _r(text) -> sp.Rational:
    return Rational(str(text))


def _pairwise_variance(xs) -> sp.Rational:
    n = len(xs)
    total = sum(((_r(a) - _r(b)) ** 2 for a, b in itertools.combinations(xs, 2)), Rational(0))
    return total / (n * (n - 1))


def _laplace(z) -> Fraction:
    """Phi(|z|) to 4 decimals, computed from erf; odd in z."""
    z = sp.nsimplify(z)
    value = sp.erf(abs(z) / sp.sqrt(2)) / 2
    rounded = Fraction(int(sp.floor(value * 10 ** 4 + Rational(1, 2))), 10 ** 4)
    return rounded if z >= 0 else -rounded


def _normal_event(event: str, var: str, mean, sd) -> Fraction:
    """P(event) for a normal variable named `var` with this mean and sd, from the erf table."""
    e = event.replace(" ", "")
    z = lambda c: (_r(c) - mean) / sd                      # noqa: E731
    if f"<{var}<" in e:
        lo, hi = e.split(f"<{var}<")
        return _laplace(z(hi)) - _laplace(z(lo))
    if e.startswith(f"{var}>"):
        return Fraction(1, 2) - _laplace(z(e[len(var) + 1:]))
    if e.startswith(f"{var}<"):
        return Fraction(1, 2) + _laplace(z(e[len(var) + 1:]))
    raise ValueError(f"cannot read the event {event!r}")


def _check_z(z) -> None:
    """A two-sided z given in a prompt (1.645, 1.96, 2.58) has 2 Phi(z) within LEVEL_TOL of 0.90/0.95/0.99."""
    level = sp.erf(_r(z) / sp.sqrt(2))
    if not any(abs(level - Rational(k, 100)) < LEVEL_TOL for k in (90, 95, 99)):
        raise ValueError(f"z = {z} is not a usual two-sided critical value")


# ------------------------------------------------------------------ floor 7
def _phuong_sai_mau(p: dict) -> list[Fraction]:
    xs = p["data"]
    return [_frac(Rational(sum(xs), len(xs))), _frac(_pairwise_variance(xs))]


def _bang_tan_so(p: dict) -> list[Fraction]:
    raw = [v for v, c in zip(p["values"], p["counts"]) for _ in range(c)]
    return [_frac(Rational(sum(raw), len(raw))), _frac(_pairwise_variance(raw))]


def _trung_binh_mau_chuan(p: dict) -> list[Fraction]:
    sd = sp.sqrt(_mean_variance(Rational(p["sigma"]) ** 2, p["n"]))     # V(X_tb), term by term
    return [_normal_event(p["event"], "X_tb", p["mu"], sd)]


def _khong_chech_tf(p: dict) -> bool:
    mu = sp.Symbol("mu", real=True)
    # any law of mean mu will do: two points mu - 1, mu + 1, each with probability 1/2
    xs = [FiniteRV(f"X{i}", {mu - 1: Rational(1, 2), mu + 1: Rational(1, 2)}) for i in range(len(p["coeffs"]))]
    t = sum((_r(c) * x for c, x in zip(p["coeffs"], xs)), Rational(0))
    return sp.simplify(E(t) - mu) == 0


def _hop_ly(p: dict) -> list[Fraction]:
    th = sp.Symbol("theta", positive=True)
    xs = p["data"]
    model = p["model"]
    if model == "bernoulli":
        logl = sum(sp.log(th ** x * (1 - th) ** (1 - x)) for x in xs)
    elif model == "poisson":
        logl = sum(sp.log(sp.exp(-th) * th ** x / sp.factorial(x)) for x in xs)
    elif model == "mu":
        logl = sum(sp.log(th * sp.exp(-th * x)) for x in xs)
    elif model == "hinh_hoc":
        logl = sum(sp.log(th * (1 - th) ** (x - 1)) for x in xs)
    else:
        raise ValueError(model)
    logl = sp.expand_log(logl, force=True)
    roots = [r for r in sp.solve(sp.diff(logl, th), th) if r.is_positive]
    if model in ("bernoulli", "hinh_hoc"):
        roots = [r for r in roots if r < 1]
    if len(roots) != 1:
        raise ValueError(f"the likelihood equation has roots {roots}")
    root = roots[0]
    if not sp.diff(logl, th, 2).subs(th, root) < 0:
        raise ValueError("the root is not a maximum")
    return [_frac(root)]


# ------------------------------------------------------------------ floor 8
def _interval(xbar, eps) -> list[Fraction]:
    mu = sp.Symbol("mu", real=True)
    roots = sp.solve(sp.Eq((_r(xbar) - mu) ** 2, eps ** 2), mu)
    return sorted(_frac(r) for r in roots)


def _khoang_biet_sigma(p: dict) -> list[Fraction]:
    _check_z(p["z"])
    return _interval(p["xbar"], _r(p["z"]) * _r(p["sigma"]) / sp.sqrt(p["n"]))


def _khoang_t(p: dict) -> list[Fraction]:
    df = p["n"] - 1
    tail = 1 - cdf(StudentT("T", df))(_r(p["t"]))
    tail = sp.N(tail, 12)
    if not any(abs(tail - q) < 5e-4 for q in (0.025, 0.05)):
        raise ValueError(f"t({df}) = {p['t']} leaves {tail} above it")
    return _interval(p["xbar"], _r(p["t"]) * _r(p["s"]) / sp.sqrt(p["n"]))


def _ty_le8(p: dict) -> list[Fraction]:
    _check_z(p["z"])
    q = sp.Symbol("p", real=True)
    f = Rational(p["m"], p["n"])
    roots = sp.solve(sp.Eq((f - q) ** 2, _r(p["z"]) ** 2 * f * (1 - f) / p["n"]), q)
    return sorted(_frac(r) for r in roots)


def _smallest(ok) -> int:
    """The smallest n >= 1 with ok(n), for ok monotone in n: doubling then bisection."""
    hi = 1
    while not ok(hi):
        hi *= 2
    lo = hi // 2                                          # ok(lo) is false (or lo = 0)
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid
    return hi


def _co_mau(p: dict) -> list[Fraction]:
    _check_z(p["z"])
    z, eps = _r(p["z"]), _r(p["eps"])
    if p["kind"] == "trung_binh":
        sigma = _r(p["sigma"])
        return [Fraction(_smallest(lambda n: bool(z * sigma / sp.sqrt(n) <= eps)))]
    f = _r(p["f"])
    return [Fraction(_smallest(lambda n: bool(z * sp.sqrt(f * (1 - f) / n) <= eps)))]


def _mean_variance(var, n: int) -> sp.Rational:
    """V((X_1 + ... + X_n)/n) for independent X_i of variance var, term by term."""
    return sum((Rational(1, n) ** 2 * var for _ in range(n)), Rational(0))


def _chebyshev(p: dict) -> list[Fraction]:
    var, eps = _r(p["var"]), _r(p["eps"])
    if p["kind"] == "can":
        return [_frac(_mean_variance(var, p["n"]) / eps ** 2)]
    delta = _r(p["delta"])
    return [Fraction(_smallest(lambda n: var / (n * eps ** 2) <= delta))]


def _tong_clt(p: dict) -> list[Fraction]:
    n = p["n"]
    mean = sum((Rational(p["m"]) for _ in range(n)), Rational(0))           # E(S) and V(S), term by term
    var = sum((Rational(p["sd"]) ** 2 for _ in range(n)), Rational(0))
    return [_normal_event(p["event"], "S", mean, sp.sqrt(var))]


# ------------------------------------------------------------------ floor 9
def _z_trung_binh(p: dict) -> list[Fraction]:
    n = p["n"]
    total = n * _r(p["xbar"])                                # the sum of the sample
    return [_frac((total - n * p["mu0"]) / (_r(p["sigma"]) * sp.sqrt(n)))]


def _t_trung_binh(p: dict) -> list[Fraction]:
    xs = [Rational(x) for x in p["data"]]
    n = len(xs)
    s = sp.sqrt(_pairwise_variance(p["data"]))
    return [_frac((sum(xs) / n - p["mu0"]) / (s / sp.sqrt(n)))]


def _ty_le9(p: dict) -> list[Fraction]:
    p0, n = _r(p["p0"]), p["n"]
    return [_frac((Rational(p["m"], n) - p0) / sp.sqrt(p0 * (1 - p0) / n))]


def _hai_trung_binh(p: dict) -> list[Fraction]:
    se = sp.sqrt(_r(p["s1"]) ** 2 / p["n1"] + _r(p["s2"]) ** 2 / p["n2"])
    return [_frac((_r(p["x1"]) - _r(p["x2"])) / se)]


def _quyet_dinh(p: dict) -> bool:
    z = (_r(p["xbar"]) - p["mu0"]) / (_r(p["sigma"]) / sp.sqrt(p["n"]))
    upper = (1 - sp.erf(z / sp.sqrt(2))) / 2                 # P(Z > z)
    lower = (1 + sp.erf(z / sp.sqrt(2))) / 2                 # P(Z < z)
    pvalue = {"!=": 2 * sp.Min(upper, lower), ">": upper, "<": lower}[p["alt"]]
    alpha = _r(p["alpha"])
    if abs(sp.N(pvalue - alpha)) < 1e-3:
        raise ValueError(f"p-value {sp.N(pvalue)} too close to alpha {alpha} to decide by a table")
    return bool(sp.N(pvalue) < alpha)


EXPECTED: dict = {
    # ---- floor 7
    "xs_g7_phuong_sai_mau": _phuong_sai_mau,
    "xs_g7_bang_tan_so": _bang_tan_so,
    "xs_g7_trung_binh_mau_chuan": _trung_binh_mau_chuan,
    "xs_g7_khong_chech_tf": _khong_chech_tf,
    "xs_g7_hop_ly": _hop_ly,
    # ---- floor 8
    "xs_g8_khoang_biet_sigma": _khoang_biet_sigma,
    "xs_g8_khoang_t": _khoang_t,
    "xs_g8_ty_le": _ty_le8,
    "xs_g8_co_mau": _co_mau,
    "xs_g8_chebyshev": _chebyshev,
    "xs_g8_tong_clt": _tong_clt,
    # ---- floor 9
    "xs_g9_z_trung_binh": _z_trung_binh,
    "xs_g9_t_trung_binh": _t_trung_binh,
    "xs_g9_ty_le": _ty_le9,
    "xs_g9_hai_trung_binh": _hai_trung_binh,
    "xs_g9_quyet_dinh": _quyet_dinh,
}
