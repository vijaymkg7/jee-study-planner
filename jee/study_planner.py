import streamlit as st
import ollama  # AI Model (Switchable with Gemini/Hugging Face)

def get_ai_study_plan(subject, topic):
    """Generate an AI-driven study plan for the selected topic."""
    prompt = f"Generate a detailed IIT JEE study plan for {subject} - {topic}, including concepts, key formulas, and problem-solving strategies."
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

def get_ai_explanation(question):
    """AI explanation for user doubts."""
    prompt = f"Explain the following JEE concept in simple terms: {question}"
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

def study_planner_tab():
    """Interactive Study Planner with AI Assistance"""
    
    # Title
    st.header("📖 IIT JEE Study Planner (AI-Enabled)")

    # Subject selection
    subject = st.selectbox("📚 Select Subject", ["Physics", "Maths", "Chemistry"])

    # Topics dictionary
    topics_dict = {
        "Physics": ["Kinematics", "Rotational Motion", "Thermodynamics", "Electromagnetism", "Modern Physics"],
        "Maths": ["Algebra", "Calculus", "Coordinate Geometry", "Probability", "Vectors & 3D"],
        "Chemistry": ["Organic Chemistry", "Inorganic Chemistry", "Physical Chemistry", "Thermodynamics"]
    }
    
    topic = st.selectbox("📌 Select Topic", topics_dict[subject])

    # Generate AI Study Plan
    if st.button("🚀 Generate Study Plan"):
        ai_plan = get_ai_study_plan(subject, topic)
        st.markdown(f"### 📑 AI-Generated Study Plan for {subject} - {topic}")
        st.write(ai_plan)

    # Study Resources
    st.subheader(f"🔗 Study Resources for {subject} - {topic}")
    st.markdown(f"📺 [**Watch concept videos on {topic}**](https://www.youtube.com/results?search_query={topic}+for+IIT+JEE)")
    st.markdown(f"📜 [**Solve previous year JEE Advanced & Mains questions**](https://jeemain.nta.nic.in/)")
    st.markdown("📘 [**Revise key formulas & theorems**](https://physicswallah.com/notes)", unsafe_allow_html=True)
    st.markdown(f"📝 [**Practice mock tests & timed quizzes**](https://nta.ac.in/Quiz)")

    # AI Doubt Solver
    st.subheader("🤖 Ask AI for Concept Explanation")
    user_question = st.text_input("🔍 Enter your doubt:")
    
    if st.button("💡 Get AI Explanation"):
        if user_question:
            explanation = get_ai_explanation(user_question)
            st.write("### 🤔 AI Explanation")
            st.write(explanation)
        else:
            st.warning("⚠️ Please enter a question.")

    # Custom Task List
    if "study_tasks" not in st.session_state:
        st.session_state.study_tasks = []

    custom_task = st.text_input("✍️ Add a custom study task:")
    
    if st.button("➕ Add Task"):
        if custom_task:
            st.session_state.study_tasks.append(custom_task)
            st.success(f"✅ Task added: {custom_task}")
        else:
            st.warning("⚠️ Please enter a task.")

    # Display Study Tasks
    if st.session_state.study_tasks:
        st.subheader("✅ Your Study Tasks:")
        for i, task in enumerate(st.session_state.study_tasks):
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                st.write(f"🔹 {task}")
            with col2:
                if st.button("❌ Remove", key=f"remove_{i}"):
                    st.session_state.study_tasks.pop(i)
                    st.rerun()
