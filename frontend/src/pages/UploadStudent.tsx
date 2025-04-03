import React, { useState } from "react";

const UploadStudent = () => {
  const [enrollmentFile, setEnrollmentFile] = useState<File | null>(null);
  const [gradeFile, setGradeFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");
  const [rawText, setRawText] = useState("");
  const [extracted, setExtracted] = useState<Record<string, any> | null>(null);

  const handleUpload = async () => {
    if (!enrollmentFile || !gradeFile) {
      setMessage("❗ 두 문서를 모두 업로드해주세요.");
      return;
    }

    const formData = new FormData();
    formData.append("enrollment", enrollmentFile);
    formData.append("grade", gradeFile);

    setUploading(true);
    setMessage("📤 업로드 중...");

    try {
      const res = await fetch("http://localhost:8000/upload/student", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setRawText(data.raw_text || "");
      setExtracted(data.extracted_info || null);
      setMessage("✅ 업로드 완료");
    } catch (err) {
      console.error(err);
      setMessage("❌ 업로드 실패");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div style={{ padding: "2rem", maxWidth: "700px", margin: "0 auto" }}>
      <h2 style={{ marginBottom: "1rem" }}>📚 학생 문서 업로드</h2>

      <div style={{ marginBottom: "1rem" }}>
        <label>📄 재학증명서 업로드: </label>
        <input
          type="file"
          accept=".pdf,.jpg,.jpeg,.png"
          onChange={(e) => setEnrollmentFile(e.target.files?.[0] || null)}
        />
      </div>

      <div style={{ marginBottom: "1rem" }}>
        <label>📄 성적증명서 업로드: </label>
        <input
          type="file"
          accept=".pdf,.jpg,.jpeg,.png"
          onChange={(e) => setGradeFile(e.target.files?.[0] || null)}
        />
      </div>

      <button onClick={handleUpload} disabled={uploading}>
        {uploading ? "업로드 중..." : "문서 확인하기"}
      </button>

      {message && <p style={{ marginTop: "1rem" }}>{message}</p>}

      {rawText && (
        <div style={{ marginTop: "2rem" }}>
          <h3>📝 원문 텍스트</h3>
          <pre
            style={{
              whiteSpace: "pre-wrap",
              background: "#f6f6f6",
              padding: "1rem",
              borderRadius: "8px",
              fontSize: "0.9rem",
              lineHeight: "1.4",
            }}
          >
            {rawText}
          </pre>
        </div>
      )}

      {extracted && (
        <div style={{ marginTop: "2rem" }}>
          <h3>📋 추출 결과</h3>
          <ul>
            {Object.entries(extracted).map(([key, value]) => (
              <li key={key}>
                <strong>{key}</strong>: {String(value)}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default UploadStudent;
