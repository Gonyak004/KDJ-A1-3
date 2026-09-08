import os
import json
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 정적 파일 마운트 (CSS, JS)
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
    # Vercel 환경변수인 'GeminiAPIKey' 및 'GEMINI_API_KEY'를 모두 탐색
    api_key = (
        os.environ.get("GeminiAPIKey")
        or os.environ.get("GEMINI_API_KEY")
        or os.getenv("GeminiAPIKey")
        or os.getenv("GEMINI_API_KEY")
    )

    if not api_key:
        loaded_keys = list(os.environ.keys())
        return JSONResponse(
            status_code=500,
            content={
                "error": f"GEMINI_API_KEY를 불러오지 못했습니다. 감지된 환경변수 목록: {loaded_keys}"
            }
        )

    try:
        # Gemini API 설정 및 호출
        genai.configure(api_key=api_key.strip())
        model = genai.GenerativeModel("gemini-3.5-flash")

        prompt = (
            f"당신은 전문 헬스 트레이너이자 영양사입니다.\n"
            f"- 운동 목표: {request.goal}\n"
            f"- 운동 수준: {request.level}\n"
            f"- 주당 운동 횟수: {request.days}일\n\n"
            f"위 조건에 맞춘 주간 운동 스케줄과 식단 추천 가이드를 보기 쉽게 한국어로 명확하고 친절하게 작성해 주세요."
        )

        response = model.generate_content(prompt)

        return {"recommendation": response.text}

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Gemini API 호출 중 에러 발생: {str(e)}"}
        )