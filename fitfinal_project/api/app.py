from http.server import BaseHTTPRequestHandler
import json
import os
import google.generativeai as genai

# Gemini API 설정
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body) if body else {}

            goal = data.get('goal', '')
            level = data.get('level', '')
            days = data.get('days', '')

            # Gemini AI 로직 처리
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"목표: {goal}, 운동수준: {level}, 주당 운동일수: {days}일에 맞는 맞춤형 운동 루틴을 추천해줘."
            response = model.generate_content(prompt)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            res_payload = json.dumps({"recommendation": response.text})
            self.wfile.write(res_payload.encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            res_payload = json.dumps({"error": str(e)})
            self.wfile.write(res_payload.encode('utf-8'))

    def do_GET(self):
        # GET 요청 시 API 상태 리턴
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"message": "FitFinal API Server running"}).encode('utf-8'))