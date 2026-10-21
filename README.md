# QA Automation Portfolio

Hi, I'm Shivank — a QA Engineer with 7+ years in manual and automated
testing across web, Android, and iOS, currently working on email and
productivity products. This repo is a generic, from-scratch set of
automation tools showing the kind of QA tooling I build day-to-day, without
using any employer-specific code, products, or processes.

I build these tools by directing Claude (Anthropic's AI coding agent) to
write and iterate on the implementation — I scope the problem, design the
verification logic and what "pass" means, and validate/debug the results
against real runs. That workflow is itself part of what's demonstrated
here: turning a recurring manual QA task into a repeatable, documented tool.

## What's in here

| Project | What it does |
|---|---|
| [`playwright-event-verification`](playwright-event-verification) | Drives a public demo e-commerce site through login → checkout with Playwright, verifying each step's outcome against expectation |
| [`qa-report-generator`](qa-report-generator) | Turns a JSON list of test results into a styled, color-coded Pass/Fail Excel report |
| [`claude-code-skill-sample`](claude-code-skill-sample) | A packaged, reusable "skill" that combines the two above into a repeatable verification workflow |
| [`bot-handling-verification`](bot-handling-verification) | Verifies a fraud/bot-detection gate: bots are silently blocked (without tipping off the UI) and analytics events are tagged `is_bot`/`bot_kind`, while genuine visitors pass through unaffected |

Each folder has its own README with specifics, sample input/output, and —
for the Playwright project — a genuine failing check with an explanation,
not a cherry-picked all-green demo.

## Background

- **Quality Assurance Engineer II, Titan** (Oct 2022 – Present) — manual QA
  across web, Android, and iOS clients; test case authoring; event/analytics
  verification; release sign-off; and building internal automation tooling
  like the pattern shown in this repo.
- Previously: Testbook.com, CEDCOSS Pvt Ltd, WebieApp Solutions.

[LinkedIn](https://www.linkedin.com/in/shivank-gupta-6baa3885)
