import pandas as pd
from database import SessionLocal, sync_engine
from models import Scholarship
from sqlalchemy import select

db = SessionLocal()
    
scholarships = db.query(Scholarship).all()
scholarship_data = []
for scholarship in scholarships:
    scholarship_data.append({
        "id": scholarship.id,
        "name": scholarship.name,
        "raw_text": scholarship.raw_text,
    })
db.close()

df_scholarships = pd.DataFrame(scholarship_data)
df_scholarships.to_csv("scholarships.csv", index=False, encoding="utf-8-sig")

print("CSV 파일 저장")
