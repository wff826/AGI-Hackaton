import React, { useState } from "react";

const UploadStudent = () => {
  const [enrollmentFile, setEnrollmentFile] = useState<File | null>(null);
  const [gradeFile, setGradeFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");

  const handleUpload = async () => {
    if (!enrollmentFile || !gradeFile) {
      setMessage("두 문서를 모두 업로드해주세요.");
      return;
    }

    const formData = new FormData();
    formData.append("enrollment", enrollmentFile);
    formData.append("grade", gradeFile);

    setUploading(true);
    setMessage("업로드 중...");

    try {
      const res = await fetch("http://localhost:8000/upload/student", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setMessage("✅ 업로드 완료: " + JSON.stringify(data));
    } catch (err) {
      console.error(err);
      setMessage("❌ 업로드 실패");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div style={{ padding: "2rem", textAlign: "center" }}>
      <h2>📚 학생 문서 업로드</h2>

      <div style={{ margin: "1rem 0" }}>
        <label>📄 재학증명서 업로드: </label>
        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setEnrollmentFile(e.target.files?.[0] || null)}
        />
      </div>

      <div style={{ margin: "1rem 0" }}>
        <label>📄 성적증명서 업로드: </label>
        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setGradeFile(e.target.files?.[0] || null)}
        />
      </div>

      <button onClick={handleUpload} disabled={uploading}>
        {uploading ? "업로드 중..." : "문서 확인하기"}
      </button>

      {message && <p style={{ marginTop: "1rem" }}>{message}</p>}
    </div>
  );
};

export default UploadStudent;
