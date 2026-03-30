import streamlit as st
from pawPawl_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# --- Session State Initialization ---
# st.session_state acts like a dictionary that survives reruns.
# The pattern "if key not in st.session_state" means:
#   "only create this object the FIRST time — reuse it every time after."
if "owner" not in st.session_state:
    st.session_state.owner = None

if "pets" not in st.session_state:
    st.session_state.pets = {}  # pet_name -> Pet object

# --- Owner Setup ---
st.subheader("Owner Info")
col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner name", value="Jordan")
with col2:
    available_minutes = st.number_input("Time available today (min)", min_value=10, max_value=480, value=90)

if st.button("Save owner"):
    st.session_state.owner = Owner(name=owner_name, available_minutes=available_minutes)
    st.session_state.pets = {}  # reset pets when owner changes
    st.success(f"Owner '{owner_name}' saved with {available_minutes} min available.")

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
    st.caption(f"Pets: {', '.join(st.session_state.pets.keys())}")

st.divider()

# --- Task Setup ---
st.subheader("Add a Task")

if not st.session_state.pets:
    st.info("Add at least one pet before adding tasks.")
else:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_pet = st.selectbox("For pet", list(st.session_state.pets.keys()))
    with col2:
        task_title = st.text_input("Task title", value="Morning walk")
    with col3:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
    with col4:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    if st.button("Add task"):
        pet = st.session_state.pets[task_pet]
        pet.add_task(Task(title=task_title, duration_minutes=int(duration), priority=priority))
        st.success(f"Added '{task_title}' to {task_pet}.")

    all_tasks = owner.get_all_tasks()
    if all_tasks:
        st.write("Current tasks:")
        st.table([
            {"pet": p.name, "task": t.title, "duration (min)": t.duration_minutes, "priority": t.priority}
            for p in owner.get_pets()
            for t in p.get_tasks()
        ])
    else:
        st.info("No tasks yet.")

st.divider()

# --- Schedule Generation ---
st.subheader("Generate Schedule")

if st.button("Generate schedule"):
    if not owner.get_all_pending_tasks():
        st.warning("No pending tasks to schedule.")
    else:
        scheduler = Scheduler(owner=owner)
        plan = scheduler.generate_plan()

        st.success(f"Scheduled {len(plan.scheduled_tasks)} tasks — {plan.total_minutes} min used.")

        st.markdown("**Scheduled:**")
        for task in plan.scheduled_tasks:
            st.markdown(f"- **[{task.priority.upper()}]** {task.title} ({task.duration_minutes} min) — {plan.reasons[task.title]}")

        if plan.skipped_tasks:
            st.markdown("**Skipped:**")
            for task in plan.skipped_tasks:
                st.markdown(f"- ~~{task.title}~~ — {plan.reasons[task.title]}")
