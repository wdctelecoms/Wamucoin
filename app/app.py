from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

SCAM_KEYWORDS = {
    "urgent": 15,
    "act now": 15,
    "limited time": 10,
    "guaranteed": 20,
    "double your money": 30,
    "risk free": 20,
    "send money": 20,
    "verify your account": 15,
    "click link": 15,
    "free money": 25,
    "bitcoin giveaway": 30,
    "account suspended": 20,
}

def analyze_message(text):
    score = 0
    reasons = []
    text = text.lower()

    for word, weight in SCAM_KEYWORDS.items():
        if word in text:
            score += weight
            reasons.append(f"Suspicious phrase detected: '{word}'")

    score = min(score, 100)

    if score >= 70:
        risk = "High Risk 🚨"
    elif score >= 40:
        risk = "Medium Risk ⚠️"
    else:
        risk = "Low Risk ✅"

    return score, risk, reasons

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        message = request.form.get("message", "")
        score, risk, reasons = analyze_message(message)
        result = {
            "score": score,
            "risk": risk,
            "reasons": reasons
        }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
