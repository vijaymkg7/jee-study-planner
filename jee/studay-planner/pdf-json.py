import streamlit as st
import cv2
import pytesseract
import re
import json
import numpy as np
from pdf2image import convert_from_bytes

# Set up Tesseract OCR (ensure it's installed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Change for your OS

# Function to extract text from image
def extract_text_from_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    extracted_text = pytesseract.image_to_string(gray)
    return extracted_text

# Function to extract exercise number
def extract_exercise_number(text):
    match = re.search(r"EXERCISE (\d+\.\d+)", text, re.IGNORECASE)
    return match.group(1) if match else "Unknown"

# Function to extract functions & integrals
def extract_functions_integrals(text):
    functions = {}
    integrals = {}
    reading_integrals = False

    lines = text.split("\n")
    for line in lines:
        match = re.match(r"(\d+)\.\s([^\n]+)", line.strip())
        if match:
            num, expr = match.groups()
            if not reading_integrals:
                functions[num] = expr.strip()
            else:
                integrals[num] = expr.strip()
        elif "∫" in line:  # Detect integrals section
            reading_integrals = True
            num = str(len(integrals) + 6)  # Assumes integrals start from 6
            integrals[num] = line.strip()

    return functions, integrals

# Streamlit UI
st.title("📄 IIT JEE Math Paper Processor")
st.write("Upload an image or PDF of an exercise, and AI will extract functions and integrals dynamically.")

uploaded_file = st.file_uploader("Upload Image or PDF", type=["png", "jpg", "jpeg", "pdf"])

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        images = convert_from_bytes(uploaded_file.read())
        image = np.array(images[0])  # Convert first page to numpy array
    else:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    extracted_text = extract_text_from_image(image)
    exercise_number = extract_exercise_number(extracted_text)
    functions, integrals = extract_functions_integrals(extracted_text)

    json_output = {
        "Exercise": exercise_number,
        "Functions": functions,
        "Integrals": integrals
    }

    st.subheader("📌 Extracted Exercise Number")
    st.write(f"**Exercise {exercise_number}**")

    st.subheader("📌 Extracted Functions")
    st.json(functions)

    st.subheader("📌 Extracted Integrals")
    st.json(integrals)

    st.subheader("📥 Download JSON")
    json_data = json.dumps(json_output, indent=4)
    st.download_button("Download JSON", json_data, file_name=f"exercise_{exercise_number}.json", mime="application/json")
