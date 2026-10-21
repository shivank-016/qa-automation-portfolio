# Bot Handling Verification

A Playwright script that verifies a common fraud/bot-handling requirement
for client-side features: a bot visitor should be silently blocked from a
gated action (without the UI tipping it off by hiding the control), and
every analytics event should carry accurate `is_bot` / `bot_kind` tags so
bot traffic doesn't pollute real visitor metrics — while a genuine visitor
is completely unaffected.

This is a generic, from-scratch version of a verification pattern I use in
real QA work: a feature ships with bot-detection logic gating an action
(e.g. an AI-generation button), and the requirement is two-sided — bots
must be blocked *and* tagged correctly, humans must pass through cleanly.

## How it works

[`demo_site/index.html`](demo_site/index.html) is a small, self-contained
page with a minimal, dependency-free bot detector (a stand-in for a real
fingerprint-based detector like FingerprintJS BotD) gating a
"Generate AI Content" button, plus an analytics stub that tags every event
with `is_bot`/`bot_kind`.

[`verify_bot_handling.py`](verify_bot_handling.py) drives that page twice:

1. **As a default Playwright session** — which genuinely looks like a bot
   to the page's detector (`navigator.webdriver` is `true`, among other
   automation signals). This is a real Playwright characteristic, not a
   flaw in the script — it's what makes this test meaningful instead of
   needing a second real device.
2. **With an init script that spoofs a normal browser's fingerprint** —
   simulating a genuine human visitor.

## What it checks, per session

1. The bot detector returns a boolean `is_bot` flag (and a `bot_kind`
   reason when true)
2. The gated action responds correctly for that visitor type: blocked for
   a bot, succeeds for a human
3. The gated button stays visible either way — bots aren't tipped off by a
   hidden/disabled control
4. Every analytics event fired during the session is tagged with the
   correct `is_bot`/`bot_kind` value

## Run it

```bash
pip install -r requirements.txt
python -m playwright install chromium
python verify_bot_handling.py
```

Writes `results/bot_handling_results.json`, which feeds straight into
[`../qa-report-generator`](../qa-report-generator) to produce a styled
Excel report — see [`results/bot_handling_report.xlsx`](results/bot_handling_report.xlsx)
for the output from the run checked into this repo (8/8 passed).

```bash
python ../qa-report-generator/report_generator.py results/bot_handling_results.json results/bot_handling_report.xlsx
```
