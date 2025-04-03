# backend/recommend.py

import os
import json
import requests
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from langchain_upstage import ChatUpstage
from langchain.schema import Document
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA

load_dotenv()
UPSTAGE_API_KEY = os.getenv("UPSTAGE_API_KEY")

os.environ["UPSTAGE_API_BASE"] = "https://api.upstage.ai/v1/solar"
llm = ChatUpstage(api_key=UPSTAGE_API_KEY, model="solar-pro")

router = APIRouter()


def is_url_accessible(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/117.0.0.0 Safari/537.36"
        )
    }
    try:
        res = requests.get(url, headers=headers, timeout=5)
        return res.status_code == 200
    except Exception:
        return False


def generate_initial_recommendations(user_info: str):
    prompt = (
        "다음 사용자에게 적절한 정부 지원금 및 장학금 프로그램을 JSON 형식으로 추천해줘.\n"
        "모든 항목은 실제 접속 가능한 정부 기관/공공기관 링크를 포함하고,\n"
        "응답은 반드시 다음과 같은 형식의 JSON만 출력해줘. 설명 없이 JSON만.\n"
        "{ \"programs\": [ {\"title\": \"...\", \"description\": \"...\", \"link\": \"...\"}, ... ] }\n\n"
        f"사용자 정보: {user_info}"
    )
    result = llm(prompt)
    content = result.content if hasattr(result, "content") else result
    try:
        return json.loads(content).get("programs", [])
    except Exception as e:
        print("❌ JSON 파싱 실패:", e)
        return []


def build_rag_chain(documents):
    embedding = HuggingFaceEmbeddings(model_name="jhgan/ko-sroberta-multitask")
    vectorstore = FAISS.from_documents(documents, embedding)
    qa_llm = ChatUpstage(model_name="solar-pro", temperature=0.7)
    return RetrievalQA.from_chain_type(llm=qa_llm, retriever=vectorstore.as_retriever())


def refine_programs_with_rag(programs, user_info, max_rounds=10):
    for i in range(max_rounds):
        invalid = [p for p in programs if not is_url_accessible(p["link"])]
        if not invalid:
            return programs

        documents = [
            Document(
                page_content=f"{p['title']}\n{p['description']}\n링크: {p['link']}",
                metadata={"source": p['link']}
            ) for p in programs
        ]
        qa = build_rag_chain(documents)

        query = (
            f"사용자 정보: {user_info}\n\n"
            f"다음 항목들 중 유효하지 않은 링크를 가진 프로그램들을 대체할 수 있는 "
            f"실제 접근 가능한 프로그램을 추천해줘.\n"
            f"다시 JSON 형식으로 programs 배열만 반환해줘.\n"
            f"대체할 항목들: {json.dumps(invalid, ensure_ascii=False)}"
        )

        result = qa.run(query)
        try:
            new_programs = json.loads(result).get("programs", [])
        except Exception:
            break

        titles_to_replace = {p["title"] for p in invalid}
        programs = [p for p in programs if p["title"] not in titles_to_replace] + new_programs

    return programs


# ✅ FastAPI 엔드포인트
@router.post("/recommend")
def recommend(user_info: str):
    try:
        initial = generate_initial_recommendations(user_info)
        final = refine_programs_with_rag(initial, user_info)
        return {"programs": final}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
