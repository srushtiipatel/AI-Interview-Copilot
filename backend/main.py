from db import SessionLocal, Interview
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
import re
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://ai-interview-copilot-backend-cpmc.onrender.com",
        ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Extract text from PDF
# -----------------------------
def extract_text(file):

    reader = PdfReader(file)
    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text

    # -----------------------------
    # CLEAN TEXT
    # -----------------------------

    # Remove extra spaces between letters
    # Convert multiple spaces/newlines into single space
# Fix PDFs that extract as spaced characters
    text = re.sub(r'(\b\w\b\s)+\b\w\b', lambda m: m.group().replace(" ", ""), text)

# Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.replace(" . ", ". ")
    text = text.replace(" , ", ", ")
    text = text.replace(" - ", "-")

    text = text.strip()
    return text


# -----------------------------
# Smart Question Generator
# -----------------------------
def generate_questions(resume_text):
    resume_text = resume_text[:4000]

    try:
        print("\n===== RESUME TEXT =====")
        print(resume_text[:3000])
        print("=======================\n")

        prompt = f"""
You are a senior technical interviewer.

Analyze the candidate's resume carefully.

Generate exactly 8 interview questions.

Requirements:
- Questions must be specific to the candidate's resume.
- Mention project names when available.
- Mention technologies, frameworks, and skills from the resume.
- Ask about architecture, challenges, implementation details, trade-offs, and outcomes.
- Avoid generic questions.

Return exactly 8 questions.

Each question must be on a new line.

Do not include numbering, bullets, headings, or explanations.

Resume:

{resume_text}
"""

        response = model.generate_content(prompt)

        text = response.text.strip()

        print("\n===== GEMINI TEXT =====")
        print(repr(text))

        questions = [
            line.strip()
            for line in text.split("\n")
            if line.strip()
        ]

        print("\n===== PARSED QUESTIONS =====")
        print(questions)

        return questions[:8]

    except Exception as e:
        print("\n===== GEMINI ERROR =====")
        print(repr(e))

        return [
            "Tell me about a challenging project you worked on.",
            "How did you design your last project architecture?",
            "What technologies did you use in your resume projects?",
            "Explain a bug you solved recently.",
            "How do you handle deadlines in projects?"
        ]
# -----------------------------
# Home Route
# -----------------------------
@app.get("/")
def home():
    return {"message": "AI Interview Copilot Backend Running"}


# -----------------------------
# Resume Upload Route
# -----------------------------
@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    text = extract_text(file.file)

    questions = generate_questions(text)

    return {
        "questions": questions
    }

@app.post("/evaluate-answer")
async def evaluate_answer(data: dict):
    try:
        # 1️⃣ Get answer and resume info
        answer = data.get("answer", "")
        resume_name = data.get("resume_name", "unknown.pdf")
        questions = data.get("questions", [])  # list of questions if available

        # 2️⃣ Prepare Gemini AI prompt
        prompt = f"""
You are an expert technical interviewer.

Evaluate this interview answer professionally but encourage the candidate politely.

Answer:
{answer}

Return response ONLY in this format:

Technical Score: number/10
Communication Score: number/10
Confidence Level: High/Medium/Low
Strengths: short paragraph
Improvements: short paragraph
Final Verdict: short paragraph
"""

        # 3️⃣ Call Gemini AI
        response = model.generate_content(prompt)

        # 4️⃣ Clean text
        cleaned_text = response.text.replace("*", "")

        # 5️⃣ SAVE INTERVIEW TO DATABASE (Step 5)
        db = SessionLocal()
        interview_entry = Interview(
            resume_name=resume_name,
            questions="\n".join(questions),
            answer=answer,
            technical_score="",  # optional: parse from cleaned_text if you want
            communication_score="",
            confidence=""
        )
        db.add(interview_entry)
        db.commit()
        db.close()

        # 6️⃣ Return evaluation to frontend
        return {
            "evaluation": cleaned_text
        }

    except Exception as e:
        print("EVALUATION ERROR:", e)
        return {
            "evaluation": "AI evaluation failed."
        }
    
# ----------------------------
# Generate Follow-up Question
# ----------------------------
@app.post("/follow-up")
async def follow_up(data: dict):

    try:

        answer = data.get("answer", "")

        prompt = f"""
You are an expert technical interviewer.

Based on this candidate answer, generate ONE smart follow-up interview question.

Candidate Answer:
{answer}

Return only the follow-up question.
"""

        response = model.generate_content(prompt)

        return {
            "follow_up": response.text
        }

    except Exception as e:

        print("FOLLOW UP ERROR:", e)

        return {
            "follow_up": "Could not generate follow-up question."
        }    