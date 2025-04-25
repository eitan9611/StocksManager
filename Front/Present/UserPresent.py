# userPresent.py
from Model.UserModel import *

def getBalance(email):
    user_data = get_user(email)
    if isinstance(user_data, dict) and "balance" in user_data:
        return user_data["balance"]
    return None

def getStocks(email):
    user_data = get_user(email)
    if isinstance(user_data, dict) and "portfolio" in user_data:
        return user_data["portfolio"]
    return []

if __name__ == "__main__":
    email = "eitan@"

    print("balance:", getBalance(email))
    print("stocks:", getStocks(email))

