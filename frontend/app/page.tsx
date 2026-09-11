"use client";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

import { useState } from "react";
import axios from "axios";

export default function Home() {

  const [followUp, setFollowUp] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [questions, setQuestions] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [evaluating, setEvaluating] = useState(false);
  const [answer, setAnswer] = useState("");
  const [evaluation, setEvaluation] = useState<any>(null);
  const [technicalScore, setTechnicalScore] = useState("");
  const [communicationScore, setCommunicationScore] = useState("");
  const [confidenceLevel, setConfidenceLevel] = useState("");
  const [answerError, setAnswerError] = useState("");
  const API_URL = "https://ai-interview-copilot-backend-cpmc.onrender.com";
  // ----------------------------
  // File Validation
  // ----------------------------
  const handleFileChange = (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {

    const selectedFile = e.target.files?.[0];

    if (!selectedFile) return;

    if (selectedFile.type !== "application/pdf") {

      setError("Please upload PDF files only.");
      setFile(null);
      return;
    }

    setError("");
    setFile(selectedFile);
  };

  // ----------------------------
  // Upload Resume
  // ----------------------------
  const uploadResume = async () => {

    if (!file) {

      setError("Please select a PDF resume first.");
      return;
    }

    setLoading(true);

    try {

      const formData = new FormData();
      formData.append("file", file);

      const res = await axios.post(
  `${API_URL}/upload-resume`,
  formData,
  {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  }
);

      setQuestions(res.data.questions);
      setEvaluation(null);
      setAnswer("");
      setError("");

    } catch (error) {

      console.error(error);
      setError("Something went wrong while uploading.");
    }

    setLoading(false);
  };

  // ----------------------------
  // Evaluate Answer
  // ----------------------------
  const evaluateAnswer = async () => {

    const cleanedAnswer = answer.trim();

    if (!cleanedAnswer || cleanedAnswer === ".") {

      setAnswerError("Please enter a valid answer.");
      return;
    }

    setAnswerError("");
    setEvaluating(true);

    try {

      const res = await axios.post(
  `${API_URL}/evaluate-answer`,
  {
    answer,
    resume_name: file?.name,
    questions,
  }
);

      setEvaluation(res.data);

      const text = res.data.evaluation;

      const techMatch = text.match(/Technical Score:\s*(.*)/);
      const commMatch = text.match(/Communication Score:\s*(.*)/);
      const confidenceMatch = text.match(/Confidence Level:\s*(.*)/);

      setTechnicalScore(techMatch ? techMatch[1] : "");
      setCommunicationScore(commMatch ? commMatch[1] : "");
      setConfidenceLevel(confidenceMatch ? confidenceMatch[1] : "");

    } catch (error) {

      console.error(error);
      setError("Failed to evaluate answer.");
    }

    setEvaluating(false);
  };

  // ----------------------------
  // Voice Recognition
  // ----------------------------
  const startListening = () => {

    const SpeechRecognition =
      (window as any).SpeechRecognition ||
      (window as any).webkitSpeechRecognition;

    if (!SpeechRecognition) {

      alert("Speech Recognition not supported in this browser");
      return;
    }

    const recognition = new SpeechRecognition();

    recognition.lang = "en-US";

    recognition.onresult = (event: any) => {

      const transcript = event.results[0][0].transcript;

      setAnswer(transcript);
    };

    recognition.start();
  };

  // ----------------------------
  // Generate Follow-up Question
  // ----------------------------
  const generateFollowUp = async () => {

    try {

      const res = await axios.post(
    `${API_URL}/follow-up`,
  {
    answer,
  }
);

      setFollowUp(res.data.follow_up);

    } catch (error) {

      console.error(error);
    }
  };

  return (

    <main className="min-h-screen bg-gray-100 p-10">

      <div className="max-w-3xl mx-auto bg-white shadow-2xl rounded-3xl p-10">

        {/* Title */}
        <h1 className="text-4xl font-bold text-center text-blue-600 mb-6">
          AI Interview Copilot
        </h1>

        <p className="text-center text-gray-500 mb-8">
          Upload your resume and generate AI-powered interview questions
        </p>

        {/* Upload Section */}
        <div className="flex flex-col items-center gap-4">

          <label className="w-full flex flex-col items-center justify-center border-2 border-dashed border-blue-400 rounded-2xl p-8 cursor-pointer bg-blue-50 hover:bg-blue-100 transition">

            <span className="text-lg font-medium text-blue-600">
              Click to Upload Resume
            </span>

            <span className="text-sm text-gray-500 mt-2">
              PDF only
            </span>

            {file && (

              <span className="mt-4 text-green-600 font-semibold">
                {file.name}
              </span>
            )}

            <input
              type="file"
              accept=".pdf"
              className="hidden"
              onChange={handleFileChange}
            />

          </label>

          {/* Error Message */}
          {error && (

            <div className="bg-red-100 text-red-600 px-4 py-2 rounded-lg w-full text-center">
              {error}
            </div>
          )}

          {/* Upload Button */}
          <button
            onClick={uploadResume}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl transition duration-300"
          >
            Upload Resume
          </button>

        </div>

        {/* Loading */}
        {loading && (

          <div className="text-center mt-6 text-blue-600 font-semibold">
            Generating AI Questions...
          </div>
        )}

        {/* Questions */}
        <div className="mt-10 space-y-4">

          {questions.map((q, i) => (

            <div
              key={i}
              className="bg-gray-50 border-l-4 border-blue-500 p-5 rounded-xl shadow"
            >
              <p className="font-medium text-gray-700">
                {q}
              </p>
            </div>
          ))}

        </div>

        {/* Answer Section */}
        {questions.length > 0 && (

          <div className="mt-12">

            <h2 className="text-2xl font-bold mb-4 text-green-600">
              Mock Interview Answer
            </h2>

            <textarea
              value={answer}
              onChange={(e) => {

                setAnswer(e.target.value);
                setAnswerError("");
              }}
              placeholder="Type your interview answer here..."
              className="w-full border p-4 rounded-xl h-40 focus:outline-none focus:ring-2 focus:ring-green-400"
            />

            {answerError && (

              <div className="mt-3 bg-red-100 text-red-600 px-4 py-2 rounded-xl">
                {answerError}
              </div>
            )}

            {/* Buttons */}
            <div className="flex gap-4 mt-4 flex-wrap">

              <button
                type="button"
                onClick={startListening}
                className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-xl transition duration-300"
              >
                🎤 Start Speaking
              </button>

              <button
                type="button"
                onClick={evaluateAnswer}
                className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-xl transition duration-300"
              >
                {evaluating ? "Evaluating..." : "Evaluate Answer"}
              </button>

              <button
                type="button"
                onClick={generateFollowUp}
                className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-xl transition duration-300"
              >
                Generate Follow-up Question
              </button>

            </div>

            {/* Follow-up Question */}
            {followUp && (

              <div className="mt-6 bg-purple-50 border-l-4 border-purple-500 p-5 rounded-xl">

                <h3 className="text-xl font-bold text-purple-700 mb-2">
                  AI Follow-up Question
                </h3>

                <p className="text-gray-700">
                  {followUp}
                </p>

              </div>
            )}

            {/* Evaluation Result */}
            {evaluation && (

              <div className="mt-8 bg-gray-50 border rounded-2xl p-6 shadow">

                {/* Title */}
                <h3 className="text-2xl font-bold text-green-600 mb-4">
                  AI Evaluation Scores
                </h3>

                {/* Chart */}
                <ResponsiveContainer width="100%" height={300}>

                  <BarChart
                    data={[
                      {
                        name: "Technical",
                        score: parseInt(technicalScore) || 0
                      },
                      {
                        name: "Communication",
                        score: parseInt(communicationScore) || 0
                      },
                      {
                        name: "Confidence",
                        score:
                          confidenceLevel === "High"
                            ? 10
                            : confidenceLevel === "Medium"
                            ? 7
                            : confidenceLevel === "Low"
                            ? 4
                            : 0,
                      },
                    ]}
                    margin={{
                      top: 20,
                      right: 30,
                      left: 20,
                      bottom: 5
                    }}
                  >

                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis domain={[0, 10]} />
                    <Tooltip />
                    <Bar
                      dataKey="score"
                      fill="#4ade80"
                      barSize={60}
                    />

                  </BarChart>

                </ResponsiveContainer>

                {/* Feedback */}
                <h3 className="text-2xl font-bold text-green-600 mt-6 mb-4">
                  AI Interview Feedback
                </h3>

                <div className="whitespace-pre-wrap text-gray-700 leading-8 max-h-96 overflow-y-auto">
                  {evaluation.evaluation}
                </div>

              </div>
            )}

          </div>
        )}

      </div>

    </main>
  );
}