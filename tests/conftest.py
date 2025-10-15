import os
import sys

# Ensure Kivy runs in a predictable headless-friendly mode during tests
# NOTE: This module is loaded by pytest before importing tests.

# Prevent Kivy from parsing pytest CLI args
os.environ.setdefault("KIVY_NO_ARGS", "1")
os.environ.setdefault("KIVY_NO_CONSOLELOG", "1")

# Make metrics independent from an actual window to avoid import-time DPI lookups
os.environ.setdefault("KIVY_METRICS_DENSITY", "1")
os.environ.setdefault("KIVY_DPI", "96")

# Prefer the mock window provider when UI tests are not explicitly requested
# (Linux job will export RUN_UI_TESTS=1 and run under xvfb to get a real window)
if os.environ.get("RUN_UI_TESTS") == "1":
    # Let Kivy use default SDL2 window under Xvfb; do not force dummy driver
    os.environ.pop("SDL_VIDEODRIVER", None)
    os.environ.setdefault("KIVY_WINDOW", "sdl2")
else:
    # Avoid creating a real OS window on non-Linux runners
    os.environ.setdefault("KIVY_WINDOW", "mock")

# Make sure project root is importable
repo_root = os.path.dirname(os.path.dirname(__file__))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)
