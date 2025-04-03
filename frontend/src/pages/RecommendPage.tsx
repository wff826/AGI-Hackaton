// 📄 src/pages/RecommendPage.tsx
import React, { useState } from "react";

interface Program {
  title: string;
  description: string;
  link: string;
}

const RecommendPage = () => {
  const [programs, setPrograms] = useState<Program[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFetch = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await fetch("http://localhost:8000/recommend-programs");
      const data = await res.json();
      setPrograms(data.programs);
    } catch (err) {
      setError("❌ 추천을 불러오는 데 실패했습니다.");
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
        boxSizing: "border-box",
        position: "relative",
      }}
    >
      <h2 style={{ fontSize: "2rem", marginBottom: "1rem" }}>🎯 장학금 추천 결과</h2>

      <button
        onClick={handleFetch}
        disabled={loading}
        style={{
          padding: "0.8rem 2rem",
          fontSize: "1rem",
          border: "none",
          backgroundColor: "#f3f3f3",
          borderRadius: "8px",
          cursor: "pointer",
          marginBottom: "2rem",
        }}
      >
        {loading ? "불러오는 중..." : "장학금 추천 확인하기"}
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <div style={{ width: "100%", maxWidth: "800px", textAlign: "left" }}>
        {programs.map((p, i) => (
          <div key={i} style={{ marginBottom: "1.5rem" }}>
            <h3>📌 {p.title}</h3>
            <p>{p.description}</p>
            {p.link?.startsWith("http") ? (
              <a href={p.link} target="_blank" rel="noopener noreferrer">
                🔗 공식 링크
              </a>
            ) : (
              <span style={{ color: "#888" }}>{p.link}</span>
            )}
          </div>
        ))}
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
