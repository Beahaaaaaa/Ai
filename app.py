import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = os.environ.get("AIzaSyDui0j44HLQBhUiY7O1resMlNKpp3wdetY")
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

@app.route("/kakao-bot", methods=["POST"])
def kakao_bot():
    try:
        body = request.get_json()
        user_message = body.get("userRequest", {}).get("utterance", "")

        if not API_KEY:
            ai_answer = "서버 설정 오류: GEMINI_API_KEY 환경 변수가 설정되지 않았습니다. Render 대시보드의 Environment Variables에서 키를 등록해 주세요."
        elif user_message:
            prompt = user_message.strip()
            
            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }]
            }
            
            headers = {"Content-Type": "application/json"}
            
            response = requests.post(
                f"{API_URL}?key={API_KEY}",
                json=payload,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                try:
                    ai_answer = result["candidates"][0]["content"]["parts"][0]["text"]
                except (KeyError, IndexError):
                    ai_answer = "AI 응답을 처리하는 중 구조 오류가 발생했습니다."
            else:
                ai_answer = f"API 호출 실패 (상태 코드: {response.status_code}, 내용: {response.text})"
        else:
            ai_answer = "메시지가 비어있습니다."

    except Exception as e:
        ai_answer = "서버 내부 오류가 발생했습니다."

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
