import streamlit as st
import json
import ollama
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
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
selected_exercises = st.sidebar.multiselect("📘 Select Exercises", list(exercises.keys()) if exercises else ["No Exercises"])

# ------------------------------- #
# 🔹 Study Plan Timeframe Selection (Editable Dates)
# ------------------------------- #
col1, col2 = st.columns([0.3, 0.7])

with col1:
    timeframe = st.radio("📅 Select Timeframe", ["Weekly", "Monthly", "Yearly"])

with col2:
    start_date = st.date_input("📆 Start Date", datetime.today())
    default_end = {
        "Weekly": start_date + timedelta(days=6),
        "Monthly": start_date + timedelta(days=30),
        "Yearly": start_date + timedelta(days=365)
    }[timeframe]
    end_date = st.date_input("📆 End Date", default_end)

available_hours = st.slider("⏳ Daily Study Hours", 2, 10, 4)

# ------------------------------- #
# 🔹 Tabs: Study Plan, Task Manager, Exercises, Progress
# ------------------------------- #
tab1, tab2, tab3, tab4 = st.tabs(["📅 AI Study Planner", "✅ Task Manager", "📖 Exercises", "📊 Progress"])

# 📅 AI Study Planner
with tab1:
    st.header("📅 AI-Powered Study Plan Generator")
    st.write(f"📖 **Selected Chapter**: {selected_chapter}")
    st.write(f"📍 **Selected Subtopics**: {', '.join(selected_subtopics) if selected_subtopics else 'None'}")
    st.write(f"📘 **Selected Exercises**: {', '.join(selected_exercises) if selected_exercises else 'None'}")

    if st.button("🚀 Generate AI Study Plan"):
        prompt = f"""
        Generate a structured study plan for:
        - Class: {selected_class}
        - Subject: {selected_subject}
        - Chapter: {selected_chapter}
        - Subtopics: {', '.join(selected_subtopics)}
        - Exercises: {', '.join(selected_exercises)}
        - Timeframe: {timeframe}
        - Start Date: {start_date.strftime('%Y-%m-%d')}
        - End Date: {end_date.strftime('%Y-%m-%d')}
        - Daily Study Hours: {available_hours}
        Assign one subtopic or exercise per day and ensure optimal coverage.
        """

        response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
        ai_study_plan = response['message']['content']

        st.subheader("📅 AI-Generated Study Plan")
        st.write(ai_study_plan)

        # Save AI-generated study plan as tasks (one subtopic/exercise per day)
        study_days = pd.date_range(start=start_date, end=end_date).tolist()
        all_topics = selected_subtopics + selected_exercises
        total_days = len(study_days)
        
        if total_days < len(all_topics):
            st.warning("⚠️ Not enough days to cover all topics. Consider a longer timeframe.")

        for i, topic in enumerate(all_topics):
            if i < total_days:  # Ensure we don't exceed available days
                st.session_state.tasks.append({
                    "date": study_days[i].strftime('%Y-%m-%d'),
                    "task": topic,
                    "status": "Pending",
                    "planned_hours": available_hours,
                    "actual_hours": 0,
                    "note": ""
                })

        st.success("✅ AI-generated study plan added as tasks!")

# ✅ Task Manager (Table Format Only)
with tab2:
    st.header("✅ Task Manager (Table Format)")

    if st.session_state.tasks:
        # Convert tasks to DataFrame
        df = pd.DataFrame(st.session_state.tasks)

        # Editable Columns (Status, Planned Hours, Actual Hours, Notes)
        edited_df = st.data_editor(
            df,
            column_config={
                "date": st.column_config.TextColumn("📆 Date"),
                "task": st.column_config.TextColumn("📌 Topic"),
                "status": st.column_config.SelectboxColumn("📋 Status", options=["Pending", "Completed"]),
                "planned_hours": st.column_config.NumberColumn("⏳ Planned Hours"),
                "actual_hours": st.column_config.NumberColumn("⏳ Actual Hours"),
                "note": st.column_config.TextColumn("📝 Notes")
            },
            hide_index=True
        )

        # Save updates back to session state
        st.session_state.tasks = edited_df.to_dict("records")

    else:
        st.warning("⚠️ No tasks available. Generate a study plan first!")

# 📊 Progress Tab
with tab4:
    st.header("📊 Study Progress Tracker")

    completed_tasks = sum(1 for task in st.session_state.tasks if task["status"] == "Completed")
    pending_tasks = sum(1 for task in st.session_state.tasks if task["status"] == "Pending")

    if completed_tasks == 0 and pending_tasks == 0:
        st.warning("⚠️ No tasks available to track progress.")
    else:
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.pie(
            [completed_tasks, pending_tasks],
            labels=["Completed", "Pending"],
            autopct="%1.1f%%",
            colors=["#4CAF50", "#FF5733"],
            shadow=True,
            startangle=90
        )
        ax.axis("equal")
        st.pyplot(fig)
        st.write(f"📈 **Progress: {completed_tasks / (completed_tasks + pending_tasks) * 100:.2f}% Completed**")
