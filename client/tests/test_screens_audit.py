"""The screens audit (tools/audit_screens.py) on a representative subset, at scales 2 and 3:
no screen may have a cut, covered, clipped or overflowing text, nor a glyph the fonts lack.

The whole audit (every screen and tab) is `python tools/audit_screens.py`; this keeps the
worst cases of each kind of screen in the test suite: the Chính đạo card with the longest node
name and why, a branch tab scrolled to its end, the summary after a Thiên kiếp nhỏ that opens
many nodes, the node card, the guide board and the HUD tracker once Chính đạo leads, the bag
scrolled to its end, the shop, the pets, and the code screen with a long traceback. The other
screens read real payloads of the server, which the tool runs in this process."""
from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import audit_screens as AS  # noqa: E402

SUBSET = {"hub/chinh_dao_luyen_longest", "hub/tab_gt_end", "hub/tab_xs", "summary/trial_passed_opens_many",
          "summary/sitting_longest", "node_card/longest_name", "node_card/most_lines_scrolled_end",
          "guide/road_main_longest", "guide/hud_tracker_main_longest", "guide/hud_tracker_welcome",
          "bag/items_end", "bag/weapons_end", "shop/buy", "pets/list", "code/failing_run_detail",
          "xa_truong/statement_longest", "td/gate", "achievements/tab_tu_luyen"}


def test_the_subset_is_still_in_the_tool():
    names = {f"{s}/{n}" for s, n, _ in AS.CASES}
    assert SUBSET <= names, SUBSET - names


def test_no_hard_problem_on_the_worst_screens():
    result = AS.run((2, 3), only=SUBSET, quiet=True)
    assert result["_errors"] == [], result["_errors"]
    hard = [f"{k[0]}/{k[1]} x{k[2]}: {p.describe()}" for k, got in result.items() if k != "_errors"
            for p in got["hard"]]
    assert hard == [], "\n".join(hard[:20])
    assert len([k for k in result if k != "_errors"]) == 2 * len(SUBSET)
