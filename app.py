import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = os.environ.get("GEMINI_API_KEY")
# 모델 이름을 최신 환경에 맞게 수정했습니다.
API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"

@app.route("/kakao-bot", methods=["POST"])
def kakao_bot():
    try:
        body = request.get_json()
        user_message = body.get("userRequest", {}).get("utterance", "")

        if not API_KEY:
            ai_answer = "서버 설정 오류: GEMINI_API_KEY가 등록되지 않았습니다."
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
