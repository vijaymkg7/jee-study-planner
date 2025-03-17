import PyPDF2
import re
import ollama

def extract_text_from_pdf(pdf_file):
    """Extracts text from a PDF file."""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        extracted_text = page.extract_text()
        if extracted_text:
            text += extracted_text + "\n"
    return text.strip()

def extract_questions(text):
    """Extracts individual IIT JEE questions from the text using regex."""
    # Assuming questions are numbered (e.g., "1. What is the value of ...?")
    question_pattern = r"\d+\.\s+.*?(?=\n\d+\.|\Z)"  # Matches until the next number or end
    questions = re.findall(question_pattern, text, re.DOTALL)
    return questions if questions else ["No questions found."]

def classify_questions(text):
    """Classifies extracted IIT JEE questions into categories using AI."""
    categories = ["Physics", "Chemistry", "Mathematics"]
    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": f"Classify the following text into Physics, Chemistry, or Mathematics:\n{text}"}]
    )
    return response["message"]["content"]

def explain_question(question):
    """Uses AI to explain a given question."""
    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": f"Explain this IIT JEE question in detail:\n{question}"}]
    )
    return response["message"]["content"]

def answer_question(question):
    """Uses AI to answer a given question."""
    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": f"Provide a detailed solution for this IIT JEE question:\n{question}"}]
    )
    return response["message"]["content"]

def process_questions(text):
    """Extracts, classifies, explains, and answers each question."""
    questions = extract_questions(text)
    processed_questions = []

    for question in questions:
        category = classify_questions(question)
        explanation = explain_question(question)
        answer = answer_question(question)
        processed_questions.append({
            "question": question,
            "category": category,
            "explanation": explanation,
            "answer": answer
        })

    return processed_questions
