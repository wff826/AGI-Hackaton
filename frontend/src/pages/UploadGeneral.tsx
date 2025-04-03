import React, { useState } from "react";
import "../components/Upload.css";

export default function UploadGeneral() {
  const [resident, setResident] = useState<File | null>(null);
  const [income, setIncome] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [result, setResult] = useState<string>("");
  const [extracted, setExtracted] = useState<Record<string, any> | null>(null);

  const handleUpload = async () => {
    if (!resident || !income) return;
    setIsUploading(true);

    const formData = new FormData();
    formData.append("resident", resident);
    formData.append("income", income);

    try {
      const res = await fetch("http://localhost:8000/upload/general", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setResult(data.raw_text || "");
      setExtracted(data.extracted_info || null);
    } catch (err) {
      console.error("업로드 실패", err);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="upload-container">
      <h2 className="upload-title">🏠 일반인 문서 업로드</h2>
      <div className="upload-row">
        <label>📄 주민등록등본 업로드:</label>
        <input type="file" accept="application/pdf" onChange={(e) => setResident(e.target.files?.[0] || null)} />
        {resident && <span>{resident.name}</span>}
      </div>
      <div className="upload-row">
        <label>📄 소득증명서 업로드:</label>
        <input type="file" accept="application/pdf" onChange={(e) => setIncome(e.target.files?.[0] || null)} />
        {income && <span>{income.name}</span>}
      </div>

      <button className="upload-button" onClick={handleUpload} disabled={!resident || !income || isUploading}>
        {isUploading ? "업로드 중..." : "업로드"}
      </button>

      {isUploading && <p>업로드 중...</p>}

      {extracted && (
        <div className="result-card">
          <h3>📋 추출된 정보</h3>
          <ul>
            {Object.entries(extracted).map(([key, value]) => (
              <li key={key}><strong>{key}</strong>: {String(value)}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
