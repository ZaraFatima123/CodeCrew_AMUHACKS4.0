// src/pages/Home.jsx
const features = [
    {
      title: "AI with PDF (RAG)",
      description: "Upload and chat with your PDF documents using advanced AI",
      path: "http://127.0.0.1:7860", // Your backend URL
      icon: "📄",
      color: "bg-blue-100",
      external: true // Flag to indicate this is an external link
    },
    {
      title: "Study Planner",
      description: "Create and manage your study schedule effectively",
      path: "/study-planner",
      icon: "📅",
      color: "bg-green-100",
      external: false
    },
    {
      title: "Live Pomodoro",
      description: "Boost productivity with the Pomodoro technique",
      path: "/pomodoro",
      icon: "⏱️",
      color: "bg-red-100",
      external: false
    },
    {
      title: "Join Our Community",
      description: "Connect with other learners and share knowledge",
      path: "/community",
      icon: "👥",
      color: "bg-purple-100",
      external: false
    }
  ];

  // In your Home.jsx mapping
{features.map((feature, index) => (
    <FeatureCard 
      key={index}
      title={feature.title}
      description={feature.description}
      path={feature.path}
      icon={feature.icon}
      color={feature.color}
      external={feature.external}
    />
  ))}