import React from 'react';
import { useNavigate } from 'react-router-dom'; // ✅ added
import './HomePage.css';

const HomePage = ({ setShowStudySchedule }) => {
  const navigate = useNavigate(); // ✅ added

  const features = [
    {
      icon: '📚',
      title: 'Chat with PDF + AI Study Planner',
      description: 'Ask questions about your documents and plan your study schedule with us!',
      action: () => window.open('https://huggingface.co/spaces/Zara-fatima/x'),
      variant: 'pdf'
    },
    {
      icon: '⏱️',
      title: 'Pomodoro Timer',
      description: 'Focus with timed study sessions',
      action: () => alert('Coming soon!'),
      variant: 'timer'
    },
    {
      icon: '📇',
      title: 'Generate flashcards',
      description: 'generate flashcards',
      action: () => alert('Coming soon!'),
      variant: 'timer'
    },
    {
      icon: '👥',
      title: 'Engage in Study group discussions!',
      description: 'Collaborate with classmates',
      action: () => navigate('/forums'), // ✅ updated
      variant: 'groups'
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

      </div>
    </div>
  );
};

export default HomePage;
