import requests

# Base URL for your backend API
BASE_URL = "http://stocks4you.somee.com/api/stocks"  # Change the port if needed

def get_all_stocks():
    """Fetch all stocks from the API."""
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching stocks:", response.status_code, response.text)
        return None

def get_stock_by_id(stock_id):
    """Fetch a single stock by its ID."""
    response = requests.get(f"{BASE_URL}/{stock_id}")
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        print("Stock not found!")
    else:
        print("Error fetching stock:", response.status_code, response.text)
    return None

def add_stock(name, symbol, price, quantity):
    """Add a new stock."""
    stock_data = {
        "name": name,
        "symbol": symbol,
        "price": price,
        "quantity": quantity
    }
    response = requests.post(BASE_URL, json=stock_data)
    if response.status_code == 200:
        print("Stock added successfully!")
        return response.json()
    else:
        print("Error adding stock:", response.status_code, response.text)
        return None

def update_stock(stock_id, name, symbol, price, quantity):
    """Update an existing stock."""
    stock_data = {
        "id": stock_id,
        "name": name,
        "symbol": symbol,
        "price": price,
        "quantity": quantity
    }
    response = requests.put(f"{BASE_URL}/{stock_id}", json=stock_data)
    if response.status_code == 200:
        print("Stock updated successfully!")
    elif response.status_code == 404:
        print("Stock not found!")
    else:
        print("Error updating stock:", response.status_code, response.text)

def delete_stock(stock_id):
    """Delete a stock by ID."""
    response = requests.delete(f"{BASE_URL}/{stock_id}")
    if response.status_code == 200:
        print("Stock deleted successfully!")
    elif response.status_code == 404:
        print("Stock not found!")
    else:
        print("Error deleting stock:", response.status_code, response.text)

def get_details(symbol):
    """Fetch detailed stock information by symbol."""
    response = requests.get(f"{BASE_URL}/details/{symbol}")
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        print("Stock details not found!")
    else:
        print("Error fetching stock details:", response.status_code, response.text)
    return None


# Example usage
if __name__ == "__main__":
    data = get_details("AAPL")
    print(data) # '0.62'