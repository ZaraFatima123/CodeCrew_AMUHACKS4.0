// // import React from 'react';
// import HomePage from './HomePage';

// function App() {
//   return (
//     <HomePage />
//   );
// }

// export default App;

import React, { useState } from 'react';
import HomePage from './HomePage';

function App() {
  const [showStudySchedule, setShowStudySchedule] = useState(false);

  return (
    <HomePage setShowStudySchedule={setShowStudySchedule} />
    
  );
}

export default App;

