import finnhub
import os
import time
import yfinance as yf
from dotenv import load_dotenv
from fredapi import Fred

load_dotenv()

class MarketData:
    def __init__(self):

        self._load_keys()
        self._init_clients()

    def _load_keys(self):
        self.finnhub_key = os.getenv("FINNHUB_API_KEY")
        self.fred_key = os.getenv("FRED_API_KEY")

        if not self.finnhub_key:
            raise Exception("FINNHUB API key not found")
        if not self.fred_key:
            raise Exception("FRED API key not found.")
        
    def _init_clients(self):
        self.finnhub = finnhub.Client(api_key=self.finnhub_key)
        self.fred = Fred(api_key=self.fred_key)

    def get_spy_price(self):
        quote = self.finnhub.quote("SPY")

        if not quote or quote.get("c") is None:
            raise Exception("Failed to fetch SPY price from Finnhub")
        return quote ["c"]
    
    def get_vix(self):
        vix = yf.Ticker("^VIX")
        data = vix.history(period="5d")

        if data.empty:
            raise Exception("Failed to fetch VIX data")
        
        return data ["Close"].iloc[-1]
    
    def get_ma200(self):
        spy = yf.Ticker("SPY")
        data = spy.history(period="1y")
        if data.empty:
            raise Exception("Failed to fetch SPY data")

        prices = data["Close"]
        
        return prices.rolling(window=200).mean().iloc[-1]
    
    def get_fed_funds_rate(self):
        data = self.fred.get_series("FEDFUNDS")
        return data.iloc[-1]
    
    def get_unemployment(self):
        data = self.fred.get_series("UNRATE")
        return data.iloc[-1]
    
    
class DecisionEngine:
    def evaluate(self, spy_price, ma200, vix, fed_rate, unemployment):
        score = 0
        reasons = []

        if spy_price < ma200:
            score -= 2
            reasons.append("SPY below 200-day average (bearish)")
        else:
            score += 2
            reasons.append("SPY above 200-day average (bullish)")

        if vix > 30:
            score -= 2
            reasons.append("High volatility (fear)")
        elif vix < 20:
            score += 1
            reasons.append("Low volatility (stable)")

        if fed_rate >4: 
            score -= 1
            reasons.append("High interest rates (tight liquidity)")
        else:
            score += 1
            reasons.append("Low interest rates (supportive)")

        if unemployment > 5:
            score -= 1
            reasons.append("Weak labor market")
        else:
            score += 1
            reasons.append("Strong labor market")

        return score, reasons
    
    
    def recommendation(self, score):
        if score <= -2:
            return "SELL"
        elif score >= 2:
            return "BUY"
        else:
            return "HOLD"
        
    def get_regime(self, score):
        if score <= -2:
            return "Risk-Off"
        elif score >= 2:
            return "Risk-On"
        else:
            return "Neutral"
        
class Portfolio:
    def __init__(self, shares):
        self.shares = shares
    
    def value(self,price):
        return self.shares * price
    

def main():

    market = MarketData()
    engine = DecisionEngine()
    portfolio = Portfolio(shares = 10000)

    data = {
        "spy": market.get_spy_price(),
        "vix": market.get_vix(),
        "ma200": market.get_ma200(),
        "fed": market.get_fed_funds_rate(),
        "unemp": market.get_unemployment()
    }

    spy_price = data["spy"]
    vix = data["vix"]
    ma200 = data["ma200"]
    fed_rate = data["fed"]
    unemployment = data["unemp"]

    score, reasons = engine.evaluate(data["spy"], data["ma200"], data["vix"], data["fed"], data["unemp"])
    action = engine.recommendation(score)
    regime = engine.get_regime(score)

    value = portfolio.value(data["spy"])

    print("\n==============================")
    print("   MARKET DASHBOARD")
    print("==============================")

    print(f"SPY         : ${spy_price:.2f}")
    print(f"Portfolio   : ${value:,.2f}")
    print(f"VIX         : {vix:.2f}")
    print(f"MA200       : {ma200:.2f}")
    print(f"Fed Rate    : {fed_rate:.2f}%")
    print(f"Unemployment: {unemployment:.2f}%")

    print("\n--- SIGNALS ---")
    for r in reasons:
        print(f"• {r}")

    print("\n--- DECISION ---")
    print(f"Score        : {score}")
    print(f"Action       : {action}")
    print(f"Regime       : {regime}")


if __name__ == "__main__":
    main()

