---
name: web-flow-verifier
description: >
  Given a target URL and a list of UI steps with expected outcomes, drives
  the page with Playwright, checks each step's actual result against what
  was expected, and produces a styled Pass/Fail Excel report. Use this
  whenever asked to verify a web flow (login, checkout, signup, etc.)
  actually behaves as specified, and to turn the results into a shareable
  report instead of a manual spreadsheet.
---

# Web Flow Verifier

This skill is a reusable pattern for a QA task that comes up constantly:
"does this flow actually do what it's supposed to, and can I get that in a
report I can hand to someone." It's a generic version of the automation
tooling I build for recurring QA verification work — this copy is built
from scratch against a public demo site so it can be shared without
exposing any employer-specific process or product detail.

## When to use this skill

- The user describes a web flow (login, checkout, form submission, signup)
  and a list of things that should happen at each step
- The user wants the result as a report, not just a pass/fail shouted back
  in chat
- The flow needs to be re-verified repeatedly (e.g., after every deploy) —
  this skill turns a one-off manual check into something you can rerun

## How to run it

1. **Define the flow** as a list of steps, each with:
   - `name` — what the check is called
   - `category` — a grouping label (Functional, Event Verification, Regression, etc.)
   - an action to perform (click, fill, navigate)
   - an expected outcome (URL, DOM text, network request pattern)

2. **Drive the page with Playwright** (see
   [`../playwright-event-verification/verify_checkout_flow.py`](../playwright-event-verification/verify_checkout_flow.py)
   for a complete worked example against saucedemo.com). For each step:
   - Perform the action
   - Capture the actual outcome (`page.url`, `page.text_content(...)`,
     captured network requests)
   - Compare against the expected outcome
   - Record a result object matching the schema in
     [`references/result-schema.md`](references/result-schema.md)

3. **Write the results to JSON**, then generate the report:
   ```bash
   python report_generator.py results.json report.xlsx
   ```
   (see [`../qa-report-generator`](../qa-report-generator))

4. **Read the failures before declaring success.** A failing check is
   sometimes a real defect, and sometimes a wrong assumption baked into the
   check itself (e.g., assuming a client-side route change fires a network
   request when it doesn't). Always state which one it is — never silently
   delete or "fix" a check just to make the report green.

## Why a skill, not a one-off script

The value here isn't the Playwright code itself — it's having a repeatable,
documented process that turns "go check if X still works" into a command
that produces the same report format every time, regardless of which flow
is being verified. That consistency is what makes it worth re-running after
every release instead of re-deriving the check from scratch each time.
