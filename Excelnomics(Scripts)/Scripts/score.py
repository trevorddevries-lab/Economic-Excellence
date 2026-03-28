
rent = 0
food = 0
transport = 0
utils = 0

# total = rent + food + transport + utils
# test-total 
total = 3000
def survival_months():
    total_money = 5000 
    num_months = 0
    while total_money > 0:
        total_money = total_money - total
        num_months = num_months + 1

    return num_months


def main():
    # will calculate economic surival score monthly based on 
    # monthly income and expenses
    income = 0
    score = 100

    if income < total:
        score = score - 15
    
    survival = survival_months()
    if survival < 3:
        score = score - 10
    if survival > 4 and survival < 8:
        score = score - 5
    if survival > 9:
        score = score + 5

    print(score)

if __name__ == "__main__":
    main()