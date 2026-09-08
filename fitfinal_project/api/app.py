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


# Request 모델들
class RecommendRequest(BaseModel):
    goal: str
    level: str
    days: str

class DietRequest(BaseModel):
    height: str
    weight: str
    gender: str
    target_weight: str


def get_gemini_model():
    # Vercel 환경변수인 'GeminiAPIKey' 및 'GEMINI_API_KEY' 탐색
    api_key = (
        os.environ.get("GeminiAPIKey")
        or os.environ.get("GEMINI_API_KEY")
        or os.getenv("GeminiAPIKey")
        or os.getenv("GEMINI_API_KEY")
    )

    if not api_key:
        return None, "GEMINI_API_KEY를 불러오지 못했습니다. Vercel 환경변수를 확인해주세요."

    try:
        genai.configure(api_key=api_key.strip())
        # 무료 등급 최적화 모델 사용
        model = genai.GenerativeModel("gemini-2.5-flash")
        return model, None
    except Exception as e:
        return None, f"Gemini API 초기화 에러: {str(e)}"


@app.post("/api/recommend")
async def recommend_routine(request: RecommendRequest):
    model, error = get_gemini_model()
    if error:
        return JSONResponse(status_code=500, content={"error": error})

    try:
        prompt = (
            f"당신은 전문 헬스 트레이너이자 영양사입니다.\n"
            f"- 운동 목표: {request.goal}\n"
            f"- 운동 수준: {request.level}\n"
            f"- 주당 운동 횟수: {request.days}일\n\n"
            f"위 조건에 맞춘 주간 운동 스케줄과 핵심 포인트를 보기 쉽게 한국어로 작성해 주세요."
        )
        response = model.generate_content(prompt)
        return {"recommendation": response.text}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"API 호출 오류: {str(e)}"})


@app.post("/api/diet")
async def recommend_diet(request: DietRequest):
    model, error = get_gemini_model()
    if error:
        return JSONResponse(status_code=500, content={"error": error})

    try:
        prompt = (
            f"당신은 전문 임상영양사이자 다이어트 컨설턴트입니다.\n"
            f"다음 사용자의 신체 스펙과 목표를 바탕으로 맞춤형 식단 관리 가이드를 제공해주세요.\n"
            f"- 키: {request.height}cm\n"
            f"- 현재 체중: {request.weight}kg\n"
            f"- 성별: {request.gender}\n"
            f"- 목표 체중: {request.target_weight}kg\n\n"
            f"다음 내용을 포함하여 보기 쉽고 체계적으로 가이드를 작성해주세요:\n"
            f"1. 기초대사량(BMR) 추정치 및 일일 권장 섭취 칼로리\n"
            f"2. 영양소 비율 가이드 (탄수화물, 단백질, 지방 비율 및 추천 식품)\n"
            f"3. 아침/점심/저녁/간식 추천 식단 예시\n"
            f"4. 지속 가능한 식단을 위한 핵심 수칙 3가지"
        )
        response = model.generate_content(prompt)
        return {"recommendation": response.text}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"API 호출 오류: {str(e)}"})