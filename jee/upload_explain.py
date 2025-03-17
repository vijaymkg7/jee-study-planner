import streamlit as st
import os
import ollama  # Using local Ollama models
from utils import extract_text_from_pdf, classify_questions
from crewai import Agent, Task, Crew

# Ensure upload directory exists 
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Define AI Agents using Ollama
explanation_agent = Agent(
    role="Concept Explainer", 
    goal="Explain difficult questions in an easy way",
    backstory="A top physics and math professor specializing in JEE Advanced concepts.",
    allow_delegation=True
)

def upload_explain_tab():
    """Main function to handle IIT JEE Paper upload & AI processing."""
    st.header("📄 Upload & Explain IIT JEE Paper")

    # Initialize session state for question index and explanations
    if 'question_index' not in st.session_state:
        st.session_state.question_index = 0
    if 'questions' not in st.session_state:
        st.session_state.questions = []
    if 'explanations' not in st.session_state:
        st.session_state.explanations = {}

    uploaded_file = st.file_uploader("Upload JEE Paper (PDF)", type=["pdf"])

    if uploaded_file:
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        st.success(f"Uploaded: {uploaded_file.name}")
        st.write("Processing file...")

        # Extract text from PDF
        text = extract_text_from_pdf(file_path)
        st.session_state.questions = text.split('\n\n')  # Assuming questions are separated by double newlines

        # Display questions list
        st.subheader("📝 All Questions")
        for i, question in enumerate(st.session_state.questions):
            with st.expander(f"Question {i+1}"):
                st.text_area(f"Question Text {i+1}", question, height=100, key=f"q_{i}")
                
                # Explain button for each question
                if st.button("📜 Explain", key=f"explain_{i}"):
                    if i not in st.session_state.explanations:
                        with st.spinner("Analyzing question..."):
                            response = ollama.chat(
                                model="mistral",
                                messages=[{"role": "user", "content": f"Explain this JEE question in detail:\n{question}"}]
                            )
                            st.session_state.explanations[i] = response["message"]["content"]
                    
                    st.markdown("### Explanation:")
                    st.write(st.session_state.explanations[i])

# Run the function in Streamlit
upload_explain_tab()
