import requests

BASE_URL = "http://localhost:5050/api/User"

def get_user(email):
    url = f"{BASE_URL}/{email}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else response.text

def create_user(email):
    url = f"{BASE_URL}/create/{email}"
    response = requests.post(url)
    return response.text if response.status_code == 200 else "error"

def update_balance(email, amount):
    url = f"{BASE_URL}/balance/{email}"
    response = requests.put(url, json=amount)
    return response.json() if response.status_code == 200 else response.text

def get_all_users():
    url = f"{BASE_URL}/get_all_users"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else response.text



if __name__ == "__main__":
    email = "eitan@"
    #print("create user...")
    #print(create_user(email))

    print(get_user(email))

