from pawPawl_system import Owner, Pet, Task, Scheduler

# --- Setup ---
owner = Owner(name="Jordan", available_minutes=90)

mochi = Pet(name="Mochi", species="dog", age=3)
luna = Pet(name="Luna", species="cat", age=5)

mochi.add_task(Task(title="Morning walk",       duration_minutes=30, priority="high",   frequency="daily"))
mochi.add_task(Task(title="Brush coat",         duration_minutes=15, priority="medium", frequency="weekly"))
mochi.add_task(Task(title="Vet check",          duration_minutes=60, priority="high",   frequency="as-needed"))  # skipped by scheduler

luna.add_task(Task(title="Feeding",             duration_minutes=10, priority="high",   frequency="daily"))
luna.add_task(Task(title="Litter box cleaning", duration_minutes=10, priority="medium", frequency="daily"))
luna.add_task(Task(title="Enrichment play",     duration_minutes=20, priority="low",    frequency="daily"))

owner.add_pet(mochi)
owner.add_pet(luna)

scheduler = Scheduler(owner=owner, day_start_minute=480)  # schedule starts at 8:00 AM

# --- Conflict Detection ---
conflicts = scheduler.detect_conflicts()
if conflicts:
    print("\n⚠ Conflicts detected:")
    for c in conflicts:
        print(f"  - {c}")

# --- Generate Plan ---
plan = scheduler.generate_plan()

# --- Display with start times ---
print(f"\n{'='*42}")
print(f"  Today's Schedule for {owner.name}")
print(f"  Time budget: {owner.available_minutes} min  |  Starts: 08:00")
print(f"{'='*42}")
print(plan.display())

# --- Explain reasoning ---
print("\nReasoning:")
print(plan.explain())

# --- Filter: tasks by pet ---
print(f"\nMochi's tasks only:")
for t in owner.get_tasks_for_pet("Mochi"):
    status = "done" if t.completed else "pending"
    print(f"  [{status}] {t.title} ({t.frequency})")

# --- Filter: as-needed tasks (excluded from auto-schedule) ---
as_needed = [t for t in owner.get_all_tasks() if t.frequency == "as-needed"]
if as_needed:
    print(f"\nAs-needed tasks (not auto-scheduled):")
    for t in as_needed:
        print(f"  {t.title} ({t.duration_minutes} min, {t.priority} priority)")

# --- Recurring: simulate next day reset ---
print(f"\n-- Next day: resetting daily tasks --")
scheduler.reset_daily_tasks()
pending_after_reset = owner.get_all_pending_tasks()
print(f"Pending tasks after reset: {[t.title for t in pending_after_reset]}")

print(f"\n{'='*42}\n")
