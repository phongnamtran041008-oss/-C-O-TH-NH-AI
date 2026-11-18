import os
import sys
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pygame  # noqa: E402
import pytest  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def pg():
    pygame.init()
    pygame.display.set_mode((480, 270))
    yield


@pytest.fixture(autouse=True)
def pg_alive():
    """A flow test ends with Game.shutdown(), which quits pygame. A unit test that happens to
    run after one (the order is alphabetical, so a new test file can land there) must still find
    pygame up, instead of passing or failing by the name of its file."""
    if not pygame.get_init() or not pygame.display.get_init() or pygame.display.get_surface() is None:
        pygame.init()
        pygame.display.set_mode((480, 270))
    yield
