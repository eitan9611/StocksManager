import yfinance as yf
import datetime
from Model.StockModel import *
import requests


def get_prices_last_year(symbol):
    today = datetime.date.today()
    day = today.day
    x_values = []
    y_values = []
    
    for i in range(12):
        month = today.month - i
        year = today.year
        
        if month <= 0:
            month += 12
            year -= 1
        
        try:
            target_day = datetime.date(year, month, day)
        except ValueError:
            # Handle cases like February 30
            target_day = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)
        
        start = target_day
        end = target_day + datetime.timedelta(days=5)
        if end > today:
            end = today
        
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(start=start, end=end)
            
            if not hist.empty:
                price = hist.iloc[0]['Close']
                if price is not None:
                    x_values.insert(0, target_day.strftime('%b'))
                    y_values.insert(0, round(float(price), 2))
        except Exception as e:
            print(f"Error fetching data for {symbol} at {target_day}: {e}")
            # Skip this month if there's an error
    
    # Ensure we have at least one value
    if not x_values:
        x_values = ['N/A']
        y_values = [0.0]
        
    return x_values, y_values

def get_prices_last_week(symbol):
    x_values = []
    y_values = []
    
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="7d")
        
        if not hist.empty:
            for idx, row in hist.iterrows():
                price = row['Close']
                if price is not None:
                    weekday = idx.strftime('%a')
                    x_values.append(weekday)
                    y_values.append(round(float(price), 2))
    except Exception as e:
        print(f"Error fetching weekly data for {symbol}: {e}")
    
    # Ensure we have at least one value
    if not x_values:
        x_values = ['N/A']
        y_values = [0.0]
        
    return x_values, y_values


def get_prices_today(symbol):
    """Get hourly stock prices for the current day."""
    x_values = []  # Hours
    y_values = []  # Prices
    
    try:
        ticker = yf.Ticker(symbol)
        # Get intraday data with 1-hour intervals
        hist = ticker.history(period="1d", interval="1h")
        
        if not hist.empty:
            for idx, row in hist.iterrows():
                price = row['Close']
                if price is not None:
                    hour = idx.strftime('%H:%M')
                    x_values.append(hour)
                    y_values.append(round(float(price), 2))
    except Exception as e:
        print(f"Error fetching daily data for {symbol}: {e}")
    
    # Ensure we have values for all 24 hours
    now = datetime.datetime.now()
    hour_labels = []
    hour_prices = [0.0] * 24  # Default values
    
    # Create labels for all 24 hours
    for i in range(24):
        hour = f"{i:02d}:00"
        hour_labels.append(hour)
    
    # Fill in the actual prices we have
    for i, hour_label in enumerate(x_values):
        if i < len(hour_labels):
            hour_index = int(hour_label.split(':')[0])
            if 0 <= hour_index < 24:
                hour_prices[hour_index] = y_values[i]
    
    return hour_labels, hour_prices

def get_prices_last_month(symbol):
    """Get weekly stock prices for the last month."""
    today = datetime.date.today()
    x_values = []  # Week labels
    y_values = []  # Prices
    
    # Calculate date one month ago
    month_ago = today.month - 1
    year = today.year
    if month_ago <= 0:
        month_ago += 12
        year -= 1
    
    try:
        start_date = datetime.date(year, month_ago, today.day)
    except ValueError:
        # Handle cases like February 30
        start_date = datetime.date(year, month_ago + 1, 1) - datetime.timedelta(days=1)
    
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(start=start_date, end=today)
        
        if not hist.empty:
            # Divide the month into 4 weeks
            days_in_period = (today - start_date).days
            days_per_week = max(1, days_in_period // 4)
            
            for i in range(4):
                week_start = start_date + datetime.timedelta(days=i * days_per_week)
                week_end = week_start + datetime.timedelta(days=days_per_week)
                if week_end > today:
                    week_end = today
                
                # Get data for this week
                week_data = hist.loc[str(week_start):str(week_end)]
                if not week_data.empty:
                    avg_price = week_data['Close'].mean()
                    week_label = f"W{i+1}"
                    x_values.append(week_label)
                    y_values.append(round(float(avg_price), 2))
    except Exception as e:
        print(f"Error fetching monthly data for {symbol}: {e}")
    
    # Ensure we have at least one value (or fill with 4 weeks if empty)
    if not x_values or len(x_values) < 4:
        missing_weeks = 4 - len(x_values)
        for i in range(missing_weeks):
            x_values.append(f"W{i+1+len(x_values)}")
            y_values.append(0.0)  # Default value when no data is available
    
    return x_values, y_values



def getStockDetails(symbol):
    """Presentation layer function to fetch and display stock details."""
    details = get_details(symbol)
    if details:
        return True, details
    else:
        return False, f"Details for symbol '{symbol}' not found."

def getCompanyDescription(symbol):
        """Fetch company description using Alpha Vantage."""
        try:
            api_key = "I39K602M3LZF843Q"
            url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={api_key}"
            response = requests.get(url)
            data = response.json()
            
            if data and 'Description' in data:
                return True, data['Description']
            else:
                return False, "No description available or invalid symbol."
        except Exception as e:
            print(f"Error fetching description: {e}")
            return False, "An error occurred while fetching the description."
        

from io import BytesIO
def get_company_logo(symbol):
    api_key = 'pk_KvBNiwpzRHanMOE-lveuow'  # Replace with your actual API key
    # get the company name:
    #print(f"domain in start: {symbol}") 
    ticker = yf.Ticker(symbol)
    company_name = ticker.info.get('longName', 'Unknown Company')
    # get the domain name:
    raw_domain = ticker.info.get('website', 'Unknown Domain')
    domain = clean_domain(raw_domain)
    url = f'https://img.logo.dev/{domain}?token={api_key}&format=png'
    #print(f"url: {url}")
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        #with open("test_logo.png", "wb") as f:
        #    f.write(response.content)
        #print(f"response: {response}")
        return response
    except Exception as e:
        print(f"Error fetching logo: {e}")
        return None
    
from urllib.parse import urlparse

def clean_domain(raw_url):
    if not raw_url.startswith('http'):
        raw_url = 'http://' + raw_url  # Ensure it's a valid URL format

    parsed = urlparse(raw_url)
    hostname = parsed.hostname or raw_url

    # Strip "www." if present
    if hostname.startswith('www.'):
        hostname = hostname[4:]

    return hostname


if __name__ == "__main__":
    symbol = "AAPL"

    print("details: ", getStockDetails(symbol))
    print("last week: ", get_prices_last_week(symbol))
    print("last year: ", get_prices_last_year(symbol))
