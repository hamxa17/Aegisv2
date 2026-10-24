# Resource allocation

Owner: Hamza · app: `resources/` · code: `resources/allocation.py`

## What it does

Aegis never has enough relief supplies for everyone, so stock is handed out in **priority order**: the most urgent
requests are served first, and only what is left goes to the less urgent ones. Requests with the same priority are
served in the order they were made (oldest first).

## Inputs

| Input | Where it comes from |
|---|---|
| Stock per resource (food, water, medicine, blankets) | `Resource.stock`, edited on the Resources page |
| Open requests | `ReliefRequest` rows with status `verified` or `assigned` |
| Priority order | `ReliefRequest.Meta.ordering = ["-priority_score", "created_at"]` (score rules are in `docs/SCORING.md`) |

## Algorithm (priority-first)

For each resource, independently:

1. Take all open requests for that need type, already sorted by priority score (high to low), then by age.
2. Start with `left = stock`.
3. For each request in that order: `given = min(requested, left)`, then `left = left - given`.
4. Save an `Allocation(request, resource, quantity=given)` row for every request that received something.

`plan_allocation(demands, stock)` is the pure function that does steps 2-3. It knows nothing about the database, so
it is easy to test. `run_allocation()` wraps it: it clears old allocations and rebuilds them inside one database
transaction, so the plan is never left half-written.

## Worked example: 500 bottles of water

| Priority | Requested | Given | Left after |
|---|---|---|---|
| Critical | 200 | 200 | 300 |
| High | 150 | 150 | 150 |
| Medium | 300 | 150 | 0 |

Total demand is 650 against 500 in stock, so **150 are short**, and all of the shortage falls on the lowest-priority
request. Critical and High requests are fully served.

## Shortage

`summary()` returns, for each resource, the total open demand and `shortage = max(demand - stock, 0)`. The Resources
page shows "covered" or "short N" from this, and the coordinator dashboard uses it for the stock-vs-demand card.

## Delivery

When a volunteer marks a request delivered, `consume(request)` removes that request's allocated quantity from stock
(never below zero).

## How it is triggered

- Coordinator presses **Recalculate allocation** on the Resources page, which runs `run_allocation()`.
- It is also run after a request is verified.

## Tests

`resources/tests.py` covers the proposal's water example (the table above) and a database test showing that a
Critical request beats an older Low request and that shortage is reported correctly. Run them with:

```bash
python manage.py test resources
```
