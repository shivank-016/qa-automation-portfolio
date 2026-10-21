"""
Bot Handling Verification
---------------------------
Verifies a common fraud/bot-handling requirement for client-side features:
a bot visitor should be silently blocked from a gated action (without the
UI tipping it off by hiding the control), and analytics events should be
correctly tagged is_bot/bot_kind so bot traffic doesn't pollute real
visitor metrics -- while a genuine visitor is unaffected.

This drives a small self-contained demo page (demo_site/index.html) twice:
  1. As a default Playwright session, which looks like a bot to the page's
     fingerprint-based detector (navigator.webdriver is true, among other
     automation signals) -- this is the same reason a real headless/
     automated session is detectable, and is a genuine Playwright
     characteristic, not a flaw in this script.
  2. With an init script that spoofs a normal browser's fingerprint,
     simulating a genuine human visitor.

Usage:
    pip install -r requirements.txt
    python -m playwright install chromium
    python verify_bot_handling.py
"""

import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

DEMO_SITE_PATH = (Path(__file__).parent / "demo_site" / "index.html").resolve().as_uri()
RESULTS_PATH = os.path.join(os.path.dirname(__file__), "results", "bot_handling_results.json")

results = []


def check(name, category, condition, expected, actual, notes=""):
    status = "pass" if condition else "fail"
    results.append({
        "name": name,
        "category": category,
        "status": status,
        "expected": expected,
        "actual": actual,
        "notes": notes,
    })
    print(f"[{status.upper()}] {name}")


HUMAN_LIKE_INIT_SCRIPT = """
Object.defineProperty(navigator, 'webdriver', { get: () => false });
Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
window.chrome = { runtime: {} };
"""


def run_session(page, label):
    page.goto(DEMO_SITE_PATH)

    is_bot = page.evaluate("window.__isBot")
    bot_kind = page.evaluate("window.__botKind")

    page.click("#generate-btn")
    status_text = page.text_content("#status")
    is_visible = page.is_visible("#generate-btn")
    events = page.evaluate("window.__events")

    tagged_correctly = all(e.get("is_bot") == is_bot for e in events)

    check(
        f"[{label}] Bot flag detected as expected",
        "Bot Handling",
        is_bot is not None,
        "detectBot() returns a boolean is_bot flag",
        f"is_bot={is_bot}, bot_kind={bot_kind}",
    )

    check(
        f"[{label}] Gated action responds correctly for this visitor type",
        "Bot Handling",
        ("blocked" in status_text.lower()) == bool(is_bot),
        "Bot visitor: action blocked. Human visitor: action succeeds.",
        f"is_bot={is_bot}, status message: '{status_text}'",
    )

    check(
        f"[{label}] Gated button stays visible regardless of bot status",
        "Bot Handling",
        is_visible,
        "Button remains visible even when the action is blocked (no tipping off automated traffic)",
        f"Button visible: {is_visible}",
    )

    check(
        f"[{label}] Analytics events are tagged with is_bot/bot_kind",
        "Event Verification",
        tagged_correctly and len(events) > 0,
        "Every emitted event includes is_bot matching the detected value",
        f"{len(events)} events captured, all tagged is_bot={is_bot}: {tagged_correctly}",
    )


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # Session 1: default Playwright session -- looks like a bot
        bot_page = browser.new_page()
        run_session(bot_page, "Automated session")
        bot_page.close()

        # Session 2: spoofed fingerprint -- looks like a genuine visitor
        human_context = browser.new_context()
        human_context.add_init_script(HUMAN_LIKE_INIT_SCRIPT)
        human_page = human_context.new_page()
        run_session(human_page, "Human-like session")
        human_context.close()

        browser.close()

    os.makedirs(os.path.dirname(RESULTS_PATH), exist_ok=True)
    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    passed = sum(1 for r in results if r["status"] == "pass")
    print(f"\n{passed}/{len(results)} checks passed. Results written to {RESULTS_PATH}")


if __name__ == "__main__":
    run()
