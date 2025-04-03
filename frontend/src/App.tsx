// App.tsx
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import StartPage from "./pages/StartPage";
import UploadStudent from "./pages/UploadStudent";
import ConfirmStudent from "./pages/ConfirmStudent";
import RecommendPage from "./pages/RecommendPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<StartPage />} />
        <Route path="/upload" element={<UploadStudent />} />
        <Route path="/confirm" element={<ConfirmStudent />} />
        <Route path="/recommend" element={<RecommendPage />} />
      </Routes>
    </Router>
  );
}

export default App;
