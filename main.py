import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

from enum import Enum

class GeminiModel(Enum):
    GEMINI_2_5_PRO_EXP = "gemini-2.5-pro-exp-03-25"
    GEMINI_2_0_FLASH = "gemini-2.0-flash"
    GEMINI_2_0_FLASH_LITE = "gemini-2.0-flash-lite"
    GEMINI_1_5_FLASH = "gemini-1.5-flash"
    GEMINI_1_5_FLASH_8B = "gemini-1.5-flash-8b"
    GEMINI_1_5_PRO = "gemini-1.5-pro"
    GEMINI_EMBEDDING = "gemini-embedding-exp"
    IMAGEN_3 = "imagen-3.0-generate-002"

load_dotenv()  # Load all environment variables

genai.configure(api_key=os.getenv("API_KEY"))

def get_gemini_response(input_text):
    model = genai.GenerativeModel(GeminiModel.GEMINI_2_0_FLASH.value)  # Use .value to pass the correct string
    response = model.generate_content(input_text)  # Ensure input_text is a string, not a list
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += str(page.extract_text())
    return text

# Prompt Template
input_prompt = """
Hey, act like a skilled or very experienced ATS (Application Tracking System)
with a deep understanding of the tech field, software engineering, data science, data analytics,
and big data engineering. Your task is to evaluate the resume based on the given job description.
You must consider that the job market is very competitive, and you should provide
the best assistance for improving the resumes. Assign the percentage match based
on the JD and the missing keywords with high accuracy.

Resume: {text}
Description: {jd}

I want the response in one single string with the structure:
{{"JD Match": "%", "MissingKeywords": [], "Profile Summary": ""}}
"""

# Streamlit App
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload a PDF")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        formatted_prompt = input_prompt.format(text=text, jd=jd)  # Ensure proper formatting
        response = get_gemini_response(formatted_prompt)  # Pass a string instead of a list
        st.subheader(response)
