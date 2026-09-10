"""
Tools the agent can call to actually do things on your laptop.

Start small and add tools deliberately — anything you hand the agent here
is something it can decide to run on its own, so keep each tool narrow
and predictable rather than exposing a general "run any shell command" tool.

SAFETY: any tool that controls your mouse/keyboard (click_at, type_text,
press_key) requires you to explicitly confirm in the terminal before it
runs. Don't remove that confirmation — it's the only thing standing
between a misheard instruction and an unintended action on your screen.
"""

import os
import subprocess
import sys

from langchain_core.tools import tool


def _confirm(action_description: str) -> bool:
    """Block and ask the user to explicitly approve a real-world action."""
    print(f"\n[CONFIRMATION NEEDED] Butcher wants to: {action_description}")
    answer = input("Type 'yes' to allow, anything else to cancel: ").strip().lower()
    return answer == "yes"


@tool
def list_directory(path: str = ".") -> str:
    """List files and folders in the given directory path on the user's laptop."""
    try:
        entries = os.listdir(path)
        return "\n".join(entries) if entries else "(empty directory)"
    except Exception as e:
        return f"Error: {e}"


@tool
def read_text_file(path: str) -> str:
    """Read and return the contents of a small text file on the user's laptop (first 5000 chars)."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read(5000)
    except Exception as e:
        return f"Error: {e}"


@tool
def open_application(app_name: str) -> str:
    """Open a desktop application by name, e.g. 'notepad', 'calculator', 'code', 'chrome'."""
    try:
        if sys.platform.startswith("win"):
            os.startfile(app_name)  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.run(["open", "-a", app_name], check=True)
        else:
            subprocess.run([app_name], check=False)
        return f"Opened {app_name}."
    except Exception as e:
        return f"Could not open {app_name}: {e}"


@tool
def get_screen_resolution() -> str:
    """Get the current screen resolution in pixels. Useful before deciding where to click."""
    import pyautogui

    width, height = pyautogui.size()
    return f"Screen resolution is {width}x{height}."


@tool
def click_at(x: int, y: int) -> str:
    """Click the mouse at the given screen pixel coordinates (x, y). Asks the user to confirm first."""
    if not _confirm(f"click at screen position ({x}, {y})"):
        return "Cancelled by user."
    import pyautogui

    pyautogui.click(x, y)
    return f"Clicked at ({x}, {y})."


@tool
def type_text(text: str) -> str:
    """Type the given text wherever the cursor/focus currently is. Asks the user to confirm first."""
    if not _confirm(f"type this text: {text!r}"):
        return "Cancelled by user."
    import pyautogui

    pyautogui.write(text, interval=0.03)
    return "Typed the text."


@tool
def press_key(key: str) -> str:
    """Press a single keyboard key, e.g. 'enter', 'tab', 'esc', 'backspace'. Asks the user to confirm first."""
    if not _confirm(f"press the '{key}' key"):
        return "Cancelled by user."
    import pyautogui

    pyautogui.press(key)
    return f"Pressed '{key}'."


# Register every tool you want the agent to have access to here.
ALL_TOOLS = [
    list_directory,
    read_text_file,
    open_application,
    get_screen_resolution,
    click_at,
    type_text,
    press_key,
]