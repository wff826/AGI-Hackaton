@app.post("/upload/resident")
async def upload_resident(file: UploadFile = File(...)):
    file_path = "temp.pdf"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # 1. 문서에서 텍스트 추출
    raw_text = call_upstage_api(file_path)

    # 2. InfoExtract로 구조화 정보 추출
    instruction = "이름, 생년, 주소를 JSON 형식으로 추출해주세요."
    extracted_info = call_info_extract(raw_text, instruction)

    return {
        "raw_text": raw_text,
        "extracted_info": extracted_info
    }
