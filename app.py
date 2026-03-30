import streamlit as st
from pawPawl_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# --- Session State ---
if "owner" not in st.session_state:
    st.session_state.owner = None
if "pets" not in st.session_state:
    st.session_state.pets = {}

# --- Owner Setup ---
st.subheader("Owner Info")
col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner name", value="Jordan")
with col2:
    available_minutes = st.number_input("Time available today (min)", min_value=10, max_value=480, value=90)

if st.button("Save owner"):
    st.session_state.owner = Owner(name=owner_name, available_minutes=available_minutes)
    st.session_state.pets = {}
    st.success(f"Owner '{owner_name}' saved — {available_minutes} min available today.")

if st.session_state.owner is None:
    st.info("Save an owner above to get started.")
    st.stop()

owner: Owner = st.session_state.owner

st.divider()

# --- Pet Setup ---
st.subheader("Add a Pet")
col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col3:
    age = st.number_input("Age", min_value=0, max_value=30, value=3)

if st.button("Add pet"):
    if pet_name in st.session_state.pets:
        st.warning(f"'{pet_name}' is already added.")
    else:
        pet = Pet(name=pet_name, species=species, age=age)
        st.session_state.pets[pet_name] = pet
        owner.add_pet(pet)
        st.success(f"Added {species} '{pet_name}'.")

if st.session_state.pets:
    st.caption("Registered pets: " + ", ".join(
        f"{p.name} ({p.species})" for p in owner.get_pets()
    ))

st.divider()

# --- Task Setup ---
st.subheader("Add a Task")

if not st.session_state.pets:
    st.info("Add at least one pet before adding tasks.")
else:
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        task_pet = st.selectbox("For pet", list(st.session_state.pets.keys()))
    with col2:
        task_title = st.text_input("Task title", value="Morning walk")
    with col3:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
    with col4:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col5:
        frequency = st.selectbox("Frequency", ["daily", "weekly", "as-needed"])

    if st.button("Add task"):
        pet = st.session_state.pets[task_pet]
        pet.add_task(Task(
            title=task_title,
            duration_minutes=int(duration),
            priority=priority,
            frequency=frequency,
        ))
        st.success(f"Added '{task_title}' to {task_pet}.")

    # Task table — sorted by priority using Scheduler.prioritize()
    all_tasks = owner.get_all_tasks()
    if all_tasks:
        scheduler = Scheduler(owner=owner)
        sorted_pending = scheduler.prioritize()
        as_needed = [t for t in all_tasks if t.frequency == "as-needed"]

        st.markdown("**All tasks (sorted by priority):**")
        rows = []
        for p in owner.get_pets():
            for t in p.get_tasks():
                rows.append({
                    "Pet": p.name,
                    "Task": t.title,
                    "Duration (min)": t.duration_minutes,
                    "Priority": t.priority,
                    "Frequency": t.frequency,
                    "Status": "done" if t.completed else "pending",
                })
        # Sort rows by priority order for display
        priority_order = {"high": 0, "medium": 1, "low": 2}
        rows.sort(key=lambda r: priority_order.get(r["Priority"], 99))
        st.table(rows)

        if as_needed:
            st.info(
                f"**As-needed tasks** (not auto-scheduled): "
                + ", ".join(f"{t.title} ({t.duration_minutes} min)" for t in as_needed)
            )
    else:
        st.info("No tasks yet.")

st.divider()

# --- Schedule Generation ---
st.subheader("Generate Schedule")

if st.button("Generate schedule"):
    if not owner.get_all_pending_tasks():
        st.warning("No pending tasks to schedule. All tasks may already be completed.")
    else:
        scheduler = Scheduler(owner=owner, day_start_minute=480)

        # Show conflict warnings BEFORE the plan
        conflicts = scheduler.detect_conflicts()
        if conflicts:
            st.error("**Conflicts detected — fix these before scheduling:**")
            for c in conflicts:
                st.warning(f"⚠ {c}")

        plan = scheduler.generate_plan()

        # Summary banner
        time_left = owner.available_minutes - plan.total_minutes
        st.success(
            f"Scheduled **{len(plan.scheduled_tasks)} tasks** — "
            f"{plan.total_minutes} of {owner.available_minutes} min used "
            f"({time_left} min free)"
        )

        # Scheduled tasks table with start times
        if plan.scheduled_tasks:
            st.markdown("**Today's schedule:**")
            schedule_rows = []
            for task in plan.scheduled_tasks:
                start = plan.start_times.get(task.title, 0)
                h, m = divmod(start, 60)
                schedule_rows.append({
                    "Start": f"{h:02d}:{m:02d}",
                    "Task": task.title,
                    "Duration (min)": task.duration_minutes,
                    "Priority": task.priority,
                    "Reason": plan.reasons[task.title],
                })
            st.table(schedule_rows)

        # Skipped tasks
        if plan.skipped_tasks:
            st.warning(f"{len(plan.skipped_tasks)} task(s) couldn't fit in your time budget:")
            for task in plan.skipped_tasks:
                st.markdown(f"- **{task.title}** — {plan.reasons[task.title]}")
