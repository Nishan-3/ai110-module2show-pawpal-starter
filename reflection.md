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
