import os
import json
from openai import OpenAI
from dotenv import load_dotenv
import base64

load_dotenv()
API_KEY = os.getenv("UPSTAGE_API_KEY")

def encode_file_to_base64(file_path: str) -> str:
    with open(file_path, "rb") as f:
        file_bytes = f.read()
        return base64.b64encode(file_bytes).decode('utf-8')

def call_info_extract(file_path: str):
    extraction_client = OpenAI(
        api_key=API_KEY,
        base_url="https://api.upstage.ai/v1/information-extraction"
    )
    
    base64_data = encode_file_to_base64(file_path)
    
    try:
        extraction_schema = create_schema(file_path)
    except Exception as e:
        return {
            "error": str(e)
        }

    # print("[DEBUG] InfoExtract Payload:", json.dumps(payload, ensure_ascii=False, indent=2))  # 디버깅 로그
    try:
        response = extraction_client.chat.completions.create(
            model="information-extract",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:application/pdf;base64,{base64_data}"
                            }
                        }
                    ]
                }
            ],
            response_format=extraction_schema
        )
    except Exception as e:
        return {
            "error": str(e)
        }
    
    try:
        result = response.choices[0].message.content
    except (IndexError, AttributeError) as e:
        return {
            "error": str(e)
        }
    
    try:
        result_json = json.loads(result)
    except json.JSONDecodeError as e:
        return {
            "error": str(e),
            "raw_content": result
        }
    
    return result_json

def create_schema(file_path: str):
    if(file_path == "enrollment_temp.pdf"):
        extraction_schema = {
            "type": "json_schema",
            "json_schema": {
                "name": "student_info_extraction",
                "schema": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "학생의 이름"
                        },
                        "studentid": {
                            "type": "string",
                            "description": "학생의 학번"
                        },
                        "major": {
                            "type": "string",
                            "description": "학생의 전공"
                        },
                        "year": {
                            "type": "string",
                            "description": "학생의 입학년도"
                        }
                    },
                    "required": ["name", "studentid", "major", "year"]
                }
            }
        }
    if (file_path == "grade_temp.pdf"):
        extraction_schema = {
            "type": "json_schema",
            "json_schema": {
                "name": "student_info_extraction",
                "schema": {
                    "type": "object",
                    "properties": {
                        "grade": {
                            "type": "string",
                            "description": "학생의 학점"
                        }
                    },
                    "required": ["grade"]
                }
            }
        }
    if (file_path == "scholarship_temp.pdf"):
        extraction_schema = {
            "type": "json_schema",
            "json_schema": {
                "name": "student_info_extraction",
                "schema": {
                    "type": "object",
                    "properties": {
                        "program_name": {
                            "type": "string",
                            "description": "장학금의 이름을 뽑아주세요...."
                        }
                    },
                    "required": ["program_name"]
                }
            }
        }
    return extraction_schema