import Upload from "./components/Upload";

function App() {
  return (
    <div className="flex flex-col items-center p-8 min-h-screen bg-gray-50">
      <h1 className="text-3xl font-bold mb-2">정부 지원금 추천</h1>
      <p className="mb-6 text-gray-500">PDF 문서를 업로드하고 추천을 받아보세요!</p>
      
      <Upload />
      
      <footer className="mt-auto text-sm text-gray-400 pt-10">
        © 2025 JARVIS. All rights reserved.
      </footer>
    </div>
  );
}

export default App;
