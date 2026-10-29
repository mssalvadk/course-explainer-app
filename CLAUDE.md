# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A small Flask app that shows a list of courses and a detail page per course. There is no database; all course data is hardcoded in `src/models.py`.

## Commands

A virtual environment lives in `venv/` (gitignored). On Windows, activate it with `venv\Scripts\activate`; otherwise call `venv/Scripts/python` directly.

```bash
# Install dependencies (README uses uv; plain pip works too)
uv pip install -r requirements.txt

# Run the dev server (debug mode) at http://127.0.0.1:5000
python src/app.py

# Run all tests
python -m unittest discover -s tests

# Run one test
python -m unittest discover -s tests -k test_index
```

There is no linter or build step configured.

## Architecture

- **`src/app.py`**: creates the Flask app and registers routes with `app.add_url_rule()` instead of `@app.route` decorators. `app.py` does `from views import ...`, a flat import, so `src/` has to be on `sys.path`. Running `python src/app.py` handles that automatically. `tests/test_app.py` does it by inserting `src/` into `sys.path` before `from app import app`.
- **`src/views.py`**: plain functions that call `render_template` and know nothing about routing. If you add a view, register it in `app.py`. Endpoint names (`index`, `course`) are what the templates pass to `url_for`. `course` takes a 1-based integer id (`/course/<int:course_id>`) that indexes into `models.courses` and returns 404 when the id is out of range.
- **`src/models.py`**: a `Course` class with `title`, `description`, `instructor`, `duration`, and `topics` (a list of strings, default empty), plus a module-level `courses` list. `views.py` imports `courses` from here. To add a course, append to that list.
- **`src/templates/`**: Jinja2 templates. `layout.html` holds the site header/nav, the `<main class="container">` with a `content` block, and the footer. It is the only template with `<html>`/`<head>` boilerplate. `index.html` and `course.html` just `{% extends 'layout.html' %}` and fill `{% block content %}` (and optionally `{% block title %}`). `index.html` builds its course links from the `courses` list using `loop.index` as the id. `course.html` shows a "Topics Covered" list only when the course has topics.

## Development Workflow

### Add unit tests

Whenever you make changes, add unit tests, run them with `python -m unittest discover -s tests`, and make sure they pass.

### Verify UI changes with Playwright (mandatory)

**After any change that affects what a page renders (templates, views, styling), you MUST:**

1. Start the Flask app with `python src/app.py` if it isn't already running.
2. Use the Playwright MCP tool to open `http://127.0.0.1:5000`.
3. Navigate to and interact with the changed feature to verify it works.
4. Take a screenshot of the working feature.
5. Save it in the `test-output/` folder (gitignored) with a descriptive filename, e.g. `feature-name-verification-YYYY-MM-DD.png`.
6. Close the browser and stop the Flask server if you started it.

This ensures UI changes are visually verified and documents the working state of the app.
