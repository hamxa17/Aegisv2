# Aegis — Team Plan

Team 2 · CSE302 · Project window: 8–23 October 2026

## Members and ownership

| # | Member | Feature area | Main files | Lines |
|---|---|---|---|---|
| 1 | Sunita Bhowmik (26101901) | Accounts and roles | `manage.py`, `requirements.txt`, `.gitignore`, `aegis/` (settings, urls, wsgi), `accounts/` (models, forms, views, decorators, urls, migration), `templates/base.html`, `templates/_field.html`, `static/css/base.css`, `static/js/main.js`; profile and photo pages | 329 (22%) |
| 2 | Sadia Afrin Chowdhury (24101131) | Relief requests and priority | `reliefrequests/` (models, scoring, forms, views, urls, tests, migration), `templates/relief/`, `templates/accounts/login.html` and `register.html`, `static/css/forms.css`, `static/js/gauge.js`, `docs/SCORING.md`, `docs/TEST_REPORT_RELIEF.md` | 337 (22%) |
| 3 | Mohammad Hamza Adnan Ahmed (24101135) | Resources and allocation | `resources/` (models, allocation engine, views, urls, tests, migration), `templates/resources/`, `static/css/resources.css`, `static/js/resources.js`, `coordination/tests.py`, `volunteers/tests.py`, `docs/ALLOCATION.md`, `docs/GIT_GUIDE.md`, `docs/DEPLOYMENT.md` | 325 (21%) |
| 4 | MD Ferdous Islam Fahim (24101129) | Verification, volunteers and delivery | `coordination/` (verify, reject, assign), `volunteers/` (tasks, delivery), `templates/volunteers/tasks.html`, `static/js/queue.js`, `docs/COORDINATOR_GUIDE.md` | 199 (13%, lighter share by team agreement) |
| 5 | Amrin Haider (24101115) | Dashboard, reports and quality | `templates/coordination/dashboard.html`, `static/css/dashboard.css`, `templates/volunteers/reports.html`, landing page (`templates/index.html`, `static/css/landing.css`, `static/js/landing.js`, `aegis/views.py`), `resources/management/commands/seed_demo.py`, `accounts/tests.py`, photos app, `README.md`, `docs/TEAM_PLAN.md` | 333 (22%) |

Line counts are taken from the original project files.

## Shared files

`coordination/views.py`, `volunteers/views.py` and `volunteers/urls.py` contain both Fahim's code (approve/reject, assign, tasks, delivery) and Amrin's code (dashboard statistics, reports). Fahim pushes these whole files so nobody overwrites anyone else.

## Ground rules

- Push only the files listed under your name.
- One file or feature per commit, with a clear message (`area: what changed`).
- Run `git pull` before you start and `git pull --rebase` before every push.
- Commit with the same email as your GitHub account, so the contributions count.
- Never push to someone else's files. Ask the owner or open a pull request.

## Pull request reviews

Sunita reviews Sadia, Sadia reviews Hamza, Hamza reviews Fahim, Fahim reviews Amrin, Amrin reviews Sunita.

## Documentation

See the Docs table in `README.md`. How to use Git: `docs/GIT_GUIDE.md`.
