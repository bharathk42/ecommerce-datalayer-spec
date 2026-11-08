# ecommerce-datalayer-spec

A vendor-neutral e-commerce data layer specification aligned to GA4's recommended ecommerce events, with a JSON Schema and a small validator so dev teams and analysts can agree on the contract before a single tag fires.

This is a generic template I use as a starting point. It contains no client data.

## Why

Most tracking bugs aren't tag bugs. They're contract bugs: a missing `currency`, a price sent as a string, an `item_id` that changes between `view_item` and `purchase`. Writing the contract down and validating against it catches these in UAT instead of in a revenue report.

## Files

| File | Purpose |
|---|---|
| `SPEC.md` | Event-by-event spec: when it fires, required fields, example payload |
| `datalayer.schema.json` | JSON Schema (draft 2020-12) for every event in the spec |
| `validate.py` | Validates a JSON file of captured `dataLayer` pushes against the schema |
| `sample-events.json` | Example pushes, including two intentional failures |

## Run it

```bash
pip install jsonschema
python validate.py sample-events.json
```

Output:

```
[PASS] #0 view_item
[PASS] #1 add_to_cart
[PASS] #2 begin_checkout
[PASS] #3 purchase
[FAIL] #4 purchase -> ecommerce.value: '149.99' is not of type 'number'
[FAIL] #5 add_to_cart -> ecommerce: 'currency' is a required property
4 passed, 2 failed
```

## Design choices

- **`new_customer` is a tri-state** (`true` / `false` / `not_specified`), not a boolean. Ad platforms treat "unknown" differently from "returning", and a boolean forces a guess. Keeping the lookback window (e.g. 12 months vs 540 days) out of the front end lets marketing change it without a code release.
- **Money is always a number** with a separate ISO 4217 `currency`.
- **`items[]` is identical across the funnel**, so you can join `view_item` to `purchase` on `item_id`.
- **Always clear `ecommerce` before a push** (`dataLayer.push({ ecommerce: null })`) to avoid GTM merging stale items into the next event.
