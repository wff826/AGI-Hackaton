// 파일: src/pages/StartPage.tsx
import React from "react";
import { useNavigate } from "react-router-dom";

const StartPage = () => {
  const navigate = useNavigate();

  return (
    <div
      style={{
        height: "100vh",
        width: "100vw",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
        textAlign: "center",
        margin: "0",
        padding: "0",
        backgroundColor: "#fff",
      }}
    >
      <div
        style={{
          maxWidth: "960px",
          width: "100%",
          margin: "0 auto",
        }}
      >
        <h1 style={{ fontSize: "3rem", marginBottom: "1.5rem" }}>
          🎓 AI 장학금 추천 서비스
        </h1>
        <p style={{ fontSize: "1.2rem", marginBottom: "2rem" }}>
          AI가 문서를 분석해 적합한 장학금을 추천해줍니다.
        </p>
        <button
          onClick={() => navigate("/upload")}
          style={{
            padding: "0.8rem 2rem",
            fontSize: "1rem",
            cursor: "pointer",
            border: "none",
            backgroundColor: "#f3f3f3",
            borderRadius: "8px",
          }}
        >
          시작하기
        </button>
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

export default StartPage;
