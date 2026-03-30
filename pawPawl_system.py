from dataclasses import dataclass, field


@dataclass
class Pet:
    name: str
    species: str
    age: int
    special_needs: list[str] = field(default_factory=list)
    tasks: list["Task"] = field(default_factory=list)

    def add_task(self, task: "Task") -> None:
        """Add a care task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> list["Task"]:
        """Return all tasks assigned to this pet."""
        return self.tasks

    def get_pending_tasks(self) -> list["Task"]:
        """Return only incomplete tasks for this pet."""
        return [t for t in self.tasks if not t.completed]

    def filter_tasks(self, status: str = "all") -> list["Task"]:
        """Filter tasks by status: 'pending', 'completed', or 'all'."""
        if status == "pending":
            return [t for t in self.tasks if not t.completed]
        if status == "completed":
            return [t for t in self.tasks if t.completed]
        return self.tasks


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str             # "low", "medium", "high"
    frequency: str = "daily"  # "daily", "weekly", "as-needed"
    completed: bool = False

    def is_high_priority(self) -> bool:
        """Return True if this task has high priority."""
        return self.priority == "high"

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def reset(self) -> None:
        """Reset completion status (used for recurring daily tasks)."""
        self.completed = False


class Owner:
    def __init__(self, name: str, available_minutes: int, preferences: list[str] = None):
        self.name = name
        self.available_minutes = available_minutes
        self.preferences = preferences or []
        self._pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this owner."""
        self._pets.append(pet)

    def get_pets(self) -> list[Pet]:
        """Return all pets belonging to this owner."""
        return self._pets

    def get_all_tasks(self) -> list[Task]:
        """Return all tasks across all pets."""
        return [task for pet in self._pets for task in pet.get_tasks()]

    def get_all_pending_tasks(self) -> list[Task]:
        """Return all incomplete tasks across all pets."""
        return [task for pet in self._pets for task in pet.get_pending_tasks()]

    def get_tasks_for_pet(self, pet_name: str) -> list[Task]:
        """Return all tasks belonging to a specific pet by name."""
        for pet in self._pets:
            if pet.name == pet_name:
                return pet.get_tasks()
        return []

    def get_tasks_by_status(self, completed: bool) -> list[Task]:
        """Return all tasks across pets filtered by completion status."""
        return [t for t in self.get_all_tasks() if t.completed == completed]


@dataclass
class Plan:
    scheduled_tasks: list[Task] = field(default_factory=list)
    total_minutes: int = 0
    skipped_tasks: list[Task] = field(default_factory=list)
    reasons: dict[str, str] = field(default_factory=dict)       # task title -> reason
    start_times: dict[str, int] = field(default_factory=dict)   # task title -> start minute
    conflicts: list[str] = field(default_factory=list)          # conflict warning messages

    def explain(self) -> str:
        """Return a human-readable explanation of why each task was scheduled or skipped."""
        lines = []
        for task in self.scheduled_tasks:
            lines.append(f"  ✓ {task.title}: {self.reasons[task.title]}")
        for task in self.skipped_tasks:
            lines.append(f"  ✗ {task.title}: {self.reasons[task.title]}")
        return "\n".join(lines)

    def display(self) -> str:
        """Return a formatted schedule with start times for each task."""
        lines = [f"{'─'*42}", "  TIME   TASK                       DURATION", f"{'─'*42}"]
        for task in self.scheduled_tasks:
            start = self.start_times.get(task.title, 0)
            h, m = divmod(start, 60)
            time_str = f"{h:02d}:{m:02d}"
            lines.append(f"  {time_str}  {task.title:<28} {task.duration_minutes} min")
        lines.append(f"{'─'*42}")
        return "\n".join(lines)


class Scheduler:
    PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

    def __init__(self, owner: Owner, day_start_minute: int = 480):
        self.owner = owner
        self.day_start_minute = day_start_minute  # default: 8:00 AM (480 min from midnight)

    def prioritize(self) -> list[Task]:
        """Sort pending, non-as-needed tasks by priority (high first), then duration (shortest first)."""
        tasks = self.owner.get_all_pending_tasks()
        # Filter out as-needed tasks (only schedule if explicitly included)
        tasks = [t for t in tasks if t.frequency != "as-needed"]
        return sorted(tasks, key=lambda t: (self.PRIORITY_ORDER.get(t.priority, 99), t.duration_minutes))

    def filter_by_pet(self, pet_name: str) -> list[Task]:
        """Return pending tasks for a single pet, sorted by priority."""
        tasks = [t for pet in self.owner.get_pets() if pet.name == pet_name
                 for t in pet.get_pending_tasks()]
        return sorted(tasks, key=lambda t: self.PRIORITY_ORDER.get(t.priority, 99))

    def detect_conflicts(self) -> list[str]:
        """Return a list of conflict warnings before scheduling."""
        warnings = []
        seen_titles: set[str] = set()

        for task in self.owner.get_all_tasks():
            # Duplicate task titles across pets
            if task.title in seen_titles:
                warnings.append(f"Duplicate task title '{task.title}' found across pets.")
            seen_titles.add(task.title)

            # Task that can never fit in the time budget
            if task.duration_minutes > self.owner.available_minutes:
                warnings.append(
                    f"'{task.title}' needs {task.duration_minutes} min but owner only has "
                    f"{self.owner.available_minutes} min — can never be scheduled."
                )

        return warnings

    def reset_daily_tasks(self) -> None:
        """Reset completion status for all daily-frequency tasks (call at start of new day)."""
        for task in self.owner.get_all_tasks():
            if task.frequency == "daily":
                task.reset()

    def generate_plan(self) -> Plan:
        """Fit prioritized tasks into the owner's time budget and assign start times."""
        plan = Plan()
        plan.conflicts = self.detect_conflicts()
        time_remaining = self.owner.available_minutes
        current_minute = self.day_start_minute

        for task in self.prioritize():
            if task.duration_minutes <= time_remaining:
                plan.scheduled_tasks.append(task)
                plan.start_times[task.title] = current_minute
                plan.total_minutes += task.duration_minutes
                current_minute += task.duration_minutes
                time_remaining -= task.duration_minutes
                plan.reasons[task.title] = f"{task.priority} priority, fits in available time"
            else:
                plan.skipped_tasks.append(task)
                plan.reasons[task.title] = (
                    f"skipped — needs {task.duration_minutes} min, "
                    f"only {time_remaining} min left"
                )

        return plan
