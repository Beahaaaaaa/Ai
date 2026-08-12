import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 버그 수정: 환경 변수 이름 끝의 불필요한 닫는 괄호 제거
API_KEY = os.environ.get("AIzaSyDui0j44HLQBhUiY7O1resMlNKpp3wdetY")
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

@app.route("/kakao-bot", methods=["POST"])
def kakao_bot():
    try:
        body = request.get_json()
        user_message = body.get("userRequest", {}).get("utterance", "")

        if user_message.startswith("@관리봇 AI"):
            prompt = user_message.replace("@관리봇 AI", "").strip()
            
            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }]
            }
            
            headers = {"Content-Type": "application/json"}
            
            # API 요청 (timeout 설정 추가로 무한 대기 방지)
            response = requests.post(
                f"{API_URL}?key={API_KEY}",
                json=payload,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                # 안전하게 응답 데이터 추출
                try:
                    ai_answer = result["candidates"][0]["content"]["parts"][0]["text"]
                except (KeyError, IndexError):
                    ai_answer = "AI 응답을 처리하는 중 오류가 발생했습니다."
            else:
                ai_answer = f"API 호출 실패 (상태 코드: {response.status_code})"
        else:
            ai_answer = "명령어를 확인해주세요."

    except Exception as e:
        ai_answer = "서버 내부 오류가 발생했습니다."
        # 디버깅을 위해 에러 로그를 남기고 싶다면 아래 주석을 해제하세요
        # print(f"Error: {e}")

    kakao_response = {
        "version": "2.0",
        "template": {
            "outputs": [{
                "simpleText": {"text": ai_answer}
            }]
        }
    }
    return jsonify(kakao_response)

if __name__ == "__main__":
    app.run(port=5000)