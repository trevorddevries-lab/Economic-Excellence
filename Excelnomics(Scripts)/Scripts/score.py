
# Calculates an overall finacial score based on monthly 
# income and expenses
def survival_months(total_expenses):
    total_money = 5000
    num_months = 0

    while total_money > 0:
        total_money -= total_expenses
        num_months += 1

    return num_months


def calculate_score(income, rent, food, transport, utils):
    total_expenses = rent + food + transport + utils
    score = 100

    if income < total_expenses:
        score -= 15

    survival = survival_months(total_expenses)

    if survival < 3:
        score -= 10
    if 4 < survival < 8:
        score -= 5
    if survival > 9:
        score += 5

    return score, survival