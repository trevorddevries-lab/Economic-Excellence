from flask import Flask, request, jsonify, render_template
from score import calculate_score
from mortgage import mortgage_estimator  # ✅ NEW IMPORT

app = Flask(__name__)

# -------------------------------
# HOME PAGE
# -------------------------------
@app.route('/')
def home():
    return render_template('index.html')


# -------------------------------
# FEATURE 1: SURVIVAL SCORE (existing)
# -------------------------------
@app.route('/score')
def calculate():
    try:
        income = float(request.args.get('income', 0))
        rent = float(request.args.get('rent', 0))
        food = float(request.args.get('food', 0))
        transport = float(request.args.get('transport', 0))
        utils = float(request.args.get('utils', 0))

        score, survival = calculate_score(income, rent, food, transport, utils)

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
        return jsonify({"error": str(e)})


# -------------------------------
# FEATURE 2: MORTGAGE CALCULATOR (YOUR FEATURE)
# -------------------------------
@app.route('/mortgage')
def mortgage():
    try:
        credit_score = int(request.args.get('credit_score', 0))
        annual_income = float(request.args.get('annual_income', 0))
        monthly_debt = float(request.args.get('monthly_debt', 0))
        down_payment = float(request.args.get('down_payment', 0))
        home_price = float(request.args.get('home_price', 0))
        loan_term = int(request.args.get('loan_term', 30))

        result = mortgage_estimator(
            credit_score,
            annual_income,
            monthly_debt,
            down_payment,
            home_price,
            loan_term
        )

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)})


# -------------------------------
# RUN APP
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9001, debug=True)