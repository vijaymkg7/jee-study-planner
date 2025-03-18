import streamlit as st
import json
import ollama
import matplotlib.pyplot as plt
from datetime import datetime
import os

st.set_page_config(page_title="AI-Powered NCERT Study Planner", layout="wide")

# ------------------------------- #
# 🔹 Load NCERT Class-wise JSON Files with File Check
# ------------------------------- #
NCERT_JSON = {
    "Class 11": {
        "Physics": "ncert_11_physics.json",
        "Chemistry": "ncert_11_chemistry.json",
        "Mathematics": "ncert_11_mathematics.json"
    },
    "Class 12": {
        "Physics": "ncert_12_physics.json",
        "Chemistry": "ncert_12_chemistry.json",
        "Mathematics": "ncert_12_mathematics.json"
    }
}

# ------------------------------- #
# 🔹 Initialize Session State
# ------------------------------- #
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# ------------------------------- #
# 🔹 Sidebar: Study Selection
# ------------------------------- #
st.sidebar.header("📊 AI-Powered Study Planner")

# ✅ Class Selection
selected_class = st.sidebar.selectbox("📚 Select Class", list(NCERT_JSON.keys()))

# ✅ Subject Selection
subjects = list(NCERT_JSON[selected_class].keys())
selected_subject = st.sidebar.selectbox("🔬 Select Subject", subjects)

# ✅ Load the correct JSON file with error handling
json_file_path = NCERT_JSON[selected_class][selected_subject]

if not os.path.exists(json_file_path):
    st.error(f"⚠️ The file `{json_file_path}` was not found. Please check the directory.")
    st.stop()

with open(json_file_path, "r") as file:
    ncert_data = json.load(file)

# ✅ Chapter Selection
chapters = list(ncert_data.keys())
selected_chapter = st.sidebar.selectbox("📖 Select Chapter", chapters)

# ✅ Subtopics & Exercises Selection
chapter_data = ncert_data[selected_chapter]
subtopics = chapter_data.get("Topics", [])
exercises = chapter_data.get("Exercises", {})

selected_subtopics = st.sidebar.multiselect("📍 Select Subtopics", subtopics)
exercise_selected = st.sidebar.selectbox("📘 Select Exercise", list(exercises.keys()) if exercises else ["No Exercises"])

# ------------------------------- #
# 🔹 Tabs: Study Plan, Task Manager, Exercises, Progress
# ------------------------------- #
tab1, tab2, tab3, tab4 = st.tabs(["📅 AI Study Planner", "✅ Task Manager", "📖 Exercises", "📊 Progress"])

# 📅 AI Study Planner
with tab1:
    st.header("📅 AI-Powered Study Plan Generator")

    exam_date = st.date_input("🎯 JEE Exam Date", datetime(2025, 5, 1))
    start_date = st.date_input("📆 Start Date", datetime.today())
    available_hours = st.slider("⏳ Daily Study Hours", 2, 10, 4)

    st.write(f"📖 **Selected Chapter**: {selected_chapter}")
    st.write(f"📍 **Selected Subtopics**: {', '.join(selected_subtopics) if selected_subtopics else 'None'}")

    if st.button("🚀 Generate AI Study Plan"):
        prompt = f"""
        Generate a structured study plan for:
        - Class: {selected_class}
        - Subject: {selected_subject}
        - Chapter: {selected_chapter}
        - Subtopics: {', '.join(selected_subtopics)}
        - Exam Date: {exam_date}
        - Daily Study Hours: {available_hours}
        Include revision, concept strengthening, and problem-solving strategies.
        """

        response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
        ai_study_plan = response['message']['content']

        st.subheader("📅 AI-Generated Study Plan")
        st.write(ai_study_plan)

        st.session_state.tasks.append({
            "task": f"Study {selected_chapter} ({', '.join(selected_subtopics)})",
            "details": f"{ai_study_plan}",
            "status": "Pending",
            "note": ""
        })

        st.success("✅ AI-generated study plan added as a Task!")

# ✅ Task Manager
with tab2:
    st.header("✅ Task Manager")

    if st.session_state.tasks:
        for i, task in enumerate(st.session_state.tasks):
            col1, col2, col3 = st.columns([0.6, 0.2, 0.2])

            with col1:
                st.write(f"📌 **{task['task']}**")
                st.write(f"📝 {task['details']}")
                st.session_state.tasks[i]["note"] = st.text_area(f"📝 Notes", task["note"], key=f"note_{i}")

            with col2:
                status = st.selectbox("📋 Status", ["Pending", "Completed"], index=0 if task["status"] == "Pending" else 1, key=f"status_{i}")
                st.session_state.tasks[i]["status"] = status

            with col3:
                if st.button("❌ Remove", key=f"remove_{i}"):
                    st.session_state.tasks.pop(i)
                    st.rerun()
    else:
        st.warning("⚠️ No tasks available. Generate a study plan first!")

# 📖 Exercises Tab
with tab3:
    st.header("📖 AI-Powered Exercise Solutions")

    st.write(f"📘 **Selected Exercise**: {exercise_selected}")

    if exercise_selected != "No Exercises":
        st.write(f"🔹 **Exercise Content**: {exercises.get(exercise_selected, 'No details available')}")

    if st.button("🧠 Solve Exercise"):
        prompt = f"""
        Solve the following NCERT Class {selected_class} {selected_subject} Exercise:
        - Chapter: {selected_chapter}
        - Exercise: {exercise_selected}
        - Question: {exercises.get(exercise_selected, 'No details available')}
        Provide step-by-step solutions with explanations.
        """

        response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
        ai_solution = response['message']['content']

        st.subheader("📝 AI-Generated Solution")
        st.write(ai_solution)

# 📊 Progress Tab with Fixed Pie Chart
with tab4:
    st.header("📊 Study Progress Tracker")

    # Count Completed and Pending Tasks
    completed_tasks = sum(1 for task in st.session_state.tasks if task["status"] == "Completed")
    pending_tasks = sum(1 for task in st.session_state.tasks if task["status"] == "Pending")

    if completed_tasks == 0 and pending_tasks == 0:
        st.warning("⚠️ No tasks available to track progress.")
    else:
        # Visualization using Matplotlib
        fig, ax = plt.subplots(figsize=(5, 3))
        labels = ["Completed", "Pending"]
        sizes = [completed_tasks, pending_tasks]
        colors = ["#4CAF50", "#FF5733"]

        ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90, colors=colors, shadow=True)
        ax.axis("equal")

        st.pyplot(fig)

        # Display Progress Stats
        total_tasks = completed_tasks + pending_tasks
        progress_percentage = (completed_tasks / total_tasks) * 100
        st.write(f"📈 **Progress: {progress_percentage:.2f}% Completed**")
