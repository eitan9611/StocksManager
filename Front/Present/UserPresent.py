# userPresent.py
from Model.UserModel import *

def userStatus(email):
    user_data = get_user(email)
    name = email.split("@")[0]

    #if the user doesn't exist - create it
    if not isinstance(user_data, dict):
        create_user(email)
        return "Welcome, " + name

    else:
        return "Welcome back, " + name
def getBalance(email):
    user_data = get_user(email)
    return user_data["balance"]

def getStocks(email):
    user_data = get_user(email)
    if isinstance(user_data, dict) and "portfolio" in user_data:
        return user_data["portfolio"]
    return []

if __name__ == "__main__":
    email = "newUser@"

    print(userStatus(email))

