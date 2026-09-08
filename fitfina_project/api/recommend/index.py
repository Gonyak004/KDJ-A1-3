from http.server import BaseHTTPRequestHandler
import json
import os
import google.generativeai as genai

api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

class handler(BaseHTTPRequestHandler):
    # GET 요청 처리 (브라우저 직접 접근 시)
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        res = {"message": "FitFinal AI API Server가 정상 작동 중입니다. POST 요청을 사용해 주세요."}
        self.wfile.write(json.dumps(res, ensure_ascii=False).encode('utf-8'))

    # POST 요청 처리 (AI 추천 버튼 클릭 시)
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))

            goal = data.get('goal', '체중 감량')
            level = data.get('level', '초보자')
            days = data.get('days', '3')

            if not api_key:
                self.send_response(500)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "GEMINI_API_KEY가 설정되지 않았습니다."}).encode('utf-8'))
                return

            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"운동 목표: {goal}, 운동 수준: {level}, 주당 운동 횟수: {days}회. 맞춤형 운동 루틴과 식단 가이드를 추천해줘."
            
            response = model.generate_content(prompt)

            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            res_data = {"recommendation": response.text}
            self.wfile.write(json.dumps(res_data, ensure_ascii=False).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()