# main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from upstage import call_upstage_api 

from domain.user.user_router import router as user_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    file_path = "temp.pdf"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    result = call_upstage_api(file_path)
    return {"text": result}

app.include_router(user_router, prefix="/api")