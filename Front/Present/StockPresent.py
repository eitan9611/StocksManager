import yfinance as yf
import datetime
from Model.StockModel import *


def get_prices_last_year(symbol):
    today = datetime.date.today()
    day = today.day
    prices = []

    for i in range(12):
        # Calculate target month and year
        month = today.month - i
        year = today.year
        if month <= 0:
            month += 12
            year -= 1

        # Attempt to use the same day number, or fallback to last valid day of the month
        try:
            target_day = datetime.date(year, month, day)
        except ValueError:
            target_day = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)

        # In the first iteration, use (yesterday, today), otherwise (target_day, target_day+5 or today)
        if i == 0:
            start = today - datetime.timedelta(days=1)
            end = today
        else:
            end = min(target_day + datetime.timedelta(days=5), today)
            start = target_day

        ticker = yf.Ticker(symbol)
        hist = ticker.history(start=start, end=end)

        if not hist.empty:
            price = hist.iloc[0]['Close']
            prices.insert(0, round(float(price), 2))
        else:
            prices.insert(0, None)

    return prices

def get_prices_last_week(symbol):
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="7d")

    if not hist.empty:
        return [round(float(price), 2) for price in hist['Close']]
    return [None] * 7

def getStockDetails(symbol):
    """Presentation layer function to fetch and display stock details."""
    details = get_details(symbol)
    if details:
        return details
    else:
        return f"Details for symbol '{symbol}' not found."

if __name__ == "__main__":
    symbol = "AAPL"

    print("details: ", getStockDetails(symbol))
    print("last week: ", get_prices_last_week(symbol))
    print("last year: ", get_prices_last_year(symbol))
