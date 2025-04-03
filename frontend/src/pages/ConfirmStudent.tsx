// 📄 src/pages/ConfirmStudent.tsx
import React from "react";
import { useNavigate } from "react-router-dom";

const ConfirmStudent = () => {
  const studentInfo = JSON.parse(localStorage.getItem("studentInfo") || "{}");
  const navigate = useNavigate();

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
        position: "relative",
        padding: "2rem",
        boxSizing: "border-box"
      }}
    >
      <h2 style={{ fontSize: "2rem", marginBottom: "2rem" }}>📊 학생 정보 확인</h2>
      <div style={{ textAlign: "center", marginBottom: "2rem" }}>
        <p style={{ marginBottom: "1rem" }}><strong>이름:</strong> {studentInfo.name}</p>
        <p style={{ marginBottom: "1rem" }}><strong>학번:</strong> {studentInfo.studentid}</p>
        <p style={{ marginBottom: "1rem" }}><strong>학과:</strong> {studentInfo.major}</p>
        <p style={{ marginBottom: "1rem" }}><strong>학년:</strong> {studentInfo.year}</p>
        <p style={{ marginBottom: "1rem" }}><strong>총 성적:</strong> {studentInfo.grade}</p>
      </div>

      <button
        onClick={() => navigate("/recommend")}
        style={{ padding: "0.8rem 2rem", fontSize: "1rem", cursor: "pointer", border: "none", backgroundColor: "#f3f3f3", borderRadius: "8px" }}
      >
        장학금 확인하기
      </button>

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

export default ConfirmStudent;
