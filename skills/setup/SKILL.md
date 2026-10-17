---
name: setup
description: Initializes a Bottega project by creating the docs/ structure and STATUS.md, a secure .gitignore, and (if wanted) a git repository. Use once at the start of a new project.
argument-hint: "[project name]"
---

# Project setup

1. Check the current directory. If `docs/STATUS.md` already exists, stop and tell the user: the project is already set up.
2. Ask the user with AskUserQuestion, in a single call:
   - **Project name**, if it isn't in `$ARGUMENTS`
   - **Git:** initialize a repository if there isn't one? (Recommended: yes)
   - **Automatic commits:** commit at the end of each slice? (Recommended: yes, locally, without pushing)
   - **User profile:** experience level, and the languages and technologies they know. The architect uses this to make suitable choices.
3. Create the structure and copy the status template:
   ```bash
   mkdir -p docs/adr docs/reviews
   cp "${CLAUDE_PLUGIN_ROOT}/templates/STATUS.md" docs/STATUS.md
   ```
   Don't copy the other documents (`01-vision.md`, `02-requirements.md`…) now: each agent creates its own from its template when its phase arrives.
4. Fill in `docs/STATUS.md`: project name, today's date, phase `P1 Idea`, git preferences and user profile.
5. If the user wants git and there is no repository, run `git init`. Create or extend `.gitignore` with at least:
   ```
   .env
   .env.*
   !.env.example
   *.pem
   *.key
   *.p12
   secrets/
   .DS_Store
   ```
6. Check which security tools are installed, and record the missing ones in `docs/STATUS.md` with the command to install each:
   ```bash
   for t in git docker gitleaks semgrep trivy osv-scanner; do command -v "$t" >/dev/null && echo "OK  $t" || echo "--  $t"; done
   ```
   Don't install anything without the user's consent.
7. Confirm to the user what was created and state the next step: `/bottega:idea` or `/bottega:start`.
