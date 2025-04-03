import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import UploadStudent from "./pages/UploadStudent";
import UploadGeneral from "./pages/UploadGeneral";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/upload-student" element={<UploadStudent />} />
        <Route path="/upload-general" element={<UploadGeneral />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
