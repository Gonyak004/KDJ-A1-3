import os
from fastapi import FastAPI
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

# 루트 및 메인 페이지 반환
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
def recommend_routine(request: RecommendRequest):
    # 환경변수에서 키 가져오기
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        return JSONResponse(
            status_code=500, 
            content={"error": "GEMINI_API_KEY가 설정되지 않았습니다. Vercel 환경변수를 확인해주세요."}
        )

    try:
        # API 키 직접 할당으로 구동 인스턴스 생성
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"목표: {request.goal}, 운동수준: {request.level}, 주당 운동일수: {request.days}일에 맞는 맞춤형 운동 루틴을 추천해줘."
        response = model.generate_content(prompt)
        
        return {"recommendation": response.text}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Gemini API 통신 에러: {str(e)}"})