from datetime import datetime

def main():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time:", current_time)

    interest_rate = 0.0234 # change this

    if interest_rate > 0.2:
        print("Invest now")
    else:
        print("Don't invest")


if __name__ == "__main__":
    main()