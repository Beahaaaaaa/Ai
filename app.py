import os
from flask import Flask, request, jsonify
import requests

app = Flask(**name**)

API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL = "gemini-2.5-flash"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

@app.route("/kakao-bot", methods=["POST"])
def kakao_bot():
try:
body = request.get_json(silent=True) or {}
user_message = body.get("userRequest", {}).get("utterance", "")

```
    if not API_KEY:
        ai_answer = "서버 설정 오류: GEMINI_API_KEY가 등록되지 않았습니다."

    elif not user_message.strip():
        ai_answer = "메시지가 비어있습니다."

    else:
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": user_message.strip()
                        }
                    ]
                }
            ]
        }

        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": API_KEY
        }

        response = requests.post(
            API_URL,
            json=payload,
            headers=headers,
            timeout=20
        )

        if response.status_code == 200:
            result = response.json()

            try:
                ai_answer = result["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError, TypeError):
                ai_answer = "AI 응답을 처리하는 중 구조 오류가 발생했습니다."

        else:
            try:
                error_data = response.json()
                error_message = error_data.get("error", {}).get("message", response.text)
            except Exception:
                error_message = response.text

            ai_answer = f"API 호출 실패 (상태 코드: {response.status_code}, 내용: {error_message})"

except requests.exceptions.Timeout:
    ai_answer = "AI 서버 응답 시간이 초과되었습니다."

except requests.exceptions.RequestException:
    ai_answer = "AI 서버에 연결할 수 없습니다."

except Exception:
    ai_answer = "서버 내부 오류가 발생했습니다."

kakao_response = {
    "version": "2.0",
    "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": ai_answer
                }
            }
        ]
    }
}

return jsonify(kakao_response)
```

if **name** == "**main**":
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
