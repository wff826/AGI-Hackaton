import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("UPSTAGE_API_KEY")
print(f"[DEBUG] API_KEY: {API_KEY}")

def call_upstage_api(file_path: str):
    url = "https://api.upstage.ai/v1/document-digitization"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    files = {"document": open(file_path, "rb")}
    data = {
        "ocr": "force",
        "coordinates": True,
        "chart_recognition": True,
        "output_formats": '["text"]',
        "base64_encoding": '["table"]',
        "model": "document-parse"
    }

    response = requests.post(url, headers=headers, files=files, data=data)

    if response.status_code != 200:
        return f"[ERROR] {response.status_code}: {response.text}"

    try:
        json_data = response.json()
        result_text = json_data.get("content", {}).get("text", "")
        return result_text or "[INFO] 텍스트 추출 결과가 없습니다."
    except Exception as e:
        return f"[ERROR] 응답 처리 중 예외 발생: {str(e)}"
