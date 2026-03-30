# PawPal+ Project Reflection

## 1. System Design

### 1a. Initial Design

The system is built around five classes:

**`Pet`** — A dataclass representing the animal being cared for. Holds basic info (`name`, `species`, `age`) and a `special_needs` list for any health or behavioral considerations. It is a pure data container with no behavior.

**`Task`** — A dataclass representing a single care activity. Stores `title`, `duration_minutes`, `priority` ("low", "medium", "high"), and `completed` status. Has one behavior method: `is_high_priority()`, which encapsulates the priority check so callers don't compare strings directly.

**`Owner`** — Represents the person using the app. Holds `name`, `available_minutes` (the time budget for the day), and `preferences`. Also manages the task list via `add_task()` and `get_tasks()`. Tasks live on the Owner because they belong to the owner's routine, not to the scheduling algorithm.

**`Scheduler`** — The core logic class. Takes an `Owner` and a `Pet` and uses them to produce a `Plan`. `prioritize()` sorts tasks by priority, and `generate_plan()` selects and orders tasks that fit within the owner's time budget.

**`Plan`** — The output of the Scheduler. Holds `scheduled_tasks`, `skipped_tasks`, `total_minutes`, and a `reasons` dict mapping each task title to a short explanation of why it was included or skipped. `explain()` formats this for display; `display()` shows the full schedule.

### 1b. Design Changes

After reviewing the skeleton, two problems were found and fixed:

**1. Duplicate task ownership between `Owner` and `Scheduler`.**
The original `Scheduler.__init__` accepted its own `tasks: list[Task]` parameter separately from the `Owner`. This meant tasks added to the owner via `add_task()` would not automatically be seen by the scheduler — the caller would have to pass them in manually and keep both in sync.

*Fix:* Removed `tasks` from `Scheduler.__init__`. The scheduler now gets tasks from `owner.get_tasks()` at plan-generation time, so there is one source of truth.

**2. `Plan.explain()` had no data to explain.**
The original `Plan` only stored `scheduled_tasks` and `skipped_tasks`. `explain()` would have had no way to communicate *why* a task was chosen or skipped — just that it was.

*Fix:* Added a `reasons: dict[str, str]` field to `Plan`. The scheduler will populate this when building the plan (e.g., `"Morning walk": "high priority, fits in time budget"`), giving `explain()` real content to work with.

---

## 2. AI Collaboration

### 2a. How I used AI

AI (Claude via Claude Code) was used throughout the project as a design reviewer and code generator. Specific uses:

- **UML review** — asked AI to review the class skeleton for missing relationships and logic bottlenecks. It caught two real problems: duplicate task ownership between `Owner` and `Scheduler`, and `Plan.explain()` having no data to work with.
- **Algorithm suggestions** — used AI to identify weaknesses in the initial greedy scheduler (no start times, unused `frequency` field, no conflict detection) and to suggest what improvements would be most useful for a real pet owner.
- **Docstring generation** — used the "Generate documentation" smart action to add 1-line docstrings to all methods.
- **Streamlit wiring** — AI helped connect backend Scheduler methods to the UI, including surfacing conflict warnings before schedule generation.

### 2b. What I changed based on AI feedback

| AI suggestion | Accepted? | Reason |
|---|---|---|
| Remove `tasks` from `Scheduler.__init__` | Yes | Eliminated a sync bug — owner is now the single source of truth |
| Add `reasons` dict to `Plan` | Yes | Without it, `explain()` had nothing to say |
| Add `start_times` to `Plan` | Yes | Pet owners need clock times, not just task order |
| Add `detect_conflicts()` to `Scheduler` | Yes | Proactively warning > silently skipping tasks |
| Use `as-needed` frequency to exclude vet tasks | Yes | Made sense — some tasks shouldn't auto-schedule |

---

## 3. Testing

### 3a. What I tested

- `test_mark_complete_changes_status` — verifies the state transition from pending to done
- `test_add_task_increases_pet_task_count` — verifies pet task list grows correctly

### 3b. What I would test next

The scheduling algorithm itself has no tests yet. If I were to add more:

- **Scheduler fills time budget exactly** — a task that fits exactly should be scheduled, not skipped
- **Scheduler skips tasks that exceed remaining time** — even high-priority tasks should be skipped if they don't fit
- **`reset_daily_tasks()` only resets daily tasks** — weekly and as-needed tasks should stay completed
- **`detect_conflicts()` catches duplicate titles** — two pets with the same task name should trigger a warning

---

## 4. Reflection

### What went well

The separation of `Scheduler` from `Owner` and `Pet` made the logic easy to test and reason about. Generating the `Plan` as its own object (rather than printing directly) made it straightforward to display in both the terminal demo and the Streamlit UI without duplicating logic.

### What was harder than expected

`st.session_state` required a mental shift — Streamlit's stateless rerun model means objects get recreated unless explicitly stored. Understanding the "check before create" pattern (`if "owner" not in st.session_state`) was the key unlock for making the UI work correctly.

### What I would improve with more time

- Add tests for the scheduler algorithm
- Let the owner set a preferred start time (currently hardcoded to 8:00 AM)
- Support editing or removing tasks after they are added
- Add a "new day" button in the UI that calls `reset_daily_tasks()`
