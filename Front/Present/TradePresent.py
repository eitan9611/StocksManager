from datetime import datetime
from Model.TradeModel import *

def format_trades_for_view(email):
    trades = get_trades_by_user(email)

    if isinstance(trades, str):
        return [["Error", trades]]  # Error message as a row

    if not trades:
        return [["No trades found"]]

    formatted_data = []

    for trade in trades:
        date = trade.get("timestamp", "")
        try:
            date = datetime.fromisoformat(date).strftime('%Y-%m-%d')
        except:
            date = str(date)

        symbol = trade.get("symbol", "N/A")
        quantity = int(trade.get("quantity", 0))
        price = float(trade.get("price", 0.0))
        total = quantity * price
        type_ = trade.get("type", "")

        formatted_data.append([
            type_,          # Buy or Sell
            date,
            symbol,
            str(quantity),
            f"${price:.2f}",
            f"${total:,.2f}"
        ])

    return formatted_data

def handle_buy_stock(email, symbol, quantity):
    result = buy_stock(email, symbol, quantity)
    if result != "error":
        return True, "Buy order successful."
    else:
        return False, f"Buy failed: {result}"

def handle_sell_stock(email, symbol, quantity):
    result = sell_stock(email, symbol, quantity)
    if result != "error":
        return True, "Sell order successful."
    else:
        return False, f"Sell failed: {result}"

# Example usage
if __name__ == "__main__":
    email = "eitan@"
    symbol = "AAPL"
    quantity = 5

    success, message = handle_buy_stock(email, symbol, quantity)
    print("Buy:", message)

    success, message = handle_sell_stock(email, symbol, quantity)
    print("Sell:", message)

    print(format_trades_for_view(email))
