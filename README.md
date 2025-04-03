# 🎓 AI Support Fund Analysis Service

Upload documents such as resident registration, income certificates, enrollment certificates, and transcripts, and let the AI analyze your eligibility for support funds and recommend relevant programs.

## 🏗 Project Overview

- **Project Name**: AGI-Hackaton
- **Objective**: Upload documents → Extract information using Upstage API → Recommend optimal government support or scholarship programs using an AI recommendation system.

## 🧩 Project Structure

```
AGI-Hackaton
├── backend
│   ├── main.py
│   ├── database.py
│   ├── domain
│   │   ├── student
│   │   └── scholarship
│   ├── llm_router.py
│   ├── llm_model.py
│   └── ...
├── frontend
│   └── ...
```

## ⚙ Key Features

### 📑 Document Upload and Analysis
- **Resident Registration, Income Certificates** → Extract general user information (name, age, income, etc.) (Planned)
- **Enrollment Certificates, Transcripts** → Extract academic and grade information.

### 🤖 Upstage API
- **Document Parsing**: Extract text from PDFs.
- **InfoExtract**: Structure key information (income, major, grades, etc.) from documents.
- Powered by `langchain_upstage` + `solar-pro` models for advanced Korean document processing.

### 🌐 AI-Based Program Recommendation
- Analyze user information and document data using trained AI models (`langchain_upstage`, `HuggingFaceEmbeddings`, etc.).
- Provide personalized recommendations for programs (scholarships, government support funds).

## 🔑 Tech Stack

- **Backend**: FastAPI, SQLAlchemy, SQLite (async engine)
- **AI Model**: LangChain, HuggingFace, Upstage
- **Frontend**: React (TypeScript)
- **Infra / DevOps**: uvicorn, pip, GitHub

## 🚀 How to Run

```bash
cd backend
python -m venv venv
.\venv\Scripts\activate  # Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## 📦 Usage Examples

1. **Student User**  
   - Upload enrollment and transcript documents via the `/upload/student` endpoint → Save to DB.  
   - Get AI recommendations via the `/recommend/recommend-programs` endpoint.

2. **Final Results with Additional Input**  
   - Use the `/recommend/final-result` endpoint to combine session data, recommended programs, and additional user input for a final response.

## 🧭 API Endpoints

- `POST /create-session`: Generate a session using a UUID.
- `POST /upload/scholarship`: Upload scholarship documents → Save to DB.
- `GET /recommend/recommend-programs`: Recommend scholarships/support programs based on user information.
- `POST /recommend/final-result`: Provide final recommendations based on additional user input.

## 📸 Example Screen
![Example Screen](./initial_page.png)

## 🤝 Contribution Guidelines
1. Fork the repository → Create a new branch → Implement features.  
2. Submit a Pull Request (PR) to propose changes.  
3. Review the code and merge after approval.