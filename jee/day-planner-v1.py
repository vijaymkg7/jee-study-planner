import streamlit as st
import json
import ollama
from datetime import datetime

st.set_page_config(page_title="AI-Powered NCERT Study Planner", layout="wide")

# Load NCERT Class 11 & 12 JSON
NCERT_JSON = {
    "Class 11": {},  # Placeholder for Class 11 topics
    "Class 12": {}   # Placeholder for Class 12 topics
}

# Load NCERT JSON files
with open("ncert_class_11.json", "r") as file:
    NCERT_JSON["Class 11"] = json.load(file)

with open("ncert_class_12.json", "r") as file:
    NCERT_JSON["Class 12"] = json.load(file)

# Initialize Session State
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Sidebar: Study Selection
st.sidebar.header("📊 AI-Powered Study Planner")

selected_class = st.sidebar.selectbox("📚 Select Class", list(NCERT_JSON.keys()))
selected_subject = st.sidebar.selectbox("🔬 Select Subject", list(NCERT_JSON[selected_class].keys()))
selected_chapter = st.sidebar.selectbox("📖 Select Chapter", list(NCERT_JSON[selected_class][selected_subject].keys()))

# Select Subtopics
subtopics = NCERT_JSON[selected_class][selected_subject][selected_chapter]
selected_subtopics = st.sidebar.multiselect("📍 Select Subtopics", subtopics)

# Study Plan & Task Manager Tabs
tab1, tab2 = st.tabs(["📅 AI Study Planner", "✅ Task Manager"])

# 📅 AI Study Planner
with tab1:
    st.header("📅 AI-Powered Study Plan Generator")

    exam_date = st.date_input("🎯 JEE Exam Date", datetime(2025, 5, 1))
    start_date = st.date_input("📆 Start Date", datetime.today())
    available_hours = st.slider("⏳ Daily Study Hours", 2, 10, 4)

    st.write(f"📖 Selected Chapter: **{selected_chapter}**")
    st.write(f"📍 Selected Subtopics: **{', '.join(selected_subtopics) if selected_subtopics else 'None'}**")

    if st.button("🚀 Generate AI Study Plan"):
        prompt = f"""
        Generate a detailed study plan for:
        - Class: {selected_class}
        - Subject: {selected_subject}
        - Chapter: {selected_chapter}
        - Subtopics: {', '.join(selected_subtopics)}
        - Exam Date: {exam_date}
        - Daily Study Hours: {available_hours}
        Include revision schedules and problem-solving practice.
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
    for i, task in enumerate(st.session_state.tasks):
        st.write(f"📌 **{task['task']}** - {task['status']}")
        st.text_area("Notes", task["note"], key=f"note_{i}")
