# Priority Scoring

Every relief request gets an automatic **priority score** when it is saved, so the most urgent cases rise to the top of the coordinator's queue.

Code: `reliefrequests/scoring.py` · Tests: `reliefrequests/tests.py`

## Scoring rules

| Condition | Points |
|---|---|
| Medical emergency | +5 |
| No food or water at hand | +4 |
| More than 50 people affected | +3 |
| Children or elderly present | +2 |
| None of the above (normal request) | 1 |

- Points add up. The highest possible score is **14**.
- Exactly 50 people does **not** count as large; it must be 51 or more.

## Severity bands

| Score | Band | Meaning |
|---|---|---|
| 8 – 14 | **Critical** | Handled first |
| 5 – 7 | **High** | Moves up quickly |
| 3 – 4 | **Medium** | Served as stock allows |
| 1 – 2 | **Low** | Served after higher bands |

## Worked examples

| Request | Calculation | Score | Band |
|---|---|---|---|
| No water, 60 people, children present | 4 + 3 + 2 | 9 | Critical |
| Medical emergency only | 5 | 5 | High |
| Medical emergency + no food/water | 5 + 4 | 9 | Critical |
| 51 people, nothing else | 3 | 3 | Medium |
| 50 people, nothing else | — | 1 | Low |
| Normal request | — | 1 | Low |

## Where the score is used
- **Request form:** the live water-level gauge previews the score as the family fills in the form.
- **Coordinator dashboard:** the request queue is sorted by score, highest first.
- **Allocation:** stock is given to higher-scoring requests first.
- **Reports page:** requests are counted by band in the "By priority" chart.