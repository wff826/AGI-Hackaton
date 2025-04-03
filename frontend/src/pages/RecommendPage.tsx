// 📄 src/pages/RecommendPage.tsx
import React, { useEffect, useState } from "react";

interface Program {
  title: string;
  description: string;
  link: string;
}

const RecommendPage = () => {
  const [programs, setPrograms] = useState<Program[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [userInput, setUserInput] = useState("");

  const handleSubmit = async () => {
    if (!userInput.trim()) return;

    setLoading(true);
    setError("");
    try {
      const res = await fetch("http://localhost:8000/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: userInput })
      });
      const data = await res.json();
      setPrograms(data.programs);
    } catch (err) {
      setError("❌ 추천 실패. 다시 시도해주세요.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        height: "100vh",
        width: "100vw",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: "#fff",
        padding: "2rem",
        position: "relative",
        boxSizing: "border-box"
      }}
    >
      <h2 style={{ fontSize: "2rem", marginBottom: "1rem" }}>🎯 장학금 추천 결과</h2>

      <div style={{ width: "100%", maxWidth: "700px", textAlign: "center" }}>
        <input
          type="text"
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          placeholder="예: 이공계 대학생 3학년"
          style={{
            width: "100%",
            padding: "0.8rem",
            fontSize: "1rem",
            marginBottom: "1rem",
            boxSizing: "border-box"
          }}
        />
        <button
          onClick={handleSubmit}
          disabled={loading}
          style={{ padding: "0.5rem 1.5rem", fontSize: "1rem", cursor: "pointer", borderRadius: "8px", border: "none", backgroundColor: "#f3f3f3" }}
        >
          {loading ? "추천 중..." : "장학금 추천받기"}
        </button>

        {error && <p style={{ color: "red", marginTop: "1rem" }}>{error}</p>}

        <div style={{ marginTop: "2rem", textAlign: "left" }}>
          {programs.map((p, i) => (
            <div key={i} style={{ marginBottom: "1.5rem" }}>
              <h3>📌 {p.title}</h3>
              <p>{p.description}</p>
              {p.link.startsWith("http") ? (
                <a href={p.link} target="_blank" rel="noopener noreferrer">
                  🔗 공식 링크
                </a>
              ) : (
                <span style={{ color: "#888" }}>{p.link}</span>
              )}
            </div>
          ))}
        </div>
      </div>

      <p
        style={{
          position: "absolute",
          bottom: "1rem",
          fontSize: "0.8rem",
          color: "#aaa",
        }}
      >
        ⓒ 2025 JARVIS Corp.
      </p>
    </div>
  );
};

export default RecommendPage;
