from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import httpx
import os
from pathlib import Path

app = FastAPI(title="Server1")

# 서버 2 주소
SERVER2_URL = os.getenv("SERVER2_URL", "http://127.0.0.1:8002")

static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir, html=False), name="static")

# html 호출
@app.get("/")
def root():
    return FileResponse(static_dir / "index.html")

class DataResponse(BaseModel):
    name: str
    data: str

@app.get("/api/query", response_model=DataResponse)
async def query(name: str = Query(..., description="조회할 키 이름")):
    url = f"{SERVER2_URL}/data"
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            # 서버 2에게 name의 값을 요청
            r = await client.get(url, params={"name": name})
        if r.status_code == 404:
            detail = r.json().get("detail", "데이터가 없습니다.")
            raise HTTPException(status_code=404, detail=detail)
        r.raise_for_status()
        payload = r.json()
        return DataResponse(**payload)
    # 서버에 연결을 실패했을 때
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"서버2 연결 실패: {e}") from e
    # 서버에 기타 오류가 생겼을 때
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"서버2 에러: {e.response.text}") from e