from typing import Dict, List, Any, Optional
import json
import time
import requests


class ApiClient:
    """Client for communicating with the backend API."""

    def __init__(self, base_url: str = "http://localhost:5000/api"):
        """Initialize the API client with a base URL."""
        self.base_url = base_url
        self.session = requests.Session()

    def get_dashboard_stats(self) -> Dict[str, Any]:
        """
        Get statistics for the dashboard.

        Returns:
            Dictionary containing dashboard statistics:
            - active_users: Dict with count and total
            - questions_answered: int
            - avg_session_length: str
            - starting_knowledge: float (percentage)
            - current_knowledge: float (percentage)
            - knowledge_gain: float (percentage)
        """
        # TODO: Replace with actual API call
        endpoint = f"{self.base_url}/dashboard/stats"
        try:
            response = self.session.get(endpoint)
            return response.json()
        except Exception as e:
            print(f"Error fetching dashboard stats: {e}")
            # Return dummy data as fallback
            return {
                "active_users": {"count": 27, "total": 80},
                "questions_answered": 3298,
                "avg_session_length": "2m 34s",
                "starting_knowledge": 64.0,
                "current_knowledge": 86.0,
                "knowledge_gain": 34.0
            }

    def get_stock_info(self, symbol: str) -> Dict[str, Any]:
        """
        Get information about a specific stock.

        Args:
            symbol: Stock symbol (e.g., AAPL, TSLA)

        Returns:
            Dictionary containing stock information
        """
        # TODO: Replace with actual API call
        endpoint = f"{self.base_url}/stocks/{symbol}"
        try:
            response = self.session.get(endpoint)
            return response.json()
        except Exception as e:
            print(f"Error fetching stock info for {symbol}: {e}")
            # Return dummy data as fallback
            return {
                "name": f"{symbol} Inc.",
                "price": 150.25,
                "change": 2.5,
                "change_percent": 1.7,
                "market_cap": "2.5T",
                "pe_ratio": 30.5,
                "dividend_yield": 0.5,
                "description": f"This is a placeholder description for {symbol}."
            }

    def get_chat_response(self, message: str) -> str:
        """
        Get a response from the chatbot.

        Args:
            message: User's message

        Returns:
            Chatbot's response
        """
        # TODO: Replace with actual API call
        endpoint = f"{self.base_url}/chat"
        try:
            response = self.session.post(endpoint, json={"message": message})
            return response.json()["response"]
        except Exception as e:
            print(f"Error getting chat response: {e}")
            # Return dummy response as fallback
            return f"I received your message: '{message}'. This is a placeholder response."