from commons import *
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Model.ExampleModel import ApiClient
import requests


class MessageBubble(QFrame):
    # def __init__(self, message, is_user=True):
    #     super().__init__()

    #     self.is_user = is_user

    #     # Set styling based on whether this is a user or bot message
    #     if is_user:
    #         self.setObjectName("user_bubble")
    #     else:
    #         self.setObjectName("bot_bubble")

    #     # Create layout
    #     layout = QVBoxLayout(self)

    #     # Add message text
    #     self.message_label = QLabel(message)
    #     self.message_label.setWordWrap(True)
    #     self.message_label.setObjectName("message_text")
    #     layout.addWidget(self.message_label)

    #     # Add timestamp
    #     current_time = QTime.currentTime().toString("hh:mm")
    #     time_label = QLabel(current_time)
    #     time_label.setObjectName("time_label")

    #     # Align timestamp to right for user messages, left for bot messages
    #     time_layout = QHBoxLayout()
    #     if is_user:
    #         time_layout.addStretch()
    #         time_layout.addWidget(time_label)
    #     else:
    #         time_layout.addWidget(time_label)
    #         time_layout.addStretch()

    #     layout.addLayout(time_layout)

    def __init__(self, message, is_user=True):
        super().__init__()

        self.is_user = is_user

        # Set styling based on whether this is a user or bot message
        if is_user:
            self.setObjectName("user_bubble")
        else:
            self.setObjectName("bot_bubble")

        # Main layout for the bubble
        main_layout = QHBoxLayout(self)
        main_layout.setAlignment(Qt.AlignLeft if not is_user else Qt.AlignRight)

        # Icon
        icon_label = QLabel()
        if is_user:
            icon_label.setPixmap(QPixmap("View/svgs/user_icon.svg").scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            icon_label.setPixmap(QPixmap("View/svgs/robot_icon.svg").scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # Message and time layout
        content_layout = QVBoxLayout()
        
        # Message and time layout
        content_layout = QVBoxLayout()

        # Message text
        self.message_label = QLabel(message)
        self.message_label.setWordWrap(True)
        self.message_label.setObjectName("message_text")
        content_layout.addWidget(self.message_label)

        # Timestamp
        current_time = QTime.currentTime().toString("hh:mm")
        time_label = QLabel(current_time)
        time_label.setObjectName("time_label")

        time_layout = QHBoxLayout()
        if is_user:
            time_layout.addStretch()
            time_layout.addWidget(time_label)
        else:
            time_layout.addWidget(time_label)
            time_layout.addStretch()

        content_layout.addLayout(time_layout)

        # עכשיו עוטפים את ה-layout בתוך QWidget
        content_widget = QWidget()
        content_widget.setLayout(content_layout)

        # ואז מוסיפים את ה-widget למיין לייאאוט
        if is_user:
            main_layout.addWidget(content_widget)
            main_layout.addWidget(icon_label)
        else:
            main_layout.addWidget(icon_label)
            main_layout.addWidget(content_widget)



class ChatBotPage(QFrame):
    def __init__(self):
        super().__init__()

        # Initialize API client
        self.api_client = ApiClient()

        # Create main layout
        main_layout = QVBoxLayout(self)

        # Create chat history area (scrollable)
        self.chat_history = QScrollArea()
        self.chat_history.setWidgetResizable(True)
        self.chat_history.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.chat_history.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Create a widget to hold all the chat bubbles
        self.chat_container = QWidget()
        self.chat_container.setObjectName("chat_container")
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setAlignment(Qt.AlignTop)
        self.chat_layout.setSpacing(10)

        # Add some padding at the bottom to make sure messages don't crowd the edge
        self.chat_layout.addStretch()

        self.chat_history.setWidget(self.chat_container)
        main_layout.addWidget(self.chat_history, 1)

        # Create input area at the bottom
        input_layout = QHBoxLayout()

        # Text input field
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type a message...")

        # Adding styles to the message input
        self.message_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #ccc;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                background-color: #f9f9f9;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
        """)

        self.message_input.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.message_input, 1)

        # Send button
        self.send_button = QPushButton()
        self.send_button.setIcon(QIcon("View/svgs/arrow_full_up1.svg"))
        self.send_button.setIconSize(QSize(24, 24))
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)

        main_layout.addLayout(input_layout)

        # Get initial welcome message from API
        initial_message = "Hello! How can I help you today?"
        self.add_message(initial_message, False)

    def add_message(self, message, is_user=True):
        bubble = MessageBubble(message, is_user)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, bubble)
        self.chat_history.verticalScrollBar().setValue(self.chat_history.verticalScrollBar().maximum())

    def send_message(self):
        message = self.message_input.text().strip()
        if message:
            self.add_message(message, True)
            self.message_input.clear()
            self.message_input.setEnabled(False)
            self.send_button.setEnabled(False)
            print(f"User message: {message}")
            QTimer.singleShot(300, lambda: self.get_bot_response(message))

    def get_bot_response(self, message):
        try:
            response = requests.post("http://localhost:5000/ask", json={"question": message})

            if response.status_code != 200:
                self.add_message(f"Error: Received status code {response.status_code}", False)
                return

            response_text = response.json().get("response", "Sorry, I couldn't understand that.")
            self.add_message(response_text, False)
        except requests.exceptions.ConnectionError:
            self.add_message("Error: Could not connect to the API. Is the server running?", False)
        except ValueError as e:  # This catches JSON parsing errors
            print(f"Error parsing JSON: {e}")
            print(f"Response content: {response.text}")
            self.add_message("Error: Invalid response from server", False)
        except Exception as e:
            print(f"Error getting response: {e}")
            self.add_message(f"Sorry, I couldn't process your request: {str(e)}", False)
        finally:
            self.message_input.setEnabled(True)
            self.send_button.setEnabled(True)
