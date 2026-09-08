import os
import json
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 정적 파일 마운트 (css, js)
if os.path.exists(os.path.join(BASE_DIR, "css")):
    app.mount("/css", StaticFiles(directory=os.path.join(BASE_DIR, "css")), name="css")

if os.path.exists(os.path.join(BASE_DIR, "js")):
    app.mount("/js", StaticFiles(directory=os.path.join(BASE_DIR, "js")), name="js")

# 메인 웹페이지 출력 (루트 접속 시 index.html 반환)
@app.get("/")
def home():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.get("/index.html")
def index_page():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

# FitFinal AI 추천 API
class RecommendRequest(BaseModel):
    goal: str
    level: str
    days: str

@app.post("/api/recommend")
def recommend_routine(request: RecommendRequest):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return JSONResponse(status_code=500, content={"error": "GEMINI_API_KEY가 설정되지 않았습니다."})

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"목표: {request.goal}, 운동수준: {request.level}, 주당 운동일수: {request.days}일에 맞는 맞춤형 운동 루틴을 추천해줘."
        response = model.generate_content(prompt)
        
        return {"recommendation": response.text}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})