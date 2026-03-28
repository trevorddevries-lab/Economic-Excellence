from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# -------------------------------
# Interest Rate Based on Credit Score
# -------------------------------
def get_interest_rate(credit_score):
    if credit_score >= 760:
        return 0.0625
    elif credit_score >= 700:
        return 0.065
    elif credit_score >= 660:
        return 0.07
    elif credit_score >= 620:
        return 0.075
    else:
        return 0.085


# -------------------------------
# Monthly Mortgage Payment
# -------------------------------
def calculate_monthly_mortgage(loan_amount, annual_rate, years):
    r = annual_rate / 12
    n = years * 12

    if r == 0:
        return loan_amount / n

    return loan_amount * (r * (1 + r)**n) / ((1 + r)**n - 1)


# -------------------------------
# Taxes, Insurance, PMI (FIXED)
# -------------------------------
def calculate_additional_costs(home_price, down_payment):
    TAX_RATE = 0.01
    INSURANCE_RATE = 0.005

    tax = (home_price * TAX_RATE) / 12
    insurance = (home_price * INSURANCE_RATE) / 12

    down_percent = down_payment / home_price
    loan_amount = home_price - down_payment

    if down_percent < 0.20:
        pmi = (loan_amount * 0.005) / 12
    else:
        pmi = 0

    return tax, insurance, pmi


# -------------------------------
# Max Affordable Home Price
# -------------------------------
def calculate_max_affordable_home(credit_score, annual_income, monthly_debt, down_payment, loan_term):

    monthly_income = annual_income / 12

    max_housing = monthly_income * 0.28
    max_total = monthly_income * 0.36

    allowed_housing = min(max_housing, max_total - monthly_debt)

    if allowed_housing <= 0:
        return 0

    interest_rate = get_interest_rate(credit_score)
    r = interest_rate / 12
    n = loan_term * 12

    home_price = 50000
    step = 1000
    best_price = 0

    while home_price <= 2000000:
        tax = (home_price * 0.01) / 12
        insurance = (home_price * 0.005) / 12

        down_percent = down_payment / home_price
        loan_amount = home_price - down_payment

        if down_percent < 0.20:
            pmi = (loan_amount * 0.005) / 12
        else:
            pmi = 0

        remaining = allowed_housing - (tax + insurance + pmi)

        if remaining <= 0:
            break

        loan = remaining * ((1 + r)**n - 1) / (r * (1 + r)**n)
        estimated_price = loan + down_payment

        if estimated_price >= home_price:
            best_price = home_price
            home_price += step
        else:
            break

    return best_price


# -------------------------------
# Main Estimator
# -------------------------------
def mortgage_estimator(credit_score, income, debt, down_payment, home_price, term):

    monthly_income = income / 12
    loan_amount = home_price - down_payment

    rate = get_interest_rate(credit_score)

    mortgage = calculate_monthly_mortgage(loan_amount, rate, term)
    tax, insurance, pmi = calculate_additional_costs(home_price, down_payment)

    total_cost = mortgage + tax + insurance + pmi

    housing_ratio = total_cost / monthly_income
    debt_ratio = (total_cost + debt) / monthly_income

    max_price = calculate_max_affordable_home(
        credit_score, income, debt, down_payment, term
    )

    return {
        "interest_rate": round(rate * 100, 2),
        "mortgage": round(mortgage, 2),
        "tax": round(tax, 2),
        "insurance": round(insurance, 2),
        "pmi": round(pmi, 2),
        "total_cost": round(total_cost, 2),
        "housing_ratio": round(housing_ratio * 100, 2),
        "debt_ratio": round(debt_ratio * 100, 2),
        "affordable": housing_ratio <= 0.28 and debt_ratio <= 0.36,
        "pmi_active": down_payment / home_price < 0.20,
        "max_home_price": int(max_price)
    }


# -------------------------------
# ROUTES
# -------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/calculate_mortgage", methods=["POST"])
def calculate_mortgage_api():
    data = request.get_json()

    result = mortgage_estimator(
        int(data["credit_score"]),
        float(data["income"]),
        float(data["debt"]),
        float(data["down_payment"]),
        float(data["home_price"]),
        int(data["term"])
    )

    return jsonify(result)


# -------------------------------
# RUN
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)