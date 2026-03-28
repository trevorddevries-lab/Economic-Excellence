from flask import Flask, request, jsonify, render_template
from score import calculate_score
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/score')
def calculate():
    try:
        # Get values from frontend (query params)
        income = float(request.args.get('income', 0))
        rent = float(request.args.get('rent', 0))
        food = float(request.args.get('food', 0))
        transport = float(request.args.get('transport', 0))
        utils = float(request.args.get('utils', 0))

        # Call your score logic
        score, survival = calculate_score(income, rent, food, transport, utils)

        # Optional status labeling
        if score >= 90:
            status = "Excellent"
        elif score >= 75:
            status = "Good"
        elif score >= 60:
            status = "Moderate"
        else:
            status = "At Risk"

        return jsonify({
            "score": score,
            "survival_months": survival,
            "status": status
        })
    except Exception as e:
        return "Error"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9001)