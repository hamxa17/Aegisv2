# Test report - Relief Requests and Priority (Sadia)

Date run: __24/10/2026__
Branch tested: `main`

## Command
```
python manage.py test reliefrequests -v 2
```

## Result
Ran 38 tests in 54.226s

OK

## What is covered
| Area | Tests |
|---|---|
| Scoring rules | proposal example (9, Critical), baseline (1, Low), band edges, "50 is not large" |
| Model | priority calculated on save, highest priority listed first |
| Submit view | family can submit, zero people rejected, coordinator blocked (403) |
| My requests view | a family only sees its own requests |

## Manual checks done
- [ x ] Water-level gauge rises and changes colour while ticking boxes
- [ x ] Submitting redirects to "My requests" with a success message
- [ x ] Priority badge matches the score shown in the form
- [ x ] Timeline shows the correct step for each status
