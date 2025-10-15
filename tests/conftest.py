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

# Do not force a specific Kivy window provider locally; CI will run headless stubs

# Make sure project root is importable
repo_root = os.path.dirname(os.path.dirname(__file__))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

# Headless-safe stubs for CI (non-Xvfb jobs)
if os.environ.get("RUN_UI_TESTS") != "1" and os.environ.get("CI") == "true":
    # Provide a minimal dummy EventLoop window and assign global Window
    try:
        from kivy.base import EventLoop
        from kivy.core import window as core_window

        class _DummyWindow:
            dpi = 96
            width = 800
            height = 600
            size = (800, 600)
            scale = 1

            def bind(self, *args, **kwargs):
                return None

            def unbind(self, *args, **kwargs):
                return None

        # Create the dummy window immediately so imports that access Window.size succeed
        if getattr(EventLoop, "window", None) is None:
            EventLoop.window = _DummyWindow()
        core_window.Window = EventLoop.window  # make global Window available

        def _ensure_window():
            if getattr(EventLoop, "window", None) is None:
                EventLoop.window = _DummyWindow()
                core_window.Window = EventLoop.window
            return EventLoop.window

        EventLoop.ensure_window = staticmethod(_ensure_window)  # type: ignore[assignment]
    except Exception:
        pass

    try:
        from kivymd.uix.pickers import MDDatePicker, MDTimePicker

        def _noop_open(self, *args, **kwargs):
            return None

        MDDatePicker.open = _noop_open  # type: ignore[attr-defined]
        MDTimePicker.open = _noop_open  # type: ignore[attr-defined]
    except Exception:
        # If kivymd is not importable yet, ignore; tests importing it will still see env vars
        pass

    try:
        from kivy.uix.popup import Popup

        def _popup_open(self, *args, **kwargs):
            # Trigger on_open hook without creating a real window
            on_open = getattr(self, "on_open", None)
            if callable(on_open):
                try:
                    on_open()
                except Exception:
                    pass
            return self

        def _popup_dismiss(self, *args, **kwargs):
            return self

        Popup.open = _popup_open  # type: ignore[assignment]
        Popup.dismiss = _popup_dismiss  # type: ignore[assignment]
    except Exception:
        pass
