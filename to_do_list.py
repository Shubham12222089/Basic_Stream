import streamlit as st
from datetime import datetime

# Title of the app
col1, col2 = st.columns([1,2])
with col1:
    st.title("To-Do List")
with col2:
    st.image('to_do.jpeg',width = 70)
# Initialize session state variables
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

if 'completed_tasks' not in st.session_state:
    st.session_state.completed_tasks = []

# Add a new task
def add_task():
    task = st.session_state.new_task
    if task:
        st.session_state.tasks.append({"task": task, "added": datetime.now()})
        st.session_state.new_task = ""

# Mark a task as completed
def complete_task(task_index):
    completed_task = st.session_state.tasks.pop(task_index)
    st.session_state.completed_tasks.append(completed_task)

# Delete a task
def delete_task(task_index):
    st.session_state.tasks.pop(task_index)

# Input field to add new tasks
st.text_input("Add a new task:", key="new_task", on_change=add_task)

# Display the to-do list
st.subheader("To-Do List")
for index, task in enumerate(st.session_state.tasks):
    task_text = task["task"]
    added_time = task["added"].strftime("%Y-%m-%d %H:%M:%S")
    col1, col2, col3 = st.columns([6, 2, 2])
    col1.write(f"{task_text} (added on {added_time})")
    col2.button("Complete", key=f"complete_{index}", on_click=complete_task, args=(index,))
    col3.button("Delete", key=f"delete_{index}", on_click=delete_task, args=(index,))

# Display the completed tasks
st.subheader("Completed Tasks")
for task in st.session_state.completed_tasks:
    task_text = task["task"]
    completed_time = task["added"].strftime("%Y-%m-%d %H:%M:%S")
    st.success(f"{task_text} (added on {completed_time})")

