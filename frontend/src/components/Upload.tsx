import React, { useState } from 'react';

interface ExtractedData {
  [key: string]: any;
}

export default function App() {
  const [step, setStep] = useState<1 | 2>(1);
  const [residentExtracted, setResidentExtracted] = useState<ExtractedData | null>(null);
  const [incomeExtracted, setIncomeExtracted] = useState<ExtractedData | null>(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async (
    e: React.ChangeEvent<HTMLInputElement>,
    type: 'resident' | 'income'
  ) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);
    setLoading(true);

    try {
      const res = await fetch(`http://localhost:8000/upload/${type}`, {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      if (type === 'resident') {
        setResidentExtracted(data.extracted_info);
      } else {
        setIncomeExtracted(data.extracted_info);
      }
    } catch (err) {
      console.error('에러 발생', err);
    } finally {
      setLoading(false);
    }
  };

  if (step === 1) {
    return (
      <div style={{ padding: '2rem', maxWidth: '600px', margin: '0 auto' }}>
        <h2 style={{ marginBottom: '1rem' }}>📄 주민등록등본 업로드</h2>
        <input type="file" accept="application/pdf" onChange={(e) => handleUpload(e, 'resident')} />

        <h2 style={{ margin: '2rem 0 1rem' }}>📄 소득증명서 업로드</h2>
        <input type="file" accept="application/pdf" onChange={(e) => handleUpload(e, 'income')} />

        {loading && <p>문서를 분석 중입니다...</p>}

        {residentExtracted && incomeExtracted && (
          <button
            style={{ marginTop: '2rem', padding: '10px 20px', fontSize: '16px' }}
            onClick={() => setStep(2)}
          >
            정보 확인하기
          </button>
        )}
      </div>
    );
  }

  if (step === 2) {
    return (
      <div style={{ padding: '2rem', maxWidth: '600px', margin: '0 auto' }}>
        <h2>📋 추출된 정보 확인</h2>

        <div style={{ marginTop: '1.5rem' }}>
          <h3>✅ 등본 정보</h3>
          <ul>
            {residentExtracted &&
              Object.entries(residentExtracted).map(([key, value]) => (
                <li key={key}>
                  <strong>{key}</strong>: {String(value)}
                </li>
              ))}
          </ul>

          <h3 style={{ marginTop: '1.5rem' }}>✅ 소득 정보</h3>
          <ul>
            {incomeExtracted &&
              Object.entries(incomeExtracted).map(([key, value]) => (
                <li key={key}>
                  <strong>{key}</strong>: {String(value)}
                </li>
              ))}
          </ul>
        </div>

        <button
          style={{ marginTop: '2rem', padding: '10px 20px', fontSize: '16px' }}
          onClick={() => alert('추천 결과 페이지는 다음 단계에서 구현됩니다.')}
        >
          지원금 추천 받기
        </button>
      </div>
    );
  }

  return null;
}