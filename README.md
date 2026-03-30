# 🐾 PawPal+

**PawPal+** is a Streamlit app that helps a busy pet owner plan daily care tasks across multiple pets — automatically sorted, scheduled, and explained.

---

## 📸 Demo

<a href="/course_images/ai110/pawpal_screenshot.png" target="_blank"><img src='/course_images/ai110/pawpal_screenshot.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

---

## Features

- **Multi-pet support** — register multiple pets (dog, cat, or other) under one owner; tasks are tracked per pet and aggregated for scheduling
- **Priority-based sorting** — tasks are sorted high → medium → low before scheduling; within the same priority, shorter tasks are scheduled first to fit more into the day
- **Time-budget scheduling** — the owner sets a daily time budget (in minutes); the scheduler fits as many tasks as possible without exceeding it and explains what was skipped and why
- **Start-time display** — each scheduled task is assigned a real clock time (08:00, 08:30…) so the owner sees an actual timetable, not just a list
- **Task frequency** — tasks are tagged `daily`, `weekly`, or `as-needed`; `as-needed` tasks are excluded from automatic scheduling and shown separately; `daily` tasks can be reset for the next day
- **Conflict warnings** — before generating a plan, the scheduler checks for duplicate task names across pets and tasks that can never fit the time budget, surfacing actionable warnings in the UI
- **Filtering** — tasks can be filtered by pet or completion status, making it easy to see only what's relevant
- **Reasoning** — every scheduled and skipped task includes a plain-language explanation of why it was included or left out

---

## Getting Started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the app

```bash
streamlit run app.py
```

### Run the terminal demo

```bash
python main.py
```

---

## Testing PawPal+

```bash
python -m pytest
```

### What the tests cover

- **Task completion** — verifies that `mark_complete()` flips `completed` from `False` to `True`
- **Pet task addition** — verifies that `add_task()` increases a pet's task count correctly

### Confidence Level

★★★☆☆ (3/5)

Core data operations are verified and reliable. Confidence is limited because the scheduling algorithm — priority sorting, time-budget fitting, conflict detection, and recurring task reset — has no automated tests yet.

---

## Smarter Scheduling

The scheduler goes beyond a simple priority sort with four improvements:

- **Start-time tracking** — each scheduled task is assigned a real clock time based on a configurable day start. `Plan.display()` shows the full timetable.
- **Filtering** — tasks can be filtered by pet name (`Owner.get_tasks_for_pet()`) or completion status (`Owner.get_tasks_by_status()`, `Pet.filter_tasks()`).
- **Recurring task support** — tasks carry a `frequency` field (`daily`, `weekly`, `as-needed`). `as-needed` tasks are excluded from auto-scheduling. `Scheduler.reset_daily_tasks()` resets daily tasks for the next day.
- **Conflict detection** — `Scheduler.detect_conflicts()` runs before scheduling and flags duplicate task titles and tasks that can never fit the time budget.

---

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan
