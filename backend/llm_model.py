# 📄 backend/recommend_router.py

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import List, Dict
from langchain_upstage import ChatUpstage
from langchain.schema import Document
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import os, requests, json, pandas as pd
from difflib import SequenceMatcher
from datetime import datetime, timezone

router = APIRouter()
llm = ChatUpstage(api_key=os.getenv("UPSTAGE_API_KEY"), model="solar-pro")

TRUSTED_DOMAINS = [
    "go.kr", "or.kr", "korea.kr", "work.go.kr", "bokjiro.go.kr",
    "welfare.seoul.kr", "seoul.go.kr", "kosaf.go.kr", "kofac.re.kr", "kicoa.or.kr"
]

class RecommendInput(BaseModel):
    user_input: str

def search_naver_url(program_title):
    url = "https://openapi.naver.com/v1/search/webkr.json"
    headers = {
        "X-Naver-Client-Id": os.getenv("NAVER_CLIENT_ID"),
        "X-Naver-Client-Secret": os.getenv("NAVER_CLIENT_SECRET")
    }
    best_link, best_score = "", -1
    now = datetime.now(timezone.utc)

    for domain in TRUSTED_DOMAINS:
        try:
            params = {
                "query": f"{program_title} site:{domain}",
                "display": 5,
                "sort": "date"
            }
            res = requests.get(url, headers=headers, params=params, timeout=5)
            data = res.json()
            for item in data.get("items", []):
                link = item.get("link", "").strip("<>")
                if not link.startswith("http"):
                    continue
                title_similarity = SequenceMatcher(None, program_title, item.get("title", "")).ratio()
                try:
                    pub_date = datetime.strptime(item.get("pubDate", ""), "%a, %d %b %Y %H:%M:%S %z")
                    recency_score = max(0, 1 - (now - pub_date).days / 30)
                except:
                    recency_score = 0
                score = 0.2 * title_similarity + 0.8 * recency_score
                if score > best_score:
                    best_score, best_link = score, link
        except Exception as e:
            print(f"Naver search failed for {program_title}: {e}")

    return best_link or f"https://www.google.com/search?q={program_title}+장학금"

def generate_program_titles(user_input: str):
    prompt = f"""
    사용자 조건: "{user_input}"

    조건에 맞는 장학금 또는 지원금 프로그램을 10개 이상 추천해주세요.
    링크 없이 제목(title)과 설명(description)만 포함하고 JSON 형식으로 반환하세요.

    {{
      "programs": [
        {{"title": "...", "description": "..."}}, ...
      ]
    }}
    """
    result = llm.invoke(prompt)
    try:
        return json.loads(result.content).get("programs", [])
    except Exception:
        return []

def enrich_with_links(programs):
    return [
        {
            "title": p["title"],
            "description": p.get("description", ""),
            "link": search_naver_url(p["title"])
        }
        for p in programs
    ]

def recommend_by_rag(user_input: str):
    csv_path = "scholarships.csv"  # ⬅️ 실제 경로에 맞게 조정
    df = pd.read_csv(csv_path).dropna(subset=["name", "raw_text"])
    docs = [
        Document(page_content=f"{row['name']} - {row['raw_text']}", metadata={"id": row["id"]})
        for _, row in df.iterrows()
    ]
    embedding = HuggingFaceEmbeddings(model_name="jhgan/ko-sbert-nli")
    vectorstore = FAISS.from_documents(docs, embedding)
    retriever = vectorstore.as_retriever()
    context = "\n\n".join([doc.page_content for doc in retriever.get_relevant_documents(user_input)])
    prompt = f"""
    다음은 장학금 정보 데이터베이스입니다:\n{context}\n
    사용자 조건: "{user_input}"

    가장 적합한 프로그램 3개를 아래와 같이 추천해주세요.
    {{
      "programs": [
        {{"title": "...", "description": "...", "link": "..."}}
      ]
    }}
    """
    result = llm.invoke(prompt)
    try:
        return json.loads(result.content).get("programs", [])
    except:
        return []



