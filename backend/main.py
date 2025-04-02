# main.py

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import requests

# .env 파일 로드
load_dotenv()
API_KEY = os.getenv("UPSTAGE_API_KEY")
print(f"[DEBUG] API_KEY: {API_KEY}")

# FastAPI 인스턴스 생성 (괄호 반드시!)
app = FastAPI()

# CORS 설정 (프론트엔드 연동 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# PDF 파일을 Upstage Document Parse API로 보내기
def call_upstage_api(file_path: str):
    url = "https://python.langchain.com/docs/integrations/providers/upstage/#document-parse"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    files = {"document": open(file_path, "rb")}
    data = {
        "ocr": "force",
        "coordinates": True,
        "chart_recognition": True,
        "output_formats": "text",
        "base64_encoding": "['table']",
        "model": "document-parse"
    }

    response = requests.post(url, headers=headers, files=files, data=data)
    
    # 응답 체크
    if response.status_code != 200:
        return f"[Error] Status {response.status_code}: {response.text}"

    return response.json()["content"]["text"]

# 업로드된 PDF를 받아 처리
@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    with open("temp.pdf", "wb") as f:
        f.write(await file.read())
    
    result = call_upstage_api("temp.pdf")
    return {"text": result}
