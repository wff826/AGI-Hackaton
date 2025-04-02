import React, { useState } from "react";

export default function Upload() {
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);
    setLoading(true);

    const res = await fetch("http://localhost:8000/upload/", {
      method: "POST",
      body: formData,
    });
    const data = await res.json();
    setResult(data.text);
    setLoading(false);
  };

  return (
    <div>
      <h2>PDF 문서 업로드</h2>
      <input type="file" accept="application/pdf" onChange={handleUpload} />
      {loading && <p>문서를 분석 중입니다...</p>}
      {result && <pre>{result}</pre>}
    </div>
  );
}
