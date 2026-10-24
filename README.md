# Aegis — Flood Relief Coordination

A Django web platform that connects flood-affected families, volunteers and coordinators so urgent requests
are prioritized and limited food, water, medicine and blankets go where they matter most.
Built by **Team 2 · CSE302**.

## Features
- Role-based accounts: affected family · volunteer · coordinator, with a profile page
- Relief requests with an **automatic priority score** (medical +5, no food/water +4, >50 people +3, children/elderly +2)
- Live **water-level gauge** on the request form showing how the request will be triaged
- **Request photos** (media CRUD): attach a photo to a request, view the gallery, edit or delete photos
- Coordinator verification, volunteer assignment and delivery tracking
- Resource management (add, edit, delete, restock) with **priority-first allocation** and shortage reporting
- Coordinator dashboard, reports and live statistics on the home page

## Stack
Django · Python · Pillow · SQLite · HTML · CSS · JavaScript (no external services)

## Apps
| App | Models | Purpose |
|---|---|---|
| `accounts` | User | Sign up, log in, profile, role-based access |
| `reliefrequests` | ReliefRequest | Request form, priority scoring, My requests |
| `resources` | Resource, Allocation | Resource CRUD, stock, allocation engine, demo data |
| `volunteers` | Assignment | Volunteer tasks, mark delivered, reports |
| `coordination` | — | Coordinator dashboard: verify, reject, assign |
| `photos` | RequestPhoto | Upload, view, edit and delete request photos |

## Run it
```bash
pip install -r requirements.txt        # installs Django and Pillow
python manage.py migrate && python manage.py seed_demo
python manage.py runserver
```
Open http://127.0.0.1:8000/. Uploaded photos are saved in the `media/` folder (not pushed to GitHub).

Demo logins (password `aegis1234`): `coord@aegis.test`, `volunteer@aegis.test`, `family@aegis.test`.
Coordinators are created via `python manage.py createsuperuser` or the admin — public sign-up only offers family/volunteer.

## Tests
```bash
python manage.py test
```
38 tests cover accounts, scoring, allocation, the coordinator and volunteer flows, and photo CRUD.

## Team & ownership
| Member | Area |
|---|---|
| Sunita Bhowmik (26101901) | Accounts, sign-up and login, profile, photo pages |
| Sadia Afrin Chowdhury (24101131) | Relief requests, priority scoring, gauge |
| Mohammad Hamza Adnan Ahmed (24101135) | Resources, allocation engine |
| MD Ferdous Islam Fahim (24101129) | Verification, volunteer tasks |
| Amrin Haider (24101115) | Dashboard, reports, home page stats, demo data, tests, photos app |

## Docs
Everything in the `docs/` folder:

| File | What it covers |
|---|---|
| `TEAM_PLAN.md` | Who does what, and the work split |
| `GIT_GUIDE.md` | How the team pulls, commits and pushes |
| `SCORING.md` | How the priority score is calculated |
| `ALLOCATION.md` | How stock is shared out, most urgent first |
| `COORDINATOR_GUIDE.md` | How coordinators use the dashboard, resources and photos |
| `DEPLOYMENT.md` | Steps for running the site on a server |
| `TEST_REPORT_RELIEF.md` | Test results for the relief request feature |
| `screenshots/` | Screenshots of the request form and My requests page |
