import React from "react";
import { useNavigate } from "react-router-dom"; // ✅ added
import "./HomePage.css";
import Pomodoro from "./Component/Pomodoro";
import { useState } from "react";

const HomePage = ({ setShowStudySchedule }) => {
  const navigate = useNavigate(); // ✅ added
  const [showPomodoro, setShowPomodoro] = useState(false);


  const features = [
    {
      icon: "📚",
      title: "Chat with PDF + AI Study Planner",
      description:
        "Ask questions about your documents and plan your study schedule with us!",
      action: () => window.open("https://huggingface.co/spaces/Zara-fatima/x"),
      variant: "pdf",
    },
    {
      icon: "⏱️",
      title: "Pomodoro Sessions",
      description: "Focus with timed study sessions",
      action: () => setShowPomodoro(true),
      variant: "timer",
    },
    {
      icon: "📇",
      title: "Generate flashcards",
      description: "generate flashcards",
      action: () => alert("Coming soon!"),
      variant: "timer",
    },
    {
      icon: "👥",
      title: "Engage in Study group discussions!",
      description: "Collaborate with classmates",
      action: () => navigate("/forums"), // ✅ updated
      variant: "groups",
    },
  ];

  return (
    <div className="homepage">
      <div className="container">
        {/* Header */}
        <header className="header">
          <h1 className="title">StudyBuddy</h1>
          <p className="subtitle">Your personal learning assistant</p>
        </header>

        {/* Features Grid */}
        <div className="features-grid">
          {features.map((feature, index) => (
            <div
              key={index}
              onClick={feature.action}
              className={`feature-card feature-card-${feature.variant}`}
            >
              <div className="feature-icon">{feature.icon}</div>
              <h3 className="feature-title">{feature.title}</h3>
              <p className="feature-desc">{feature.description}</p>
            </div>
          ))}
        </div>
        {/* Pomodoro Section */}
        {showPomodoro && (
          <div className="pomodoro-wrapper">
            <Pomodoro />
            <button
              onClick={() => setShowPomodoro(false)}
              className="close-btn"
            >
              Close Pomodoro
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default HomePage;
