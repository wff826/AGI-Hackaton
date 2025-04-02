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
    <div className="bg-white p-6 rounded-lg shadow w-full max-w-md">
      <label className="block mb-2 font-semibold">지원금 신청 문서 업로드</label>
      <input
        type="file"
        accept="application/pdf"
        onChange={handleUpload}
        className="mb-4 w-full"
      />
      {loading ? (
        <p className="text-blue-500">문서를 분석 중입니다...</p>
      ) : (
        result && (
          <div className="bg-gray-100 p-4 rounded mt-4">
            <h2 className="font-bold mb-2">추출된 정보</h2>
            <pre className="whitespace-pre-wrap text-sm">{result}</pre>
          </div>
        )
      )}
    </div>
  );
}
