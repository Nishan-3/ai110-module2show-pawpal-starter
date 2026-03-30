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


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str           # "low", "medium", "high"
    frequency: str = "daily"  # "daily", "weekly", "as-needed"
    completed: bool = False

    def is_high_priority(self) -> bool:
        """Return True if this task has high priority."""
        return self.priority == "high"

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True


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
        """Returns all tasks across all pets."""
        return [task for pet in self._pets for task in pet.get_tasks()]

    def get_all_pending_tasks(self) -> list[Task]:
        """Returns all incomplete tasks across all pets."""
        return [task for pet in self._pets for task in pet.get_pending_tasks()]


@dataclass
class Plan:
    scheduled_tasks: list[Task] = field(default_factory=list)
    total_minutes: int = 0
    skipped_tasks: list[Task] = field(default_factory=list)
    reasons: dict[str, str] = field(default_factory=dict)  # task title -> reason chosen/skipped

    def explain(self) -> str:
        """Return a human-readable explanation of why each task was scheduled or skipped."""
        pass

    def display(self) -> str:
        """Return a formatted string showing the full daily schedule."""
        pass


class Scheduler:
    PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

    def __init__(self, owner: Owner):
        self.owner = owner

    def prioritize(self) -> list[Task]:
        """Sort all pending tasks by priority (high first), then duration (shortest first)."""
        tasks = self.owner.get_all_pending_tasks()
        return sorted(tasks, key=lambda t: (self.PRIORITY_ORDER.get(t.priority, 99), t.duration_minutes))

    def generate_plan(self) -> Plan:
        """Fit as many prioritized tasks as possible within the owner's time budget."""
        plan = Plan()
        time_remaining = self.owner.available_minutes

        for task in self.prioritize():
            if task.duration_minutes <= time_remaining:
                plan.scheduled_tasks.append(task)
                plan.total_minutes += task.duration_minutes
                time_remaining -= task.duration_minutes
                plan.reasons[task.title] = f"{task.priority} priority, fits in available time"
            else:
                plan.skipped_tasks.append(task)
                plan.reasons[task.title] = f"skipped — needs {task.duration_minutes} min, only {time_remaining} min left"

        return plan
