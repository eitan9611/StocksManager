import requests

BASE_URL = "http://stocks4you.somee.com/api/trade"  # Adjust as needed

def buy_stock(email, symbol, quantity):
    url = f"{BASE_URL}/buy"
    data = {"Email": email, "Symbol": symbol, "Quantity": quantity}
    response = requests.post(url, json=data)
    return response.text if response.status_code == 200 else "error"

def sell_stock(email, symbol, quantity):
    url = f"{BASE_URL}/sell"
    data = {"Email": email, "Symbol": symbol, "Quantity": quantity}
    response = requests.post(url, json=data)
    return response.text if response.status_code == 200 else "error"

def get_trades_by_user(email):
    url = f"{BASE_URL}/trades/{email}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else response.text
