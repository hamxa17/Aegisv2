# Git guide for the Aegis team

Repository: https://github.com/hamxa17/Aegisv2

## One-time setup (everyone)
```
git config --global user.name  "Your Full Name"
git config --global user.email "the-email-you-use-on-github@example.com"
git clone https://github.com/hamxa17/Aegisv2.git
cd Aegisv2
```
The email **must match your GitHub account**, otherwise your commits are not credited to you.

## Every working session
```
git switch main
git pull origin main --no-edit        # get the team's latest work
# ... work only on the files listed under your name in TEAM_PLAN.md ...
git status                            # check: only your files appear
git add path/to/file                  # never use "git add ."
git commit -m "area: what changed"
git pull --rebase                     # before every push
git push origin main
```
If `main` is protected, work on your own branch (`git switch -c YourName`), push it with `git push origin YourName`, then open a pull request on GitHub and ask your review buddy to approve it. Do not delete your branch after merging.

## Commit messages
`area: what changed`, for example `views: add submit_request`, `style: add gauge styles`, `test: cover band edges`.

## Rules
1. Push only the files listed under your name in `docs/TEAM_PLAN.md`.
2. Never use `git push --force`.
3. One file or feature per commit. Aim for about 8–10 commits each.
4. Read `git status` before every commit.

## Running the project
```
python -m venv venv
venv\Scripts\activate                 # Mac/Linux: source venv/bin/activate
pip install -r requirements.txt       # installs Django and Pillow
python manage.py migrate
python manage.py seed_demo            # demo users and data (password: aegis1234)
python manage.py runserver            # http://127.0.0.1:8000
python manage.py test                 # all tests must pass before you push
```
Demo logins: `coord@aegis.test`, `volunteer@aegis.test`, `family@aegis.test`. Uploaded photos go to the `media/` folder, which is not pushed to GitHub.

## Common problems
| Problem | Fix |
|---|---|
| `rejected ... fetch first` | `git pull --rebase`, then push again |
| `CONFLICT` after a pull | Don't commit. Run `git status` and ask the file's owner |
| A text editor (vim) opens | Press `Esc`, type `:wq`, press `Enter` |
| Wrong file staged | `git restore --staged path/to/file` |
| `ModuleNotFoundError` when running | Pull the latest `main` and run `pip install -r requirements.txt` |
