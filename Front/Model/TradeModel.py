import requests

BASE_URL = "http://localhost:5000/api/trade"  # Adjust as needed

def buy_stock(email, symbol, quantity):
    url = f"{BASE_URL}/buy"
    data = {"Email": email, "Symbol": symbol, "Quantity": quantity}
    response = requests.post(url, json=data)
    return response.json() if response.status_code == 200 else response.text

def sell_stock(email, symbol, quantity):
    url = f"{BASE_URL}/sell"
    data = {"Email": email, "Symbol": symbol, "Quantity": quantity}
    response = requests.post(url, json=data)
    return response.json() if response.status_code == 200 else response.text

if __name__ == "__main__":
    email = "user@example.com"
    symbol = "AAPL"
    quantity = 5

    print("Buying stock...")
    print(buy_stock(email, symbol, quantity))

    print("Selling stock...")
    print(sell_stock(email, symbol, quantity))
