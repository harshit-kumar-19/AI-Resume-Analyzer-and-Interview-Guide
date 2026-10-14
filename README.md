Project Overview: AI Resume Analyzer & Mock Interview Copilot

The AI Resume Analyzer & Mock Interview Copilot is a full-stack, AI-powered career preparation web application designed to help job seekers optimize their resumes and practice real-time technical and behavioral mock interviews.


Key Features & Capabilities

# Resume Parsing & Assessment: Users upload their resume in PDF format (pypdf) alongside a target job role. The app extracts text and evaluates alignment, providing actionable resume feedback and highlighting areas for improvement.

# Custom Question Generation: Dynamically generates 5 tailored interview questions based on specific candidate experiences and job requirements.

# Interactive Mock Interviews & Instant Feedback: Candidates input answers to interview questions and receive detailed evaluations, including numerical ratings (out of 10), constructive feedback, and sample model answers.


Technical Stack & Architecture

# Frontend/UI: Built with Streamlit for a modern, responsive web application interface.

# AI Engine: Powered by Groq Cloud API (llama-3.3-70b-versatile / llama-3.1-8b-instant), delivering high-speed, zero-latency inference for real-time coaching responses.

# Deployment & Security: Deployed publicly on Streamlit Community Cloud, utilizing Streamlit Secrets management to isolate and safeguard API credentials securely away from the source code repository on GitHub.
