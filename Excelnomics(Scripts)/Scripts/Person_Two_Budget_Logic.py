#CATEGORY DEFINITIONS
NEEDS = [
    "rent",
    "utilities",
    "groceries",
    "transport",
    "insurance",
    "debt_minimums"
]

WANTS = [
    "subscriptions",
    "eating_out",
    "shopping",
    "entertainment",
    "travel",
    "hobbies"
]

SAVINGS = [
    "savings",
    "investments"
]


#INPUT FUNCTIONS
def get_float_input(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Value cannot be negative.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def get_income_type():
    while True:
        choice = input("Enter income type (monthly/biweekly): ").lower()
        if choice in ["monthly", "biweekly"]:
            return choice
        print("Please enter 'monthly' or 'biweekly'.")


def get_crisis_mode():
    while True:
        choice = input("Enable crisis mode? (y/n): ").lower()
        if choice in ["y", "n"]:
            return choice == "y"
        print("Enter 'y' or 'n'.")


def get_expenses():
    expenses = {}

    print("\nEnter your monthly expenses: ")
    for category in NEEDS + WANTS + SAVINGS:
        value = get_float_input(f"{category.capitalize()}: $")
        expenses[category] = value
    
    return expenses


#CORE CALCULATIONS
def calculate_monthly_income(income, income_type):
    if income_type == "biweekly":
        return income * 26 / 12
    return income


def calculate_total_expenses(expenses):
    return sum(expenses.values())


def categorize_expenses(expenses):
    needs_total = sum(expenses[k] for k in NEEDS if k in expenses)
    wants_total = sum(expenses[k] for k in WANTS if k in expenses)
    savings_total = sum(expenses[k] for k in SAVINGS if k in expenses)
    return needs_total, wants_total, savings_total


def calculate_budget(monthly_income, needs_total, savings_total):
    # Wants is now dynamic remainder
    wants_budget = monthly_income - (needs_total + savings_total)

    return {
        "needs": needs_total,  # actual spending
        "wants": max(wants_budget, 0),  # prevent negative display
        "savings": savings_total  # actual savings
    }


def calculate_crisis_budget(monthly_income):
    return {
        "needs": monthly_income * 0.7,
        "wants": monthly_income * 0.1,
        "savings": monthly_income * 0.2
    }


def calculate_leftover(income, total_expenses):
    return income - total_expenses


def get_risk_level(leftover):
    if leftover > 0:
        return "LOW"
    elif leftover == 0:
        return "MEDIUM"
    else:
        return "HIGH"


#BUDGET VIOLATION LOGIC
def check_budget_status(needs_total, wants_total, savings_total, budget, leftover):
    alerts = []

    if wants_total > budget["wants"]:
        alerts.append("Wants exceed available money after needs and savings.")

    if savings_total <= 0:
        alerts.append("No savings detected. Consider saving money.")

    if leftover < 0:
        alerts.append("You are losing money every month.")

    return alerts


#UTILITIES
def round_dict(d):
    return {k: round(v, 2) for k, v in d.items()}


def calculate_percentages(needs_total, wants_total, savings_total, income):
    if income <= 0:
        return {
            "needs_pct": 0,
            "wants_pct": 0,
            "savings_pct": 0
        }
    return {
        "needs_pct": round((needs_total / income) * 100, 1),
        "wants_pct": round((wants_total / income) * 100, 1),
        "savings_pct": round((savings_total / income) * 100, 1)
    }


#MAIN ANALYSIS FUNCTION
def run_budget_analysis(income, income_type, expenses, crisis_mode=False):
    monthly_income = calculate_monthly_income(income, income_type)
    total_expenses = calculate_total_expenses(expenses)

    needs_total, wants_total, savings_total = categorize_expenses(expenses)

    percentages = calculate_percentages(
        needs_total, wants_total, savings_total, monthly_income
    )

    if crisis_mode:
        budget = calculate_crisis_budget(monthly_income)
    else:
        budget = calculate_budget(monthly_income, needs_total, savings_total)

    leftover = calculate_leftover(monthly_income, total_expenses)

    alerts = check_budget_status(
        needs_total, wants_total, savings_total, budget, leftover
    )

    return {
        "monthly_income": round(monthly_income, 2),
        "total_expenses": round(total_expenses, 2),
        "needs_total": round(needs_total, 2),
        "wants_total": round(wants_total, 2),
        "savings_total": round(savings_total, 2),
        "budget": round_dict(budget),
        "leftover": round(leftover, 2),
        "percentages": percentages,
        "alerts": alerts,
        "risk_level": get_risk_level(leftover)
    }


#TEST RUN (REMOVE LATER)
if __name__ == "__main__":
    print("===== FINANCIAL SURVIVAL TOOL =====\n")

    income_type = get_income_type()
    income = get_float_input("Enter your income: $")
    expenses = get_expenses()
    crisis_mode = get_crisis_mode()

    result = run_budget_analysis(income, income_type, expenses, crisis_mode)

    print("\n=== Results ===")
    for key, value in result.items():
        print(f"{key}: {value}")