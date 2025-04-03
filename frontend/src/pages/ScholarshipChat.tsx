// 📁 src/pages/ScholarshipChat.tsx
import React, { useState } from "react";
import axios from "axios";

interface Program {
  title: string;
  description: string;
  link: string;
}

const ScholarshipChat = () => {
  const [input, setInput] = useState("");
  const [chatHistory, setChatHistory] = useState<any[]>([]);
  const [loadingStep, setLoadingStep] = useState(0);

  const handleSend = async () => {
    if (!input.trim()) return;
    setChatHistory([...chatHistory, { role: "user", content: input }]);
    setLoadingStep(1);

    try {
      const response = await axios.post("http://localhost:8000/recommend", {
        query: input,
      });

      const merged_programs: Program[] = response.data.programs || [];
      setChatHistory((prev) => [...prev, { role: "ai", content: merged_programs }]);
    } catch (err) {
      alert("❌ 추천 실패: " + err);
    } finally {
      setInput("");
      setLoadingStep(0);
    }
  };

  return (
    <div style={{ maxWidth: 800, margin: "0 auto", padding: "2rem" }}>
      <h2>🎓 맞춤형 장학금/지원금 추천 챗봇</h2>
      <p>🔍 아래에 조건을 입력하면 적절한 장학금/지원금 제도와 접속 가능한 링크를 추천해드립니다.</p>

      <div style={{ marginTop: "1rem" }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="예: 이공계열 대학생 3학년입니다. 어떤 장학금이 있나요?"
          style={{ width: "100%", padding: "0.5rem", fontSize: "1rem" }}
        />
        <button onClick={handleSend} style={{ marginTop: "0.5rem" }}>
          전송
        </button>
      </div>

      {loadingStep > 0 && <p>🔄 추천 중...</p>}

      <div style={{ marginTop: "2rem" }}>
        {chatHistory.map((msg, idx) => (
          <div key={idx} style={{ marginBottom: "1.5rem" }}>
            {msg.role === "user" ? (
              <div style={{ backgroundColor: "#eef", padding: "0.5rem" }}>
                🧑 {msg.content}
              </div>
            ) : (
              <div style={{ backgroundColor: "#f9f9f9", padding: "0.5rem" }}>
                {msg.content.map((p: Program, i: number) => (
                  <div key={i} style={{ marginBottom: "1rem" }}>
                    <h4>📌 {p.title}</h4>
                    <p>{p.description}</p>
                    {p.link.startsWith("http") ? (
                      <a href={p.link} target="_blank" rel="noopener noreferrer">
                        🔗 공식 링크
                      </a>
                    ) : (
                      <p style={{ color: "red" }}>⚠️ 유효한 링크를 찾지 못했습니다.</p>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default ScholarshipChat;
