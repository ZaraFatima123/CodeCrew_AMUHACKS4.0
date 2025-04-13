import React from "react";
import "../App.css";

export default function Pomodoro() {
  const videos = [
    {
      title: "4-Hour Study with Me | Pomodoro Timer 60-10 | Lo-Fi",
      url: "https://www.youtube.com/embed/vC4dLeqnvAw",
    },
    {
      title: "Pomodoro Timer 3x30 (1.5hr) | ADHD | Let's get focused!",
      url: "https://www.youtube.com/embed/brnafxH_0E8",
    },
    {
      title: "25/5 Pomodoro Timer - Relaxing Lofi, Deep Focus",
      url: "https://www.youtube.com/embed/DyiPr9jkW38",
    },
    {
      title: "STUDY WITH ME 4hrs with breaks 50/10 pomodoro (no music)",
      url: "https://www.youtube.com/embed/ZEbCz7B2-Eg",
    },
    {
      title: "3-HOUR STUDY WITH ME Pomodoro 25/5 [with Rain Sounds] No",
      url: "https://www.youtube.com/embed/Ud5nv8CIZiM",
    },
  ];

  const resources = [
    {
      title: "Pomofocus - Customizable Pomodoro Timer",
      url: "https://pomofocus.io/",
    },
    {
      title: "TomatoTimers - Simple Pomodoro Timer",
      url: "https://www.tomatotimers.com/",
    },
    {
      title: "The Pomodoro Technique (Official Site)",
      url: "https://www.pomodorotechnique.com",
    },
    {
      title: "Best Apps for Pomodoro Technique",
      url: "https://zapier.com/blog/best-pomodoro-apps/",
    },
  ];

  return (
    <div className="pomodoro-container">
      <h1 className="pomodoro-title">Pomodoro Sessions</h1>
      <p className="pomodoro-description">
        Use these Pomodoro sessions to stay focused and productive.
      </p>

      {/* Video Section */}
      <div className="video-grid">
        {videos.map((video, index) => (
          <iframe
            key={index}
            className="video-iframe"
            src={video.url}
            title={video.title}
            allowFullScreen
          ></iframe>
        ))}
      </div>

      {/* Resources Section */}
      <div className="pomodoro-resources">
        <h2>📚 Useful Links:</h2>
        <ul>
          {resources.map((resource, index) => (
            <li key={index}>
              <a href={resource.url} target="_blank" rel="noopener noreferrer">
                {resource.title}
              </a>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
