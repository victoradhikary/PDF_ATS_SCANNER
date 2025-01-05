import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the generative AI API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from the generative AI model
def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

# Function to extract text from the uploaded PDF
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""  # Extract text, handling None gracefully
    return text

# Streamlit app
st.title("SMART RESUME EVALUATOR")
st.text("Improve your resume for ATS")

# Input fields
jd = st.text_area("Paste The Job Description")
uploaded_file = st.file_uploader(
    "Upload your resume", type='pdf', help="Please upload your resume in PDF format"
)

# Button to trigger evaluation
submit = st.button("Evaluate")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)

        # Replace placeholders in the input prompt with actual values
        input_prompt = f"""
        Hey Act Like a skilled or very experienced ATS (Application Tracking System)
        with a deep understanding of the tech field, software engineering, data science,
        data analysis, and big data engineering. Your task is to evaluate the resume based 
        on the given job description. You must consider the job market is very competitive 
        and you should provide the best assistance for improving the resumes. Assign the 
        percentage matching based on the JD and the missing keywords with high accuracy.
        resume: {text}
        description: {jd}

        I want the response in one single string having the structure:
        {{"JD Match":"%", "MissingKeywords":[], "Profile Summary":""}}
        """

        try:
            # Get the response from the generative AI
            response = get_gemini_response(input_prompt)
            st.subheader("Evaluation Result")
            st.text(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please upload a PDF file containing your resume.")
