# QA Report Generator

A small Python tool that turns a JSON list of test/verification results into
a styled, color-coded Pass/Fail Excel report — no manual spreadsheet upkeep.

This is a generic, standalone version of a reporting pipeline pattern I use
day-to-day in manual and automated QA work: run a batch of checks, dump the
raw results, and have a script produce the report a team actually reads,
instead of hand-formatting a spreadsheet after every test cycle.

## What it does

- Takes a JSON file of results (`name`, `category`, `status`, `expected`,
  `actual`, `notes` per test case)
- Computes a summary (total / passed / failed / pass rate)
- Writes an `.xlsx` report with:
  - A summary block at the top
  - One row per test case, color-coded green (pass) / red (fail)
  - Frozen header row, sized columns, wrapped text for readability

## Usage

```bash
pip install -r requirements.txt
python report_generator.py sample_results.json sample_output/report.xlsx
```

See [`sample_output/report.xlsx`](sample_output/report.xlsx) for an example
of the generated report, built from [`sample_results.json`](sample_results.json).

## Why this exists

In real QA work, the input to this script is usually produced by an
automated test run (see [`../playwright-event-verification`](../playwright-event-verification))
or a batch of manually-executed test cases. Separating "run the checks" from
"produce the report" keeps the reporting format consistent regardless of
what produced the results, and means the report never silently drifts out
of date with the underlying data — it's regenerated from source every time.
