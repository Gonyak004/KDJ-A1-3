import os
import json
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 정적 파일 마운트
if os.path.exists(os.path.join(BASE_DIR, "css")):
    app.mount("/css", StaticFiles(directory=os.path.join(BASE_DIR, "css")), name="css")

if os.path.exists(os.path.join(BASE_DIR, "js")):
    app.mount("/js", StaticFiles(directory=os.path.join(BASE_DIR, "js")), name="js")

# 메인 웹페이지 출력
@app.get("/")
def home():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.get("/index.html")
def index_page():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))


class RecommendRequest(BaseModel):
    goal: str
    level: str
    days: str


@app.post("/api/recommend")
async def recommend_routine(request: RecommendRequest):
    # 1. 환경변수를 파이썬 os 모듈의 모든 구성을 뒤져서 확실하게 가져옵니다.
    api_key = os.environ.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

    # 2. 만약 그래도 안 불러와지면 디버깅용 메시지를 자세히 응답에 남깁니다.
    if not api_key:
        # Vercel 환경에서 들어있는 전체 환경변수 키 목록 출력 (보안을 위해 값은 출력 안함)
        loaded_keys = list(os.environ.keys())
        return JSONResponse(
            status_code=500,
            content={
                "error": f"GEMINI_API_KEY를 불러오지 못했습니다. 감지된 환경변수 목록: {loaded_keys}"
            }
        )

    try:
        # Gemini API 초기화
        genai.configure(api_key=api_key.strip()) # 혹시 들어갔을지 모를 공백 제거
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = (
            f"목표: {request.goal}, 운동수준: {request.level}, "
            f"주당 운동일수: {request.days}일에 맞는 맞춤형 운동 루틴을 상세히 추천해줘."
        )

        response = model.generate_content(prompt)

        return {"recommendation": response.text}

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Gemini API 호출 중 에러 발생: {str(e)}"}
        )