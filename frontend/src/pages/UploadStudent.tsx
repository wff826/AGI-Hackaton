// 📄 src/pages/UploadStudent.tsx
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const UploadStudent = () => {
  const [enrollmentFile, setEnrollmentFile] = useState<File | null>(null);
  const [gradeFile, setGradeFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleUpload = async () => {
    if (!enrollmentFile || !gradeFile) return;
    const formData = new FormData();
    formData.append("enrollment_file", enrollmentFile);
    formData.append("grade_file", gradeFile);

    setUploading(true);
    try {
      const res = await fetch("http://localhost:8000/upload/student", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      localStorage.setItem("studentInfo", JSON.stringify(data.student));
      setMessage("✅ 업로드 완료");
    } catch (err) {
      setMessage("❌ 업로드 실패");
    } finally {
      setUploading(false);
    }
  };

  const goToNext = () => {
    navigate("/confirm");
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
        position: "relative",
      }}
    >
      <h2 style={{ fontSize: "2rem", marginBottom: "2rem" }}>📑 학생 문서 업로드</h2>

      <div style={{ marginBottom: "1rem" }}>
        <label>재학증명서 업로드: </label>
        <input
          type="file"
          accept="application/pdf,image/jpeg,image/jpg"
          onChange={(e) => setEnrollmentFile(e.target.files?.[0] || null)}
        />
      </div>

      <div style={{ marginBottom: "1rem" }}>
        <label>성적증명서 업로드: </label>
        <input
          type="file"
          accept="application/pdf,image/jpeg,image/jpg"
          onChange={(e) => setGradeFile(e.target.files?.[0] || null)}
        />
      </div>

      <button onClick={handleUpload} disabled={uploading} style={{ marginBottom: "1rem" }}>
        {uploading ? "업로드 중..." : "문서 확인하기"}
      </button>

      {message && <p style={{ marginBottom: "1rem" }}>{message}</p>}

      {message === "✅ 업로드 완료" && (
        <button
          style={{ marginBottom: "1rem" }}
          onClick={goToNext}
        >
          다음으로
        </button>
      )}

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

export default UploadStudent;
