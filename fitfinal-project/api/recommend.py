import json
import os
from http.server import BaseHTTPRequestHandler
from google import genai

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        
        try:
            data = json.loads(body.decode('utf-8'))
            goal = data.get('goal', '건강 관리')
            level = data.get('level', '초급자')
            days = data.get('days', '3')

            # Vercel 환경 변수에 설정된 GEMINI_API_KEY 불러오기
            api_key = os.environ.get("GEMINI_API_KEY")
            
            if not api_key:
                self._send_response(500, {"error": "GEMINI_API_KEY가 설정되지 않았습니다."})
                return

            # Gemini Client 초기화
            client = genai.Client(api_key=api_key)

            prompt = f"운동 목표: {goal}, 운동 수준: {level}, 주당 운동 횟수: {days}회. 이 사용자를 위한 주간 운동 루틴과 식단 가이드를 300자 이내로 친절하게 작성해줘."

            # Gemini 2.5 Flash 모델 호출 (빠르고 무료 티어 제공)
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )

            result_text = response.text

            self._send_response(200, {"recommendation": result_text})

        except Exception as e:
            self._send_response(500, {"error": f"서버 오류 발생: {str(e)}"})

    def _send_response(self, status_code, body):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(body).encode('utf-8'))