# Playwright Checkout Flow Verification

A Playwright script that drives a public demo e-commerce site
([saucedemo.com](https://www.saucedemo.com)) through a login → add-to-cart →
checkout flow and verifies each step produces the state change it's
supposed to, instead of relying on a human clicking through and eyeballing
the result.

This is a generic, from-scratch version of the event/flow verification
pattern I use in real QA work: drive the app, capture evidence (URL, DOM
state, network requests), and assert it against what the flow is *supposed*
to do at each step.

## What it checks

1. Login redirects to the inventory page with valid credentials
2. The cart badge count reflects items added
3. The cart page lists the correct items
4. The checkout overview page shows an order total
5. The checkout-complete page shows a confirmation message
6. Flow transitions produce the network activity expected of them

## Run it

```bash
pip install -r requirements.txt
python -m playwright install chromium
python verify_checkout_flow.py
```

Writes `results/checkout_flow_results.json`, which can be fed straight into
[`../qa-report-generator`](../qa-report-generator) to produce a styled
Excel report — see [`results/checkout_flow_report.xlsx`](results/checkout_flow_report.xlsx)
for the output from the run checked into this repo.

## A real finding from this script, not a staged one

Check #6 fails on the live site, and it's a genuine result worth reading,
not a bug in the script: saucedemo.com's inventory → cart → checkout
transitions are client-side JS routing, so no full network request fires on
navigation. A verification harness that assumes "a flow step means a
network call" will produce a false failure here — which is itself a useful
thing for a verification script to surface. In real event-verification
work, confirming *whether* a given UI action is expected to produce a
network/analytics call — before asserting on it — is as much a part of the
job as writing the assertion itself. I left this check failing (with a note
explaining why) rather than quietly removing or "fixing" it, because a
report that's all green isn't a very convincing one.
