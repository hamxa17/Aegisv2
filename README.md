# Aegis — Flood Relief Coordination

A Django web platform that connects flood-affected families, volunteers and coordinators so urgent requests
are prioritized and limited food, water, medicine and blankets go where they matter most.
Built by **Team 2 · CSE302**.

## Features
- Role-based accounts: affected family · volunteer · coordinator
- Relief requests with an **automatic priority score** (medical +5, no food/water +4, >50 people +3, children/elderly +2)
- Live **water-level gauge** on the request form showing how the request will be triaged
- Coordinator verification, volunteer assignment and delivery tracking
- Resource stock with **priority-first allocation** and shortage reporting
- Reports and statistics

## Stack
Django · Python · SQLite · HTML · CSS · JavaScript (no external services)

## Run it
```bash
pip install -r requirements.txt
python manage.py migrate && python manage.py seed_demo
python manage.py runserver
```
Demo logins (password `aegis1234`): `coord@aegis.test`, `volunteer@aegis.test`, `family@aegis.test`.
Coordinators are created via `python manage.py createsuperuser` or the admin — public sign-up only offers family/volunteer.

## Team & ownership
| Member | Area |
|---|---|
| Amrin Haider (24101115) | Project setup, accounts, base layout |
| MD Ferdous Islam Fahim (24101129) | Relief requests, priority scoring, gauge |
| Sadia Afrin Chowdhury (24101131) | Coordinator dashboard, verification, assignment |
| Mohammad Hamza Adnan Ahmed (24101135) | Resources, allocation engine, demo data |
| Sunita Bhowmik (26101901) | Volunteers, reports, landing page, docs |

See `docs/TEAM_PLAN.md` and `docs/GIT_GUIDE.md`.
