import os
import json
import urllib.parse
import urllib.request
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 정적 파일 경로 연결 (CSS, JS)
if os.path.exists(os.path.join(BASE_DIR, "css")):
    app.mount("/css", StaticFiles(directory=os.path.join(BASE_DIR, "css")), name="css")

if os.path.exists(os.path.join(BASE_DIR, "js")):
    app.mount("/js", StaticFiles(directory=os.path.join(BASE_DIR, "js")), name="js")

# 루트 페이지
@app.get("/")
def home():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.get("/index.html")
def index_page():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))


# Pydantic 데이터 모델
class RecommendRequest(BaseModel):
    goal: str
    level: str
    days: str

class DietRequest(BaseModel):
    height: str
    weight: str
    gender: str
    target_weight: str


# Gemini 모델 초기화
def get_gemini_model():
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
        model = genai.GenerativeModel("gemini-3.5-flash")
        return model, None
    except Exception as e:
        return None, f"Gemini API 초기화 에러: {str(e)}"


# 1. AI 맞춤 루틴 생성 API
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


# 2. AI 맞춤 식단 생성 API
@app.post("/api/diet")
async def recommend_diet(request: DietRequest):
    model, error = get_gemini_model()
    if error:
        return JSONResponse(status_code=500, content={"error": error})

    try:
        prompt = (
            f"당신은 전문 임상영양사이자 다이어트 컨설턴트입니다.\n"
            f"- 키: {request.height}cm\n"
            f"- 현재 체중: {request.weight}kg\n"
            f"- 성별: {request.gender}\n"
            f"- 목표 체중: {request.target_weight}kg\n\n"
            f"위 조건을 바탕으로 기초대사량 추정치, 일일 권장 칼로리, 영양소 비율, 추천 식단 예시를 한국어로 작성해 주세요."
        )
        response = model.generate_content(prompt)
        return {"recommendation": response.text}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"API 호출 오류: {str(e)}"})


# 3. YouTube Data API v3 연동 검색 대리 API
@app.get("/api/youtube")
async def search_youtube(query: str = ""):
    youtube_api_key = os.environ.get("YOUTUBE_API_KEY") or os.getenv("YOUTUBE_API_KEY")

    if not youtube_api_key:
        return JSONResponse(
            status_code=500,
            content={"error": "YOUTUBE_API_KEY가 설정되지 않았습니다. Vercel Settings -> Environment Variables에서 키를 추가해주세요."}
        )

    if not query.strip():
        return JSONResponse(status_code=400, content={"error": "검색어를 입력해주세요."})

    try:
        # 정확한 운동 자세 가이드 수집을 위한 검색어 보정
        search_query = f"{query.strip()} 자세 운동 가이드"
        encoded_query = urllib.parse.quote(search_query)

        # YouTube Data API v3 호출 URL
        url = (
            f"https://www.googleapis.com/youtube/v3/search"
            f"?part=snippet"
            f"&q={encoded_query}"
            f"&type=video"
            f"&maxResults=6"
            f"&key={youtube_api_key.strip()}"
        )

        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode('utf-8')
            data = json.loads(res_body)

        videos = []
        for item in data.get("items", []):
            video_id = item.get("id", {}).get("videoId")
            snippet = item.get("snippet", {})
            if video_id:
                thumbnails = snippet.get("thumbnails", {})
                thumb_url = (
                    thumbnails.get("high", {}).get("url")
                    or thumbnails.get("medium", {}).get("url")
                    or thumbnails.get("default", {}).get("url")
                )
                videos.append({
                    "id": video_id,
                    "title": snippet.get("title", ""),
                    "channelTitle": snippet.get("channelTitle", ""),
                    "thumbnail": thumb_url,
                    "url": f"https://www.youtube.com/watch?v={video_id}"
                })

        return {"videos": videos}

    except urllib.error.HTTPError as e:
        error_msg = e.read().decode('utf-8')
        return JSONResponse(status_code=e.code, content={"error": f"YouTube API 호출 중 오류 발생: {error_msg}"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"서버 오류: {str(e)}"})