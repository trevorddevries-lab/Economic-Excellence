from flask import Flask, request, jsonify, render_template
from score import calculate_score
from Mortgage import mortgage_estimator
from portfolio import get_market_snapshot

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/score-page')
def score_page():
    return render_template('score.html', score=85, status="Good", survival="3 Months")

@app.route("/portfolio-data")
def portfolio_data():
    try:
        data = get_market_snapshot()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9001, debug=True)