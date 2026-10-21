# Result Schema

Every check recorded by a verification run (Playwright or otherwise) should
be a JSON object with this shape, matching what
[`qa-report-generator/report_generator.py`](../../qa-report-generator/report_generator.py)
expects as input:

```json
{
  "name": "Checkout: checkout_completed event fires",
  "category": "Event Verification",
  "status": "pass",
  "expected": "checkout_completed event fires with order_total",
  "actual": "Event fired with order_total=42.50",
  "notes": ""
}
```

| Field      | Required | Notes                                                                 |
|------------|----------|------------------------------------------------------------------------|
| `name`     | yes      | Short, specific — should read like a test case title                  |
| `category` | yes      | Groups related checks in the report (Functional, Event Verification, Regression, Security, ...) |
| `status`   | yes      | `"pass"` or `"fail"` — lowercase                                       |
| `expected` | yes      | What should have happened, stated concretely (not "it should work")   |
| `actual`   | yes      | What was actually observed — the evidence, not a summary of it         |
| `notes`    | no       | Use this for anything a reader needs to not misread the result — e.g. flagging that a failure is a wrong assumption in the check itself, not a product defect |

Keeping `expected` and `actual` as concrete, evidence-based strings (not
"works" / "doesn't work") is what makes the generated report useful on its
own, without needing to re-run the check to understand what happened.
