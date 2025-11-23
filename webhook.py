import requests
from flask import Flask, request

app = Flask(__name__)

# ⭐ 這裡放 Make.com Webhook URL（你的那條）
MAKE_WEBHOOK_URL = "https://hook.eu2.make.com/4tq2cdq4j6xqhagxaw952ujc6i7gy42k"

# ⭐ 要跟 Meta Webhook 的「驗證權杖」一模一樣
VERIFY_TOKEN = "angelbot"


@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    print("⚡ Webhook Triggered, method =", request.method)

    # ====== FB/IG 第一次驗證用的 GET ======
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        print("👉 GET params:", {"mode": mode, "token": token, "challenge": challenge})

        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("✅ 驗證成功，回傳 challenge")
            return challenge, 200
        else:
            print("❌ 驗證失敗，token 不符")
            return "Error, invalid token", 403

    # ====== IG 真正傳來的事件（POST） ======
    if request.method == "POST":
        print("📩 收到原始 POST body：", request.data)
        data = request.json
        print("📩 解析後 JSON：", data)

        # ⭐ 轉送到 Make.com（非常重要）
        try:
            print("🚀 正在轉送到 Make:", MAKE_WEBHOOK_URL)
            resp = requests.post(MAKE_WEBHOOK_URL, json=data)
            print("✅ 已送出，Make 回應:", resp.status_code, resp.text)
        except Exception as e:
            print("❌ 轉送到 Make.com 失敗：", e)

        return "OK", 200


if __name__ == "__main__":
    app.run(port=80)
