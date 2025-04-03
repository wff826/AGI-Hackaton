import os
import json
import requests
from langchain_upstage import ChatUpstage
from langchain.tools import tool
from datetime import datetime, timezone
from difflib import SequenceMatcher
import re
from datetime import datetime
from dateutil.parser import parse


# ✅ API 키 설정
UPSTAGE_API_KEY = os.getenv("UPSTAGE_API_KEY")
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")
os.environ["UPSTAGE_API_BASE"] = "https://api.upstage.ai/v1/solar"
llm = ChatUpstage(api_key=UPSTAGE_API_KEY, model="solar-pro")

#추가됨됨
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


template = """
너는 장학금 추천 전문가야.

다음은 지금까지의 대화 기록이야:
{chat_history}

사용자의 입력: {input}

사용자가 입력한 조건들을 고려해서, 적절한 장학금/지원금 프로그램을 추천하거나
추가적으로 필요한 정보를 정중하게 질문해.

항상 사용자와 대화하는 톤으로 대답해.
"""

temp = PromptTemplate(input_variables=["chat_history", "input"], template=template)




# ✅ 신뢰 도메인
TRUSTED_DOMAINS = ["go.kr", "or.kr", "korea.kr", "work.go.kr", "bokjiro.go.kr", "welfare.seoul.kr", "seoul.go.kr", "kosaf.go.kr", "kofac.re.kr", "kicoa.or.kr"]

# ✅ 유효한 링크 필터링
# ✅ NAVER API 기반 링크 검색
def compute_title_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()

from datetime import datetime, timezone

def search_naver_url(program_title):
    url = "https://openapi.naver.com/v1/search/webkr.json"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }

    best_link = ""
    best_score = -1

    now = datetime.now(timezone.utc)  # ✅ 경고 없는 UTC 기준 현재 시간

    for domain in TRUSTED_DOMAINS:
        params = {
            "query": f"{program_title} site:{domain}",
            "display": 5,
            "sort": "date"
        }

        try:
            res = requests.get(url, headers=headers, params=params, timeout=5)
            data = res.json()

            for item in data.get("items", []):
                link = item.get("link", "").strip("<>")
                naver_title = item.get("title", "").replace("<b>", "").replace("</b>", "")
                pub_date_str = item.get("pubDate", "")

                if not link.startswith("http"):
                    continue

                # ✅ 속도 향상: 링크 유효성 검증 생략 (원하면 fallback에서 검증 가능)
                try:
                    pub_date = datetime.strptime(pub_date_str, "%a, %d %b %Y %H:%M:%S %z")
                    recency_score = max(0, 1 - (now - pub_date).days / 30)
                except:
                    recency_score = 0

                title_similarity = compute_title_similarity(program_title, naver_title)

                total_score = 0.2 * title_similarity + 0.8 * recency_score

                if total_score > best_score:
                    best_score = total_score
                    best_link = link

        except Exception as e:
            print(f"❌ NAVER 검색 오류 (도메인: {domain}): {e}")

    return best_link or f"https://www.google.com/search?q={program_title}+장학금"



# ✅ 단계 1: LLM이 장학금 제목/설명 추천
def generate_program_titles(user_input: str):
    prompt = f"""
    아래는 사용자의 정보입니다: "{user_input}"

    사용자의 조건에 따라 적절한 장학금 또는 지원 프로그램을 최소 20개 추천해주세요.
    각 항목은 제목(title)과 설명(description)만 포함하고, 링크는 절대 포함하지 마세요.

    반드시 아래 형식의 JSON만 출력하세요:
    {{
      "programs": [
        {{"title": "...", "description": "..."}},
        ...
      ]
    }}
    """
    result = llm.invoke(prompt)
    try:
        raw_content = result.content

        data = json.loads(raw_content)
        return data.get("programs", [])
    except Exception as e:
        return e

# ✅ 단계 2: NAVER API를 통한 링크 매핑
def enrich_with_links(programs):
    enriched = []
    for p in programs:
        title = p["title"]
        link = search_naver_url(title)
        enriched.append({
            "title": title,
            "description": p.get("description", ""),
            "link": link or "⚠️ 유효한 링크를 찾지 못했습니다."
        })
    return enriched

# ✅ 단계 3: DB기반 RAG이용

from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings  # or Upstage, HuggingFace 등
from langchain.schema import Document
import pandas as pd

csv_path = "D:\\code\\2025-1\\AGI_Hackathon2\\AGI-Hackaton\\backend\\scholarships.csv"
df = pd.read_csv(csv_path)

df_clean = df.dropna(subset=["name", "raw_text"])

# Document 리스트 생성
docs = [
    Document(
        page_content=f"{row['name']} - {row['raw_text']}",
        metadata={
            "id": row["id"],
            "name": row["name"]
        }
    )
    for _, row in df_clean.iterrows()
]

embedding = HuggingFaceEmbeddings(model_name="jhgan/ko-sbert-nli")
vectorstore = FAISS.from_documents(docs, embedding)
retriever = vectorstore.as_retriever()

def recommend_by_rag(user_input: str):
    retrieved_docs = retriever.get_relevant_documents(user_input)

    context = "\n\n".join([doc.page_content for doc in retrieved_docs])

    prompt = f"""
    다음은 장학금 정보 데이터베이스에서 검색된 내용입니다:
    {context}

    사용자의 조건: "{user_input}"

    이 내용을 바탕으로 사용자에게 적합한 장학금 3가지를 추천해주세요.
    각 항목은 JSON 형식으로 제공하고, 제목(title), 설명(description), 링크(url)을 포함하세요.

    반드시 아래 형식의 JSON만 출력하세요:
    {{
      "programs": [
        {{"title": "...", "description": "...", "url": "..."}},
        ...
      ]
    }}
    """

    result = llm.invoke(prompt)
    return result.content  # JSON 문자열





# ✅ Streamlit UI


def initial_input(base_input: str):
    rag_result = recommend_by_rag(base_input)
    rag_result = json.loads(rag_result)
    output = rag_result["programs"]
    return output
    
    
# base_input = '사용자정보'
# st.session_state.chat_history.append(("ai", json.loads(recommend_by_rag(base_input))["programs"]))
# for role, msg in st.session_state.chat_history:
#     with st.chat_message("🧑" if role == "user" else "🤖"):
#         if role == "ai":
#             for p in msg:
#                 link = p.get('link', '')
#                 st.markdown(f"### 📌 {p['title']}")
#                 st.markdown(p['description'])
#                 if isinstance(link, str) and link.startswith("http"):
#                     st.markdown(f"🔗 [공식 링크]({link})")
#                 else:
#                     st.markdown("⚠️ 유효한 링크를 찾지 못했습니다.")
#         else:
#             st.markdown(msg)


# # ✅ 사용자 입력
# user_input = st.chat_input("예: 이공계열 대학생 3학년입니다. 어떤 장학금이 있나요?")

# if user_input:
#     st.session_state.chat_history.append(("user", user_input))

#     with st.spinner("Step 1️⃣: 조건에 맞는 프로그램을 찾는 중..."):
#         programs = generate_program_titles(user_input)

#     with st.spinner("Step 2️⃣: 공식 링크를 검색 중..."):
#         enriched_programs = enrich_with_links(programs)

#     with st.spinner("Step 3️⃣: 실제 유효한 링크와 일치하는 프로그램 필터링 중..."):
#         DBdata = recommend_by_rag(user_input)
    

#     DBdata = json.loads(DBdata)

#     merged_programs = DBdata["programs"] + enriched_programs

#     st.session_state.chat_history.append(("ai", merged_programs))

# # ✅ 대화 출력
# for role, msg in st.session_state.chat_history:
#     with st.chat_message("🧑" if role == "user" else "🤖"):
#         if role == "ai":
#             for p in msg:
#                 link = p.get('link', '')
#                 st.markdown(f"### 📌 {p['title']}")
#                 st.markdown(p['description'])
#                 if isinstance(link, str) and link.startswith("http"):
#                     st.markdown(f"🔗 [공식 링크]({link})")
#                 else:
#                     st.markdown("⚠️ 유효한 링크를 찾지 못했습니다.")
#         else:
#             st.markdown(msg)