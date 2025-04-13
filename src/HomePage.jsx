import React from 'react';
import './HomePage.css';

const HomePage = () => {
  const features = [
    {
      icon: '📚',
      title: 'Chat with PDF',
      description: 'Ask questions about your documents',
      action: () => window.open('http://127.0.0.1:7860', '_blank'),
      variant: 'pdf'
    },
    {
      icon: ' 📋',
      title: 'AI Study Planner',
      description: 'Upload your syllabus and get tailored schedule to study!',
      action: () => alert('Coming soon!'),
      variant: 'stats'
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
      title: 'Study Groups',
      description: 'Collaborate with classmates',
      action: () => alert('Coming soon!'),
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

        {/* Footer */}
      </div>
    </div>
  );
};

export default HomePage;
