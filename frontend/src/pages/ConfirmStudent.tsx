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
        padding: "1rem"
      }}
    >
      <h2 style={{ fontSize: "2rem", marginBottom: "2rem" }}>📊 학생 정보 확인</h2>
      <ul style={{ listStyle: "none", padding: 0, marginBottom: "2rem", textAlign: "center" }}>
        <li style={{ marginBottom: "0.5rem" }}><strong>이름:</strong> {studentInfo.name}</li>
        <li style={{ marginBottom: "0.5rem" }}><strong>학번:</strong> {studentInfo.studentid}</li>
        <li style={{ marginBottom: "0.5rem" }}><strong>학과:</strong> {studentInfo.major}</li>
        <li style={{ marginBottom: "0.5rem" }}><strong>학년:</strong> {studentInfo.year}</li>
        <li style={{ marginBottom: "0.5rem" }}><strong>총 성적:</strong> {studentInfo.grade}</li>
      </ul>

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
