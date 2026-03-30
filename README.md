# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Testing PawPal+

Run the test suite with:

```bash
python -m pytest
```

### What the tests cover

- **Task completion** — verifies that `mark_complete()` flips `completed` from `False` to `True`
- **Pet task addition** — verifies that `add_task()` increases a pet's task count correctly

### Confidence Level

★★★☆☆ (3/5)

The core data operations (adding tasks, marking completion) are verified and reliable. Confidence is limited because the scheduling algorithm itself — priority sorting, time-budget fitting, conflict detection, and recurring task reset — has no tests yet. Edge cases like zero available time, all tasks skipped, or duplicate pet names are untested.

---

## Smarter Scheduling

The scheduler goes beyond a simple priority sort with four improvements:

- **Start-time tracking** — each scheduled task is assigned a real clock time (e.g. 08:00, 08:30) based on a configurable day start. `Plan.display()` shows the full timetable.
- **Filtering** — tasks can be filtered by pet name (`Owner.get_tasks_for_pet()`) or completion status (`Owner.get_tasks_by_status()`, `Pet.filter_tasks()`), making it easy to view just what's relevant.
- **Recurring task support** — tasks carry a `frequency` field (`daily`, `weekly`, `as-needed`). `as-needed` tasks are excluded from automatic scheduling. `Scheduler.reset_daily_tasks()` resets daily tasks at the start of each new day so they appear again tomorrow.
- **Conflict detection** — `Scheduler.detect_conflicts()` runs before scheduling and flags duplicate task titles across pets and tasks whose duration exceeds the owner's entire time budget (tasks that could never be scheduled).
