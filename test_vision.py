"""
Quick manual test for the vision-based screen finder, without going through
the full voice loop. Run this from the project root with the venv active:

    python test_vision.py

It takes a screenshot, asks moondream to locate whatever you describe, and
prints the coordinates it found — so you can sanity-check accuracy before
trusting it to actually click things.
"""

import sys

sys.path.insert(0, "src")

from tools import _ask_vision_for_coordinates, _screenshot_path  # noqa: E402


def main():
    description = input("Describe something visible on your screen right now: ")

    print("Taking screenshot...")
    image_path = _screenshot_path()
    print(f"Saved to {image_path} (you can open it to see exactly what the model saw)")

    print("Asking the vision model...")
    coords = _ask_vision_for_coordinates(description, image_path)

    if coords is None:
        print("Result: could not find it.")
    else:
        x, y = coords
        print(f"Result: found at approximately ({x}, {y})")
        print("Move your mouse there manually and compare — is it close?")


if __name__ == "__main__":
    main()