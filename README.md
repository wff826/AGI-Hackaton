# 🎓 AI 지원금 분석 서비스

주민등록등본, 소득증명서, 재학증명서, 성적증명서를 업로드하면  
AI가 지원금 수혜 가능성을 분석하고 관련 제도를 추천해주는 서비스입니다.

---

## 🧩 프로젝트 구조

AGI-Hackaton
├── backend
│   ├── main.py
│   ├── database.py
│   ├── upstage.py
│   └── ...
├── frontend
│   ├── src
│   │   ├── App.tsx
│   │   ├── pages
│   │   │   ├── Home.tsx
│   │   │   ├── UploadGeneral.tsx
│   │   │   └── UploadStudent.tsx
│   │   └── ...

## ⚙ 주요 기능

### 👤 일반 사용자
- ✅ **주민등록등본 + 소득증명서** PDF 업로드
- 🤖 AI가 문서 내용을 분석하여 연령, 지역, 소득 정보를 추출
- 🎯 적합한 정부지원금 추천 기반 정보 제공 *(예: 청년/소득 기준)*

### 🎓 학생 사용자
- ✅ **재학증명서 + 성적증명서** PDF 업로드
- 🤖 학적 정보 분석 → **장학금/학자금 지원 프로그램 추천**

---

## 🔌 API 연결

| 기능 | API | 설명 |
|------|-----|------|
| 📄 문서 파싱 | Upstage **Document Parsing API** | PDF에서 텍스트 추출 |
| 🔍 정보 추출 | Upstage **InfoExtract API** | 문서에서 의미 있는 정보 추출 (예: 이름, 지역, 소득 등) |

---

## 🚀 실행 방법

### 🖥 백엔드 실행

```bash
cd backend
python -m venv venv
.\venv\Scripts\activate  # (Mac: source venv/bin/activate)
pip install -r requirements.txt
uvicorn main:app --reload
