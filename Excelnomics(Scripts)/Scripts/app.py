from flask import Flask, request, jsonify, render_template
from score import calculate_score
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['GET'])
def calculate():
    income = float(request.args.get('income', 0))
    rent = float(request.args.get('rent', 0))
    food = float(request.args.get('food', 0))
    transport = float(request.args.get('transport', 0))
    utils = float(request.args.get('utils', 0))

    result = calculate_score(income, rent, food, transport, utils)

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9001)