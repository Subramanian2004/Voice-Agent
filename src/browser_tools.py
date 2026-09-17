"""
Browser automation tools using Playwright — the right tool for anything
happening inside a web page, since it finds elements by their actual
text/labels instead of guessing screen coordinates from a screenshot.

SAFETY: this launches Butcher's OWN isolated browser, with its own profile
folder inside this project (browser_profile/) — completely separate from
your everyday Chrome. It has no access to your real logins, saved
passwords, cookies, or history. If a task needs you to be logged into
something, log in inside this browser specifically; that session will
persist across runs but never touches your main browser.
"""

import os

from langchain_core.tools import tool

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_BROWSER_PROFILE_DIR = os.path.join(_PROJECT_ROOT, "browser_profile")

_playwright = None
_context = None
_page = None


def _confirm(action_description: str) -> bool:
    print(f"\n[CONFIRMATION NEEDED] Butcher wants to: {action_description}")
    answer = input("Type 'yes' to allow, anything else to cancel: ").strip().lower()
    return answer == "yes"


def _get_page():
    """Lazily launch Butcher's own isolated browser on first use, reuse after that."""
    global _playwright, _context, _page

    if _page is not None:
        return _page

    from playwright.sync_api import sync_playwright

    _playwright = sync_playwright().start()
    _context = _playwright.chromium.launch_persistent_context(
        _BROWSER_PROFILE_DIR,
        headless=False,
    )
    _page = _context.pages[0] if _context.pages else _context.new_page()
    return _page


def close_browser():
    """Call this on shutdown so the browser closes cleanly instead of being left running."""
    global _playwright, _context, _page
    if _context is not None:
        _context.close()
    if _playwright is not None:
        _playwright.stop()
    _context = None
    _page = None
    _playwright = None


@tool
def open_browser_url(url: str) -> str:
    """Open a URL in Butcher's own browser window (separate from your normal Chrome)."""
    page = _get_page()
    if not url.startswith("http"):
        url = "https://" + url
    page.goto(url)
    return f"Opened {url}"


@tool
def read_browser_page() -> str:
    """Get the visible text of the current page in Butcher's browser, to see what's
    there before deciding what to click or fill in."""
    page = _get_page()
    text = page.inner_text("body")
    return text[:3000]


@tool
def click_browser_text(text: str) -> str:
    """Click the first element on the current page containing this visible text
    (a link, button, menu item, etc). Asks the user to confirm first."""
    if not _confirm(f"click the element containing the text '{text}' on the current page"):
        return "Cancelled by user."
    page = _get_page()
    try:
        page.get_by_text(text, exact=False).first.click(timeout=5000)
        return f"Clicked element containing '{text}'."
    except Exception as e:
        return f"Could not click '{text}': {e}"


@tool
def type_in_browser_field(label_or_placeholder: str, text: str) -> str:
    """Type text into a browser form field identified by its label or placeholder
    text, e.g. 'Search' or 'Email address'. Asks the user to confirm first."""
    if not _confirm(f"type '{text}' into the field '{label_or_placeholder}'"):
        return "Cancelled by user."
    page = _get_page()
    try:
        try:
            field = page.get_by_label(label_or_placeholder, exact=False)
            field.fill(text, timeout=5000)
        except Exception:
            field = page.get_by_placeholder(label_or_placeholder, exact=False)
            field.fill(text, timeout=5000)
        return f"Typed into '{label_or_placeholder}'."
    except Exception as e:
        return f"Could not find field '{label_or_placeholder}': {e}"


BROWSER_TOOLS = [
    open_browser_url,
    read_browser_page,
    click_browser_text,
    type_in_browser_field,
]