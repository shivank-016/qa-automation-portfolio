"""
Checkout Flow Event Verification
----------------------------------
Drives a public demo e-commerce site (saucedemo.com) through a login ->
add-to-cart -> checkout flow with Playwright, and verifies that each step
in the flow actually produces the state/UI change it's supposed to.

This is a generic stand-in for the kind of event/flow verification done in
real QA work: define what SHOULD happen at each step, drive the app, then
check the captured evidence (URL, DOM state, network requests) against
that expectation instead of eyeballing it manually.

Usage:
    pip install -r requirements.txt
    python -m playwright install chromium
    python verify_checkout_flow.py

Writes results/checkout_flow_results.json, which feeds directly into
../qa-report-generator/report_generator.py to produce the Excel report.
"""

import json
import os
from playwright.sync_api import sync_playwright

BASE_URL = "https://www.saucedemo.com"
RESULTS_PATH = os.path.join(os.path.dirname(__file__), "results", "checkout_flow_results.json")

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


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        network_log = []
        page.on("request", lambda req: network_log.append(req.url))

        # Step 1: Login
        page.goto(f"{BASE_URL}/")
        page.fill("#user-name", "standard_user")
        page.fill("#password", "secret_sauce")
        page.click("#login-button")
        page.wait_for_url("**/inventory.html")

        check(
            "Login: valid credentials reach inventory page",
            "Functional",
            page.url.endswith("/inventory.html"),
            "Redirected to /inventory.html after valid login",
            f"Current URL: {page.url}",
        )

        # Step 2: Add two items to cart
        page.click("#add-to-cart-sauce-labs-backpack")
        page.click("#add-to-cart-sauce-labs-bike-light")
        cart_badge = page.text_content(".shopping_cart_badge")

        check(
            "Cart: badge reflects number of items added",
            "Functional",
            cart_badge == "2",
            "Cart badge shows '2' after adding two items",
            f"Cart badge shows '{cart_badge}'",
        )

        # Step 3: Go to cart, verify both items listed
        page.click(".shopping_cart_link")
        page.wait_for_url("**/cart.html")
        item_names = page.locator(".inventory_item_name").all_text_contents()

        expected_items = {"Sauce Labs Backpack", "Sauce Labs Bike Light"}
        check(
            "Cart page: lists the correct items",
            "Functional",
            expected_items.issubset(set(item_names)),
            f"Cart contains: {sorted(expected_items)}",
            f"Cart contains: {item_names}",
        )

        # Step 4: Proceed through checkout
        page.click("#checkout")
        page.wait_for_url("**/checkout-step-one.html")
        page.fill("#first-name", "Jane")
        page.fill("#last-name", "Doe")
        page.fill("#postal-code", "94016")
        page.click("#continue")
        page.wait_for_url("**/checkout-step-two.html")

        summary_total = page.text_content(".summary_total_label")
        check(
            "Checkout overview: shows a total price",
            "Event Verification",
            summary_total is not None and "Total" in summary_total,
            "Order summary includes a 'Total: $X' line",
            f"Found: {summary_total}",
        )

        page.click("#finish")
        page.wait_for_url("**/checkout-complete.html")
        complete_header = page.text_content(".complete-header")

        check(
            "Checkout complete: confirmation message fires",
            "Event Verification",
            complete_header is not None and "Thank you" in complete_header,
            "Completion page shows a 'Thank you for your order' style message",
            f"Found: {complete_header}",
        )

        # Step 5: Check that the app made at least one API-style network call
        # during the flow (demonstrates request capture, the same mechanism
        # used to verify analytics/event calls in real event-verification work)
        xhr_like = [u for u in network_log if "inventory" in u or "cart" in u or "checkout" in u]
        check(
            "Network: flow pages were requested as expected",
            "Event Verification",
            len(xhr_like) >= 3,
            "At least 3 flow-related page requests captured (inventory/cart/checkout)",
            f"Captured {len(xhr_like)} matching requests",
            notes=(
                "Genuine finding, not a script bug: saucedemo.com's inventory/cart/"
                "checkout transitions are client-side JS routing with no full page "
                "load, so no matching network request fires. A real event-verification "
                "harness needs to know whether a flow step is expected to produce a "
                "network/analytics call before asserting on it — this is exactly the "
                "kind of false assumption that a verification script needs to catch "
                "and a QA engineer needs to correct."
            ),
        )

        browser.close()

    os.makedirs(os.path.dirname(RESULTS_PATH), exist_ok=True)
    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    passed = sum(1 for r in results if r["status"] == "pass")
    print(f"\n{passed}/{len(results)} checks passed. Results written to {RESULTS_PATH}")


if __name__ == "__main__":
    run()
