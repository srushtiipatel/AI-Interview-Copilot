# 🤖 AI Interview Copilot

AI Interview Copilot is an AI-powered web application that helps users prepare for technical interviews by analyzing their resume, generating personalized interview questions using Google's Gemini AI, and evaluating their responses with detailed feedback.

---

## 🚀 Live Demo

### 🌐 Frontend (Vercel)

https://ai-interview-copilot-olive.vercel.app/

### ⚡ Backend API (Railway)

https://ai-interview-copilot-production-8295.up.railway.app

---

# ✨ Features

- 📄 Upload Resume (PDF)
- 🤖 AI-generated interview questions
- 💬 AI-powered answer evaluation
- 📊 Technical Score
- 🗣️ Communication Score
- 💪 Confidence Score
- ⚡ FastAPI backend
- 🎨 Responsive Next.js frontend
- ☁️ Deployed using Railway & Vercel

---

# 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Frontend | Next.js, TypeScript |
| Backend | FastAPI |
| AI Model | Google Gemini 2.5 Flash |
| Database | SQLite |
| Deployment | Vercel, Railway |
| Version Control | Git & GitHub |

---

# 🏗️ Project Architecture

```
                User
                  │
                  ▼
     Next.js Frontend (Vercel)
                  │
                  ▼
      FastAPI Backend (Railway)
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
   Gemini AI API         SQLite
```

---

# 📂 Project Structure

```
AI-Interview-Copilot
│
├── backend
│   ├── main.py
│   ├── requirements.txt
│   ├── db.py
│   └── ...
│
├── frontend
│   ├── app
│   ├── public
│   ├── package.json
│   └── ...
│
└── README.md
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/srushtiipatel/AI-Interview-Copilot.git
```

---

## Backend Setup

```bash
cd backend

python -m venv .venv

pip install -r requirements.txt

uvicorn main:app --reload
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

---

# 📸 Screenshots

### Home Page

<img width="1416" height="731" alt="image" src="https://github.com/user-attachments/assets/ef9a57c5-4137-4dae-84e4-6e713822346f" />


---

### Resume Upload

<img width="1202" height="901" alt="image" src="https://github.com/user-attachments/assets/5643677f-cd20-47ec-bb1a-425565478f5c" />


---

### AI Generated Questions

<img width="728" height="883" alt="image" src="https://github.com/user-attachments/assets/99f6ded5-f192-419d-8f1f-e8e84fa9522f" />


---

### Interview Evaluation

<img width="566" height="903" alt="image" src="https://github.com/user-attachments/assets/cc5e004d-ae68-4f4f-af98-2c8d9972c4ad" />



---

# 🎯 Future Improvements

- 🎤 Voice-based interview simulation
- 🔐 User Authentication
- 📈 Interview History Dashboard
- 📄 Downloadable Feedback Report
- 🌙 Dark Mode
- 📱 Mobile Optimization

---

# 👩‍💻 Author

**Srushti Patel**

GitHub:
https://github.com/srushtiipatel

LinkedIn:
www.linkedin.com/in/srushti-patel-539486303

---

# ⭐ If you found this project helpful, consider giving it a Star!
