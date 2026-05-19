from db import SessionLocal, Interview
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
import re
from google import genai
client = genai.Client(api_key="AIzaSyD70h-ah9VXXAITQRfYqF2KC5DgtVnii4E")
app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    text = re.sub(r'(?<=\w)\s(?=\w)', '', text)

    # Convert multiple spaces/newlines into single space
    text = re.sub(r'\s+', ' ', text)

    return text.lower()


# -----------------------------
# Smart Question Generator
# -----------------------------
def generate_questions(resume_text):

    try:
        prompt = f"""
You are a senior technical interviewer.

From the resume below, generate exactly 8 strong interview questions.

Rules:
- Mix of technical + project + behavioral questions
- Must be specific to resume content
- No generic questions like "tell me about yourself"
- Return ONLY questions, one per line

Resume:
{resume_text}
"""

        response = client.models.generate_content(
            model="gemini-2.0-flash",   # IMPORTANT: change model
            contents=prompt
        )

        text = response.text.strip()

        questions = [
            line.strip("- ").strip()
            for line in text.split("\n")
            if line.strip()
        ]

        return questions[:8]

    except Exception as e:
        print("GEMINI ERROR:", e)

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
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

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

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return {
            "follow_up": response.text
        }

    except Exception as e:

        print("FOLLOW UP ERROR:", e)

        return {
            "follow_up": "Could not generate follow-up question."
        }    