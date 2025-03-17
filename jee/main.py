import streamlit as st
import os
import ollama  # AI Model (Switchable with Gemini/Hugging Face)
from utils import extract_text_from_pdf, classify_questions  # Custom functions for text extraction
from study_planner import study_planner_tab  # Import study planner tab
from upload_explain import upload_explain_tab  # Import upload explain tab
from strategy import strategy_tab  # Import strategy tab

# ✅ Set Page Config (Must be first)
st.set_page_config(page_title="JEE Planner", layout="wide")

# ✅ Ensure upload directory exists
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ✅ Define Tabs
tab1, tab2, tab3 = st.tabs(["📚 Study Planner", "📑 Upload & Explain IIT Paper", "📋 Strategy"])

# ✅ Render Tabs
with tab1:
    study_planner_tab()
with tab2:
    upload_explain_tab()

with tab3:
    strategy_tab()
