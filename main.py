from pawPawl_system import Owner, Pet, Task, Scheduler

# --- Setup ---
owner = Owner(name="Jordan", available_minutes=90)

mochi = Pet(name="Mochi", species="dog", age=3)
luna = Pet(name="Luna", species="cat", age=5)

# Tasks for Mochi
mochi.add_task(Task(title="Morning walk", duration_minutes=30, priority="high"))
mochi.add_task(Task(title="Brush coat", duration_minutes=15, priority="medium"))

# Tasks for Luna
luna.add_task(Task(title="Feeding", duration_minutes=10, priority="high"))
luna.add_task(Task(title="Litter box cleaning", duration_minutes=10, priority="medium"))
luna.add_task(Task(title="Enrichment play", duration_minutes=20, priority="low"))

owner.add_pet(mochi)
owner.add_pet(luna)

# --- Schedule ---
scheduler = Scheduler(owner=owner)
plan = scheduler.generate_plan()

# --- Display ---
print(f"\n{'='*40}")
print(f"  Today's Schedule for {owner.name}")
print(f"  Time budget: {owner.available_minutes} min")
print(f"{'='*40}")

print("\nScheduled tasks:")
for task in plan.scheduled_tasks:
    print(f"  [{task.priority.upper():6}] {task.title} ({task.duration_minutes} min)")
    print(f"           → {plan.reasons[task.title]}")

if plan.skipped_tasks:
    print("\nSkipped tasks:")
    for task in plan.skipped_tasks:
        print(f"  [SKIP] {task.title} — {plan.reasons[task.title]}")

print(f"\nTotal time scheduled: {plan.total_minutes} / {owner.available_minutes} min")
print(f"{'='*40}\n")
