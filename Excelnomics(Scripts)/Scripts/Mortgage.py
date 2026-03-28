import math

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
    monthly_rate = annual_rate / 12
    n = years * 12

    if monthly_rate == 0:
        return loan_amount / n

    return loan_amount * (monthly_rate * (1 + monthly_rate)**n) / ((1 + monthly_rate)**n - 1)


# -------------------------------
# Taxes, Insurance, PMI (FIXED)
# -------------------------------
def calculate_additional_costs(home_price, down_payment):
    """
    Monthly costs:
    - Property tax: 1.2% yearly → monthly
    - Insurance: 0.5% yearly → monthly
    - PMI: ONLY if down payment < 20%, based on LOAN amount
    """

    property_tax = (home_price * 0.012) / 12
    insurance = (home_price * 0.005) / 12

    down_percent = down_payment / home_price
    loan_amount = home_price - down_payment

    if down_percent < 0.20:
        pmi = (loan_amount * 0.005) / 12
    else:
        pmi = 0

    return property_tax, insurance, pmi


# -------------------------------
# Affordability Check (28/36 rule)
# -------------------------------
def affordability_check(monthly_income, monthly_debt, housing_cost):
    housing_ratio = housing_cost / monthly_income
    total_debt_ratio = (housing_cost + monthly_debt) / monthly_income

    affordable = housing_ratio <= 0.28 and total_debt_ratio <= 0.36

    return housing_ratio, total_debt_ratio, affordable


# -------------------------------
# Max Affordable Home Price
# -------------------------------
def calculate_max_affordable_home(credit_score, annual_income, monthly_debt, down_payment, loan_term):

    monthly_income = annual_income / 12

    max_housing = monthly_income * 0.28
    max_total_debt = monthly_income * 0.36

    allowed_housing = min(max_housing, max_total_debt - monthly_debt)

    if allowed_housing <= 0:
        return 0

    interest_rate = get_interest_rate(credit_score)
    r = interest_rate / 12
    n = loan_term * 12

    home_price = 50000
    step = 1000
    best_price = 0

    while home_price <= 2000000:
        tax = (home_price * 0.012) / 12
        insurance = (home_price * 0.005) / 12

        down_percent = down_payment / home_price
        loan_amount = home_price - down_payment

        if down_percent < 0.20:
            pmi = (loan_amount * 0.005) / 12
        else:
            pmi = 0

        remaining_for_mortgage = allowed_housing - (tax + insurance + pmi)

        if remaining_for_mortgage <= 0:
            break

        loan = remaining_for_mortgage * ((1 + r)**n - 1) / (r * (1 + r)**n)

        estimated_price = loan + down_payment

        if estimated_price >= home_price:
            best_price = home_price
            home_price += step
        else:
            break

    return best_price


# -------------------------------
# Full Estimator
# -------------------------------
def mortgage_estimator(credit_score, annual_income, monthly_debt, down_payment, home_price, loan_term):

    monthly_income = annual_income / 12
    loan_amount = home_price - down_payment

    interest_rate = get_interest_rate(credit_score)

    mortgage = calculate_monthly_mortgage(loan_amount, interest_rate, loan_term)
    tax, insurance, pmi = calculate_additional_costs(home_price, down_payment)

    total_cost = mortgage + tax + insurance + pmi

    housing_ratio, debt_ratio, affordable = affordability_check(monthly_income, monthly_debt, total_cost)

    max_price = calculate_max_affordable_home(credit_score, annual_income, monthly_debt, down_payment, loan_term)

    return {
        "interest_rate": interest_rate * 100,
        "mortgage": mortgage,
        "tax": tax,
        "insurance": insurance,
        "pmi": pmi,
        "total_cost": total_cost,
        "housing_ratio": housing_ratio,
        "debt_ratio": debt_ratio,
        "affordable": affordable,
        "max_home_price": max_price,
        "pmi_active": down_payment / home_price < 0.20
    }


# -------------------------------
# MANUAL INPUTS (EDIT THESE)
# -------------------------------
if __name__ == "__main__":

    credit_score = 730
    annual_income = 120000
    monthly_debt = 1000
    down_payment = 50000
    home_price = 450000
    loan_term = 30

    result = mortgage_estimator(
        credit_score,
        annual_income,
        monthly_debt,
        down_payment,
        home_price,
        loan_term
    )

    print("\n========== RESULTS ==========")

    print("\n--- CURRENT HOUSE ---")
    print(f"Home Price: ${home_price}")
    print(f"Interest Rate: {result['interest_rate']:.2f}%")
    print(f"Mortgage Payment: ${result['mortgage']:.2f}")
    print(f"Monthly Tax: ${result['tax']:.2f}")
    print(f"Insurance: ${result['insurance']:.2f}")
    print(f"PMI: ${result['pmi']:.2f}")
    print(f"PMI Active: {'YES' if result['pmi_active'] else 'NO'}")
    print(f"Total Monthly Cost: ${result['total_cost']:.2f}")

    print("\n--- AFFORDABILITY ---")
    print(f"Housing Ratio: {result['housing_ratio']*100:.2f}%")
    print(f"Debt Ratio: {result['debt_ratio']*100:.2f}%")

    if result["affordable"]:
        print("✅ AFFORDABLE")
    else:
        print("⚠️ NOT AFFORDABLE")

    print("\n--- MAX AFFORDABLE HOME PRICE ---")
    print(f"💡 You can afford up to: ${result['max_home_price']:,}")