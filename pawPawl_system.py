from dataclasses import dataclass, field


@dataclass
class Pet:
    name: str
    species: str
    age: int
    special_needs: list[str] = field(default_factory=list)


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    completed: bool = False

    def is_high_priority(self) -> bool:
        pass


class Owner:
    def __init__(self, name: str, available_minutes: int, preferences: list[str] = None):
        self.name = name
        self.available_minutes = available_minutes
        self.preferences = preferences or []
        self._tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        pass

    def get_tasks(self) -> list[Task]:
        pass


@dataclass
class Plan:
    scheduled_tasks: list[Task] = field(default_factory=list)
    total_minutes: int = 0
    skipped_tasks: list[Task] = field(default_factory=list)
    reasons: dict[str, str] = field(default_factory=dict)  # task title -> reason chosen/skipped

    def explain(self) -> str:
        pass

    def display(self) -> str:
        pass


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet):
        self.owner = owner
        self.pet = pet

    def generate_plan(self) -> Plan:
        pass

    def prioritize(self) -> list[Task]:
        pass
