# GitHub guide for beginners (5 members)

## One-time setup (everyone)
```bash
git config --global user.name  "Your Full Name"
git config --global user.email "the-email-you-used-on-github@example.com"   # must match GitHub!
```

## Repo owner (Amrin) — once
1. GitHub → **New repository** → name `aegis-flood-relief` → add README → Create.
2. *Settings → Collaborators* → add the other four by username.
3. *Settings → Branches → Add rule* for `main`: require a pull request before merging (1 approval).
4. Clone, and create your branch:
```bash
git clone https://github.com/<owner>/aegis-flood-relief.git
cd aegis-flood-relief
git checkout -b amrin
```

## Other members — once
```bash
git clone https://github.com/<owner>/aegis-flood-relief.git
cd aegis-flood-relief
git checkout -b fahim          # sadia / hamza / sunita
```

## Every week (the whole workflow)
```bash
git checkout main && git pull                 # 1. get the latest team work
git checkout <your-branch> && git merge main  # 2. bring it into your branch
# ... add/edit ONLY the files assigned to you in TEAM_PLAN.md ...
git add path/to/file1 path/to/file2           # 3. add specific files (not "git add .")
git commit -m "scoring: add priority rules"   # 4. small commit, clear message
git push -u origin <your-branch>              # 5. push (repeat 3-5 several times a week)
```
Then on GitHub: **Compare & pull request** → base `main` ← compare `<your-branch>` → assign your review buddy →
buddy clicks **Review → Approve** → you click **Merge pull request** (use *Create a merge commit*, so every commit stays credited).

## Commit message style
`area: what changed` — e.g. `resources: add plan_allocation function`, `ui: style request gauge`, `test: cover band edges`.

## Merge conflicts (rare — files are split by owner)
Only `base.html` / `settings.py` are shared, and both are Amrin's. If you need a change there, message Amrin or edit it
in a tiny separate commit. If Git says *CONFLICT*, open the file, keep both sides' meaning, delete the `<<<<<<<` markers,
then `git add <file>` and `git commit`.

## Running the project
```bash
python -m venv venv && source venv/bin/activate     # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo       # demo users + data (password: aegis1234)
python manage.py runserver       # http://127.0.0.1:8000
python manage.py test            # all tests must pass before opening a PR
```
Demo logins: `coord@aegis.test`, `volunteer@aegis.test`, `family@aegis.test`.
