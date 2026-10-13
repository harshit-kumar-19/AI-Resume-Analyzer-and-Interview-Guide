import os
import streamlit as st
from groq import Groq
import pypdf

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="AI Mock Interview Copilot",
    page_icon="🎙️",
    layout="wide"
)

# ---------------------------------------------------------
# CLIENT INITIALIZATION (GROQ API)
# ---------------------------------------------------------
# Checks environment variables first, then Streamlit secrets as fallback
groq_api_key = os.environ.get("GROQ_API_KEY")

if not groq_api_key:
    try:
        groq_api_key = st.secrets.get("GROQ_API_KEY")
    except Exception:
        groq_api_key = None

try:
    client = Groq(api_key=groq_api_key) if groq_api_key else None
except Exception as e:
    client = None

# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------
def extract_text_from_pdf(uploaded_file):
    """Extracts text content from an uploaded PDF resume."""
    reader = pypdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

def analyze_resume(resume_text, job_role):
    """Sends resume text and target role to Groq for analysis and question generation."""
    if not client:
        return "Error: Groq API client is not initialized. Please set your GROQ_API_KEY."
    
    prompt = f"""
    You are an expert technical interviewer and career coach.
    Target Job Role: {job_role}
    
    Candidate Resume:
    {resume_text}
    
    Please provide:
    1. A brief professional assessment/feedback of the resume tailored for this role.
    2. 5 specific technical and behavioral interview questions based on this resume.
    3. Key improvement tips.
    """
    
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": "You are a professional AI interview coach."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"API Error: {str(e)}"

def evaluate_answer(question, user_answer):
    """Evaluates the candidate's mock interview answer."""
    if not client:
        return "Error: Groq client not initialized."
        
    prompt = f"""
    Interview Question: {question}
    Candidate's Answer: {user_answer}
    
    Evaluate this answer. Provide a rating out of 10, constructive feedback, and a model answer or suggestions for improvement.
    """
    
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": "You are a supportive, expert mock interviewer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"API Error: {str(e)}"

# ---------------------------------------------------------
# MAIN UI LAYOUT
# ---------------------------------------------------------
st.markdown("## 🎙️ AI-Powered Interview Copilot & Resume Coach")
st.markdown("Second-Year Mini-Project Prototype | AKGEC / AKTU Curriculum")
st.markdown("---")

# API Key Warning Banner if missing
if not client:
    st.error("⚠️ Groq API Client could not be initialized. Please set your `GROQ_API_KEY` in environment variables or Streamlit secrets.")

# Session State Initialization
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "resume_feedback" not in st.session_state:
    st.session_state.resume_feedback = ""
if "job_role" not in st.session_state:
    st.session_state.job_role = ""

# Sidebar Controls
with st.sidebar:
    st.header("⚙️ Configuration")
    input_key = st.text_input("Enter Groq API Key (gsk_...)", type="password")
    if input_key:
        os.environ["GROQ_API_KEY"] = input_key
        client = Groq(api_key=input_key)
        st.success("API Key updated successfully!")
        
    st.markdown("---")
    st.markdown("### About")
    st.info("This application uses **Groq** and **Meta Llama 3.3** to analyze student resumes and run interactive mock interviews with zero latency.")

# Step 1: Resume Upload & Analysis Section
st.subheader("Step 1: Upload Your Resume & Target Role")
col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
with col2:
    job_role = st.text_input("Target Job Role (e.g., Software Engineer, Data Analyst)")

if st.button("Analyze Resume & Generate Questions", type="primary"):
    if not uploaded_file:
        st.warning("Please upload a PDF resume first.")
    elif not job_role:
        st.warning("Please specify a target job role.")
    elif not client:
        st.error("Please provide a valid Groq API key.")
    else:
        with st.spinner("Analyzing resume with Groq Llama 3.3..."):
            st.session_state.resume_text = extract_text_from_pdf(uploaded_file)
            st.session_state.job_role = job_role
            st.session_state.resume_feedback = analyze_resume(st.session_state.resume_text, job_role)

# Display Feedback if available
if st.session_state.resume_feedback:
    st.markdown("---")
    st.subheader("📋 Resume Feedback & Interview Plan")
    st.write(st.session_state.resume_feedback)
    
    st.markdown("---")
    st.subheader("💬 Interactive Mock Interview Practice")
    question_to_practice = st.text_input("Enter a question from the interview prep list above to practice:")
    user_answer = st.text_area("Type your answer here:")
    
    if st.button("Evaluate My Answer"):
        if not question_to_practice or not user_answer:
            st.warning("Please enter both the question and your answer.")
        else:
            with st.spinner("Evaluating your response..."):
                evaluation = evaluate_answer(question_to_practice, user_answer)
                st.markdown("### 📊 Interviewer Evaluation")
                st.write(evaluation)