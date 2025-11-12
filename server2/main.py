from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from pathlib import Path

app = FastAPI(title="Server2")

DATA_FILE = Path(__file__).parent / "data.json" # 파일명

class DataResponse(BaseModel):
    name: str
    data: str

# 시작 시 JSON파일을 로딩
@app.on_event("startup")
def load_data():
    global DATA
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        DATA = json.load(f)

# 서버 1으로 부터 값 요청을 받으면 실행
@app.get("/data", response_model=DataResponse)
def get_data(name: str):
    if name not in DATA:
        raise HTTPException(status_code=404, detail=f"'{name}'에 해당하는 데이터가 없습니다.")
    return DataResponse(name=name, data=DATA[name])