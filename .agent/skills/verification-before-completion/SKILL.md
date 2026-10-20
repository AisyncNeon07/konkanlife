---
name: verification-before-completion
description: Use to thoroughly verify and validate work before marking tasks as complete
---

# Verification Before Completion

## Overview

Always verify changes thoroughly before declaring a task finished. Never assume an edit worked without direct verification.

## Verification Checklist

### 1. Code Syntax & Linting
- Ensure all Python files compile cleanly without syntax errors:
  `python -m py_compile <changed_file.py>`
- Check for missing imports or undefined variables.

### 2. Automated Tests & Migrations
- Run Django system checks:
  `python manage.py check`
- Check migration state:
  `python manage.py showmigrations`
- Run the test suite:
  `python manage.py test` or `pytest`

### 3. Manual / Integration Checks
- Verify templates render properly with required context variables.
- Verify static assets (Tailwind CSS, JS) compile and load.
- Check edge cases (empty states, invalid inputs, unauthenticated requests).

### 4. Clean Workspace
- Ensure no temporary scratch files, debug print statements, or unintended diffs remain.
