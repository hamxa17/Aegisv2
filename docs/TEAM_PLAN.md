# Aegis — 4-Week Team Plan (5 members, equal contribution)

Repo: one `main` branch (GitHub's name for "master") + one personal branch per member.
Every member owns **one Django app, one CSS file, one JS file, one test file and one doc** — so the GitHub
contributor graph shows an even split of files, lines and commits.

| Member | Branch | Owns (backend) | Owns (front end) | Owns (docs) |
|---|---|---|---|---|
| **Amrin Haider** | `amrin` | `aegis/` project config, `accounts/` (login, register, roles) | `base.html`, `base.css`, `main.js`, login/register templates | `docs/DEPLOYMENT.md` |
| **MD Ferdous Islam Fahim** | `fahim` | `reliefrequests/` (model, **priority scoring**, submit form, my-requests) | `request_form.html`, `my_requests.html`, `forms.css`, `gauge.js` | `docs/SCORING.md` |
| **Sadia Afrin Chowdhury** | `sadia` | `coordination/` (verify / reject / assign, coordinator dashboard) | `coordination/dashboard.html`, `dashboard.css`, `queue.js` | `docs/COORDINATOR_GUIDE.md` |
| **Mohammad Hamza Adnan Ahmed** | `hamza` | `resources/` (stock, **allocation engine**, shortage, seed command) | `resources.html`, `resources.css`, `resources.js` | `docs/ALLOCATION.md` |
| **Sunita Bhowmik** | `sunita` | `volunteers/` (assignments, delivery, reports) | `index.html` (landing), `landing.css`, `landing.js`, `tasks.html`, `reports.html` | `README.md` |

## Weekly schedule (what each person pushes)

Rule: **at least 3 commits per person per week**, pushed to your own branch, then one Pull Request into `main`
(opened by Friday, reviewed by your review buddy, merged by the PR author).

### Week 1 — Foundation (merge order matters: Amrin first, same day, then the rest)
| Member | Push these | Suggested commits |
|---|---|---|
| Amrin | `manage.py`, `requirements.txt`, `.gitignore`, `aegis/` (settings, urls, wsgi, views), `static/css/base.css`, `static/js/main.js`, `templates/base.html`, `templates/_field.html` | 1 project skeleton · 2 settings + urls · 3 base layout + CSS |
| Fahim | `reliefrequests/` `__init__`, `apps.py`, **`scoring.py`**, `models.py`, `admin.py`, `tests.py` | 1 scoring rules · 2 model · 3 scoring tests |
| Sadia | `coordination/` `__init__`, `apps.py` + empty `urls.py` stub; `static/css/dashboard.css` | 1 app skeleton · 2 stats/table CSS · 3 badges + timeline CSS |
| Hamza | `resources/` `__init__`, `apps.py`, `models.py`, **`allocation.py`**, `admin.py`, `tests.py` | 1 models · 2 allocation function · 3 allocation tests |
| Sunita | `volunteers/` `__init__`, `apps.py`, `models.py`, `admin.py`; `static/css/landing.css`; `templates/index.html` | 1 Assignment model · 2 landing CSS · 3 landing page |

### Week 2 — Core features
| Member | Push these | Suggested commits |
|---|---|---|
| Amrin | `accounts/` (`models`, `forms`, `views`, `urls`, `decorators`, `admin`, `migrations`), `templates/accounts/login.html`, `register.html` | 1 User model · 2 forms + views · 3 templates + role decorator |
| Fahim | `reliefrequests/forms.py`, `views.py` (submit), `urls.py`, `templates/relief/request_form.html`, `static/css/forms.css`, `static/js/gauge.js` | 1 form · 2 submit view · 3 form page · 4 water-level gauge |
| Sadia | `coordination/views.py` (dashboard, review, assign), `urls.py`, `templates/coordination/dashboard.html`, `static/js/queue.js` | 1 dashboard view · 2 verify/reject · 3 assign · 4 template + filter JS |
| Hamza | `resources/views.py`, `urls.py`, `templates/resources/resources.html`, `static/css/resources.css`, `static/js/resources.js` | 1 list view · 2 update stock · 3 recalc button · 4 template + CSS |
| Sunita | `volunteers/views.py` (tasks, mark_delivered), `urls.py`, `templates/volunteers/tasks.html`, `static/js/landing.js` | 1 tasks view · 2 delivery view · 3 tasks page · 4 count-up + confirm JS |

### Week 3 — Integration & tracking
| Member | Push these |
|---|---|
| Amrin | `accounts/tests.py`; role-aware navbar polish in `base.html`; `home_redirect` routing; Django messages styling; run migrations on a clean DB and fix conflicts |
| Fahim | `my_requests` view + `templates/relief/my_requests.html` (stats + status timeline); validation messages |
| Sadia | `coordination/tests.py`; shortage card on dashboard; call allocation after verify; empty states |
| Hamza | `resources/management/commands/seed_demo.py` (demo data); `consume()` stock deduction on delivery; shortage summary |
| Sunita | `reports` view + `templates/volunteers/reports.html`; `volunteers/tests.py`; mobile-responsive checks on landing |

### Week 4 — Testing, polish, documentation, release
| Member | Push these |
|---|---|
| Amrin | `docs/DEPLOYMENT.md` (env vars, `DEBUG=0`, hosting); security pass (CSRF, role guards); tag `v1.0` after all PRs merged |
| Fahim | `docs/SCORING.md` (rules, worked examples, test table); edge-case fixes; screenshots of the request page |
| Sadia | `docs/COORDINATOR_GUIDE.md`; accessibility pass (labels, contrast, keyboard); screenshots of dashboard |
| Hamza | `docs/ALLOCATION.md` (priority-first algorithm, 500 vs 650 water example); performance check with 500 seeded requests |
| Sunita | `README.md` (setup, screenshots, team table); presentation demo script; final cross-browser check |

## Review buddies (everyone reviews exactly one PR per week)
Amrin → Fahim → Sadia → Hamza → Sunita → Amrin.

## Dependencies you must respect
`accounts` (Amrin) is needed by everyone → merge first. `reliefrequests` models are imported by `resources`, `volunteers`
and `coordination` → Fahim merges Week 1 PR second. Everyone else can merge in any order after that.

## Equal-contribution checklist (check every Friday)
- GitHub → *Insights → Contributors*: all 5 names present, commit counts within ~20% of each other.
- Each member has ≥ 1 merged PR and ≥ 1 PR review per week.
- Commits use the member's own name and the **same email as their GitHub account** (otherwise GitHub will not credit them).
- Nobody commits another person's work from their laptop. If you pair, add `Co-authored-by:` to the commit message.

## Scope note
Your slides mention both "Aegis" (requests, priority, resources, volunteers) and an older "Ashroy" concept (shelters, supply cycles,
duplicate-family flags, 8-class diagram). This codebase implements **Aegis**. If your instructor expects shelters/duplicates, add them
as a Week 4 stretch: `shelters` app (Hamza), `DuplicateFlag` (Fahim), shelter-assignment score (Sadia) — and update the class diagram.
