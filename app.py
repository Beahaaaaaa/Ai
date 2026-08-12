import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
API_KEY = os.environ.get("GEMINI_API_KEY")
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

@app.route("/kakao-bot", methods=["POST"])
def kakao_bot():
    try:
        body = request.get_json()
        msg = body.get("userRequest", {}).get("utterance", "").strip()
        if not API_KEY: ans = "API Key 오류"
        elif msg:
            Complete_URL = f"{API_URL}?key={API_KEY}"
            payload = {
                "system_instruction": {"parts": [{"text": "16줄을 절대 넘기지 말고 짧고 간결하게 대답해라."}]},
                "contents": [{"parts": [{"text": msg}]}]
            }
            res = requests.post(Complete_URL, json=payload, headers={"Content-Type": "application/json"}, timeout=10)
            ans = res.json()["candidates"][0]["content"]["parts"][0]["text"] if res.status_code == 200 else f"오류: {res.status_code}"
        else: ans = "메시지 없음"
    except: ans = "서버 오류"
    return jsonify({"version": "2.0", "template": {"outputs": [{"simpleText": {"text": ans}}]}})

if __name__ == "__main__":
    app.run(port=5000)
