from flask import Flask, request, jsonify, render_template
from score import calculate_score
from Mortgage import mortgage_estimator

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/score-page')
def score_page():
    return render_template('score.html', score=85, status="Good", survival="3 Months")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9001, debug=True)