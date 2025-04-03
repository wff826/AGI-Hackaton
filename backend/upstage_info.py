import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("UPSTAGE_API_KEY")

def call_info_extract(text: str, instruction: str):
    url = "https://api.upstage.ai/v1/information-extraction"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "information-extract",
        "messages": [
            {
                "type": "text", 
                "role": "user",
                "content": f"{text}\n\n{instruction}"
            }
        ],
        "output_format": "json",
        "response_format": {
            "format": "json"
        }
    }

    print("[DEBUG] InfoExtract Payload:", json.dumps(payload, ensure_ascii=False, indent=2))  # 디버깅

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        return {
            "error": f"[INFO EXTRACT ERROR] {response.status_code}",
            "detail": response.text
        }

    result = response.json().get("result")
    if isinstance(result, str):
        try:
            return json.loads(result)
        except:
            return {"error": "파싱 실패", "raw": result}
    return result
