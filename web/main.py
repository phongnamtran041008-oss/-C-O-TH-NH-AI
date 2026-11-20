"""Toán Tu Tiên in the browser (M12): the entry pygbag runs. tools/build_web.py copies this
file next to a copy of client/ and packs both; see docs/WEB_BUILD.md."""
import asyncio

import pygame  # noqa: F401  (named here so pygbag fetches pygame-ce before the game starts)

from client.main import web_main

asyncio.run(web_main())
