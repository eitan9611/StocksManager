import requests

BASE_URL = "http://localhost:5000/api"

def get_user(email):
    url = f"{BASE_URL}/user/{email}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else response.text

def create_user(user_data):
    url = f"{BASE_URL}/user/create"
    response = requests.post(url, json=user_data)
    return response.json() if response.status_code == 200 else response.text

def update_balance(email, amount):
    url = f"{BASE_URL}/user/balance/{email}"
    response = requests.put(url, json=amount)
    return response.json() if response.status_code == 200 else response.text

def get_all_users():
    url = f"{BASE_URL}/user"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else response.text

def buy_stock(email, symbol, quantity):
    url = f"{BASE_URL}/trade/buy"
    data = {"Email": email, "Symbol": symbol, "Quantity": quantity}
    response = requests.post(url, json=data)
    return response.json() if response.status_code == 200 else response.text

def sell_stock(email, symbol, quantity):
    url = f"{BASE_URL}/trade/sell"
    data = {"Email": email, "Symbol": symbol, "Quantity": quantity}
    response = requests.post(url, json=data)
    return response.json() if response.status_code == 200 else response.text

if __name__ == "__main__":
    email = "user@example.com"
    symbol = "AAPL"
    quantity = 5
    user_data = {"Email": email, "Balance": 1000.0}
    amount = 200.0

    print("Creating user...")
    print(create_user(user_data))

    print("Getting user...")
    print(get_user(email))

    print("Updating balance...")
    print(update_balance(email, amount))

    print("Getting all users...")
    print(get_all_users())

    print("Buying stock...")
    print(buy_stock(email, symbol, quantity))

    print("Selling stock...")
    print(sell_stock(email, symbol, quantity))
