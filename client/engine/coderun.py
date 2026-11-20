"""Running the learner's own program, on the learner's own machine (milestone M6).

The plan is explicit about this: a programming exercise is marked the way a school runner
does it - take the learner's solution file, run it once per test with that test's input on
stdin, with a time limit, and look at what it printed. Nothing of the player's code is ever
sent anywhere, and the game never runs code that came from a server: the only thing started
here is one file the player wrote, with a fixed command line.

Verdicts (plan 5.2): CE, RE, TLE come from the run itself and are decided here; AC and WA
need the expected output, which only the server has, so comparing is its job
(server/app/learning/math_problems.py). This module just reports what happened.

No pygame and nothing else from the game: tools/check_all.py imports it to check that every
exercise's reference solution really produces the expected output.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

OK, CE, RE, TLE = "ok", "ce", "re", "tle"
DEFAULT_TIME_LIMIT_MS = 2000
MAX_OUTPUT_CHARS = 100_000
KILL_GRACE_S = 2.0
# The pygbag web build (M12) has no subprocess: programs run in-process, see run_in_process
IN_BROWSER = sys.platform == "emscripten"
WEB_SLOWDOWN = 3


@dataclass
class RunResult:
    """What one test run did. `status` is ok / re / tle (ce never reaches a run)."""
    status: str
    output: str = ""
    error: str = ""                 # the tail of stderr, for the player to read
    ms: int = 0

    @property
    def ok(self) -> bool:
        return self.status == OK


@dataclass
class Attempt:
    """One Chạy thử or Nộp bài: the compile check, then one run per test."""
    status: str                     # ok (every test ran) / ce / re / tle - the first thing that went wrong
    runs: list[RunResult] = field(default_factory=list)
    error: str = ""                 # the compile error, or the error of the run that failed

    @property
    def outputs(self) -> list[str]:
        return [r.output for r in self.runs]

    @property
    def times_ms(self) -> list[int]:
        return [r.ms for r in self.runs]


class NoPython(RuntimeError):
    """No Python interpreter to run the exercise with (a packaged game is not one)."""


def interpreter(explicit: str = "") -> str:
    """The Python that runs the learner's program. Running from source that is the one
    running the game; a packaged game is not a Python interpreter, so one has to be found
    on the PATH, or named by the player in config.json ("python_path")."""
    if explicit:
        if Path(explicit).is_file():
            return explicit
        found = shutil.which(explicit)
        if found:
            return found
        raise NoPython(explicit)
    if not getattr(sys, "frozen", False) and sys.executable:
        return sys.executable
    for name in ("python3", "python", "py"):
        found = shutil.which(name)
        if found:
            return found
    raise NoPython("python")


def compile_problem(code: str, filename: str = "bai_lam.py") -> str:
    """The compile error of this source, or "" when it is syntactically fine. Compiling is
    not running: nothing in the code is executed here."""
    try:
        compile(code, filename, "exec")
    except SyntaxError as e:
        where = f" (dòng {e.lineno})" if e.lineno else ""
        return f"{type(e).__name__}{where}: {e.msg}"
    except ValueError as e:                     # e.g. source with a NUL byte
        return f"ValueError: {e}"
    return ""


def write_solution(path: Path, code: str) -> Path:
    """Save the solution where the player can also open it in their own editor."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(code, "utf-8", newline="\n")
    return path


def run_one(path: Path, data: str, time_limit_ms: int = DEFAULT_TIME_LIMIT_MS,
            python: str = "", max_output_chars: int = MAX_OUTPUT_CHARS) -> RunResult:
    """Run the solution file once with `data` on stdin. The command line is fixed: the
    interpreter, -I (ignore environment variables and the user's site directory, so a run
    is the same everywhere), -X utf8 (so printing Vietnamese works whatever the machine's
    code page is - PYTHONIOENCODING would be ignored, that is what -I means) and the file.
    Test data only ever goes in through stdin."""
    if IN_BROWSER:
        return run_in_process(path.read_text("utf-8"), data, time_limit_ms, max_output_chars, path.name)
    exe = interpreter(python)
    limit = max(0.1, time_limit_ms / 1000)
    env = {k: v for k, v in os.environ.items() if not k.startswith("PYTHON")}
    started = time.perf_counter()
    try:
        proc = subprocess.run([exe, "-I", "-X", "utf8", str(path)], input=data, capture_output=True,
                              text=True, encoding="utf-8", errors="replace", timeout=limit,
                              cwd=str(path.parent), env=env)
    except subprocess.TimeoutExpired:
        return RunResult(TLE, ms=time_limit_ms)
    except OSError as e:
        return RunResult(RE, error=f"không chạy được: {e}", ms=0)
    ms = int((time.perf_counter() - started) * 1000)
    out = (proc.stdout or "")[:max_output_chars]
    if proc.returncode != 0:
        tail = "\n".join((proc.stderr or "").strip().splitlines()[-6:])
        return RunResult(RE, output=out, error=tail, ms=ms)
    return RunResult(OK, output=out, ms=ms)


class _TimeUp(BaseException):
    """Raised inside the player's program by the tracer when its time is up."""


def run_in_process(source: str, data: str, time_limit_ms: int = DEFAULT_TIME_LIMIT_MS,
                   max_output_chars: int = MAX_OUTPUT_CHARS, filename: str = "bai_lam.py") -> RunResult:
    """The web build (M12): a page cannot start another Python, so the program runs inside
    the game's own interpreter, with `data` as its stdin and its prints caught. The time
    limit is kept by a line tracer that stops the program when the time is up. Tracing
    slows Python down a few times, so the program gets WEB_SLOWDOWN times its limit; the
    time it reports is what it really took. The page freezes while the program runs (there
    is no thread to run it on), at most WEB_SLOWDOWN x the limit per test."""
    import builtins
    import io
    import traceback

    code = compile(source, filename, "exec")
    stdin, out, err = io.StringIO(data), io.StringIO(), io.StringIO()
    started = time.perf_counter()
    deadline = started + max(0.1, time_limit_ms / 1000) * WEB_SLOWDOWN
    count = 0

    def tracer(frame, event, arg):
        nonlocal count
        count += 1
        if not count & 255 and time.perf_counter() > deadline:
            raise _TimeUp
        return tracer

    def read_line(prompt=""):
        line = stdin.readline()
        if not line:
            raise EOFError("EOF when reading a line")
        return line[:-1] if line.endswith("\n") else line

    env = {"__name__": "__main__", "__file__": filename, "__builtins__": builtins, "input": read_line}
    saved = sys.stdin, sys.stdout, sys.stderr, sys.gettrace(), sys.getrecursionlimit()
    status = OK
    sys.stdin, sys.stdout, sys.stderr = stdin, out, err
    sys.settrace(tracer)
    try:
        exec(code, env)
    except _TimeUp:
        status = TLE
    except SystemExit as e:
        if e.code not in (None, 0):
            status = RE
            if not isinstance(e.code, int):
                err.write(f"{e.code}\n")
    except BaseException:
        status = RE
        traceback.print_exc(file=err)
    finally:
        sys.settrace(saved[3])
        sys.stdin, sys.stdout, sys.stderr = saved[:3]
        sys.setrecursionlimit(saved[4])
    ms = int((time.perf_counter() - started) * 1000)
    if status == TLE:
        return RunResult(TLE, ms=time_limit_ms)
    output = out.getvalue()[:max_output_chars]
    if status == RE:
        tail = "\n".join(err.getvalue().strip().splitlines()[-6:])
        return RunResult(RE, output=output, error=tail, ms=ms)
    return RunResult(OK, output=output, ms=ms)


def run_tests(path: Path, inputs: list[str], time_limit_ms: int = DEFAULT_TIME_LIMIT_MS,
              python: str = "", code: str | None = None,
              max_output_chars: int = MAX_OUTPUT_CHARS) -> Attempt:
    """Compile the solution, then run it once per test, stopping at the first test that
    does not finish (a program that crashes or runs out of time on test 2 has nothing more
    to say about test 3). `code` saves reading the file again when the caller has it."""
    source = code if code is not None else path.read_text("utf-8")
    problem = compile_problem(source, path.name)
    if problem:
        return Attempt(CE, error=problem)
    runs: list[RunResult] = []
    for data in inputs:
        result = run_one(path, data, time_limit_ms, python, max_output_chars)
        runs.append(result)
        if not result.ok:
            return Attempt(result.status, runs, error=result.error)
    return Attempt(OK, runs)
