from flask import Flask, jsonify, request
import random
import time

app = Flask(__name__)


# Add CORS headers
@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    return response


# Dashboard stats
@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    # Simulate database delay
    time.sleep(0.2)

    # Add some randomness to make it look more realistic
    active_users = random.randint(24, 30)

    return jsonify({
        "active_users": {"count": active_users, "total": 80},
        "questions_answered": random.randint(3200, 3400),
        "avg_session_length": f"{random.randint(2, 3)}m {random.randint(10, 59)}s",
        "starting_knowledge": round(random.uniform(60.0, 68.0), 1),
        "current_knowledge": round(random.uniform(80.0, 90.0), 1),
        "knowledge_gain": round(random.uniform(30.0, 40.0), 1)
    })


# Stock info
@app.route('/api/stocks/<symbol>', methods=['GET'])
def get_stock_info(symbol):
    # Simulate database delay
    time.sleep(0.3)

    # Stock data (simulate with random values)
    stocks = {
        'AAPL': {
            "name": "Apple Inc.",
            "price": round(random.uniform(180.0, 190.0), 2),
            "change": round(random.uniform(-5.0, 7.0), 2),
            "market_cap": "2.8T",
            "pe_ratio": round(random.uniform(28.0, 32.0), 1),
            "dividend_yield": round(random.uniform(0.4, 0.6), 2),
            "description": "Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide. The company offers iPhone, a line of smartphones; Mac, a line of personal computers; iPad, a line of multi-purpose tablets; and wearables, home, and accessories."
        },
        'TSLA': {
            "name": "Tesla, Inc.",
            "price": round(random.uniform(220.0, 240.0), 2),
            "change": round(random.uniform(-8.0, 10.0), 2),
            "market_cap": "750B",
            "pe_ratio": round(random.uniform(60.0, 70.0), 1),
            "dividend_yield": 0.0,
            "description": "Tesla, Inc. designs, develops, manufactures, leases, and sells electric vehicles, and energy generation and storage systems. The company operates in two segments, Automotive, and Energy Generation and Storage."
        },
        'MSFT': {
            "name": "Microsoft Corporation",
            "price": round(random.uniform(370.0, 390.0), 2),
            "change": round(random.uniform(-6.0, 8.0), 2),
            "market_cap": "2.9T",
            "pe_ratio": round(random.uniform(35.0, 38.0), 1),
            "dividend_yield": round(random.uniform(0.7, 0.9), 2),
            "description": "Microsoft Corporation develops, licenses, and supports software, services, devices, and solutions worldwide. The company operates through three segments: Productivity and Business Processes, Intelligent Cloud, and More Personal Computing."
        }
    }

    # If symbol exists in our "database", return it
    stock_data = stocks.get(symbol.upper())
    if stock_data:
        # Calculate change percent based on price and change
        change_percent = (stock_data['change'] / (stock_data['price'] - stock_data['change'])) * 100
        stock_data['change_percent'] = round(change_percent, 2)
        return jsonify(stock_data)

    # Otherwise, generate some random data
    price = round(random.uniform(50.0, 200.0), 2)
    change = round(random.uniform(-10.0, 10.0), 2)
    change_percent = (change / (price - change)) * 100

    return jsonify({
        "name": f"{symbol.upper()} Inc.",
        "price": price,
        "change": change,
        "change_percent": round(change_percent, 2),
        "market_cap": f"{random.randint(1, 500)}B",
        "pe_ratio": round(random.uniform(10.0, 50.0), 1),
        "dividend_yield": round(random.uniform(0.0, 3.0), 2),
        "description": f"This is a placeholder description for {symbol.upper()}. No detailed information is available for this stock symbol."
    })


# Chat API
@app.route('/api/chat', methods=['POST'])
def get_chat_response():
    # Simulate API delay
    time.sleep(0.5)

    data = request.json
    user_message = data.get('message', '')

    # Simple responses based on keywords
    responses = [
        ("hello",
         ["Hello! How can I help you today?", "Hi there! How can I assist you?", "Greetings! What can I do for you?"]),
        ("stock", ["I can help you find information about stocks. Just use the Stock Info page.",
                   "Are you interested in investing? Check out our Stock Info page for more details."]),
        ("help", ["I'm here to help! You can ask me about stocks, dashboard information, or general questions.",
                  "How can I assist you today? I can provide information about various topics."]),
        ("thank", ["You're welcome!", "Happy to help!", "My pleasure!"]),
        ("bye", ["Goodbye! Have a great day!", "See you later!", "Take care!"])
    ]

    # Check for keyword matches
    for keyword, replies in responses:
        if keyword in user_message.lower():
            return jsonify({"response": random.choice(replies)})

    # Default responses
    default_responses = [
        f"I received your message: '{user_message}'. How can I help further?",
        "That's interesting. Can you tell me more about what you're looking for?",
        "I understand you're asking about that. Let me help you find the information you need.",
        "Thanks for your question. Would you like more specific information about this topic?"
    ]

    return jsonify({"response": random.choice(default_responses)})


if __name__ == '__main__':
    print("Starting backend server at http://localhost:5000")
    app.run(debug=True)