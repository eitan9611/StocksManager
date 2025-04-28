import yfinance as yf
import datetime
from Model.StockModel import *
import requests


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
        return True, details
    else:
        return False, f"Details for symbol '{symbol}' not found."


from io import BytesIO
def getStockLogo(symbol):
    """Fetch stock information and logo using Alpha Vantage."""
    try:
        # Using the provided Alpha Vantage API key
        api_key = "I39K602M3LZF843Q"
        
        # First try to get company information from Alpha Vantage
        url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={api_key}"
        response = requests.get(url)
        data = response.json()
        
        if data and 'Symbol' in data:
            # Alpha Vantage doesn't provide logos directly in their API
            # So we'll use a service that generates logos based on the company name or symbol
            
            # If company name is available, use it for a better logo
            if 'Name' in data and data['Name']:
                company_name = data['Name'].split(' ')[0]  # Use first word of company name
                logo_url = f"https://ui-avatars.com/api/?name={company_name}&background=random&color=fff&size=150&bold=true"
            else:
                # Fall back to using the symbol
                logo_url = f"https://ui-avatars.com/api/?name={symbol}&background=random&color=fff&size=150&bold=true"
                
            logo_response = requests.get(logo_url)
            return logo_response
        else:
            # If Alpha Vantage doesn't have data, just generate a logo from the symbol
            logo_url = f"https://ui-avatars.com/api/?name={symbol}&background=random&color=fff&size=150&bold=true"
            return requests.get(logo_url)
            
    except Exception as e:
        print(f"Error in getStockLogo: {e}")
        
        # As a last resort, still try to return a generated logo
        try:
            logo_url = f"https://ui-avatars.com/api/?name={symbol}&background=random&color=fff&size=150&bold=true"
            return requests.get(logo_url)
        except:
            return None


if __name__ == "__main__":
    symbol = "AAPL"

    print("details: ", getStockDetails(symbol))
    print("last week: ", get_prices_last_week(symbol))
    print("last year: ", get_prices_last_year(symbol))
