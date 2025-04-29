from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
                               QHBoxLayout, QLineEdit, QCheckBox, QFrame, QScrollArea)
from PySide6.QtGui import QPixmap, QCursor
from PySide6.QtCore import Qt
import urllib.parse
import webbrowser
import threading
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import sys

# Google OAuth constants
CLIENT_ID = "694671541821-spb05gl88fh798oh4vd1o6nn4ughdm2t.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = "http://localhost:5025/callback"
AUTH_URL = f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=openid email"


class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)

        if "code" in params:
            auth_code = params["code"][0]
            self.server.auth_code = auth_code
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"""
                <html>
                    <head>
                        <title>Authorization Successful</title>
                        <script>
                            window.onload = function() {
                                window.open('', '_self', '');
                                window.close();
                            }
                        </script>
                    </head>
                    <body>
                        <h2>Authorization successful. You can close this window.</h2>
                    </body>
                </html>
            """)
            self.server.auth_code_received = True


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        screen_geometry = QApplication.primaryScreen().geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        window_width = int(screen_width * 0.7)
        window_height = int(screen_height * 0.7)

        self.setWindowTitle("Stock4U - Login")
        self.setGeometry(100, 100, window_width, window_height)

        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Left side (image)
        left_frame = QFrame()
        left_frame.setMinimumWidth(400)
        left_frame.setStyleSheet("background-color: black;")

        self.image_label = QLabel()
        pixmap = QPixmap("./View/svgs/wmremove-transformed.jpeg")
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)
        self.image_label.setAlignment(Qt.AlignCenter)

        left_layout = QVBoxLayout(left_frame)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.addWidget(self.image_label)

        # Right side (form with scroll)
        right_frame = QFrame()
        right_layout = QVBoxLayout(right_frame)
        right_layout.setContentsMargins(0, 0, 0, 0)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        scroll_container = QWidget()
        scroll_layout = QVBoxLayout(scroll_container)
        scroll_layout.setAlignment(Qt.AlignCenter)

        login_frame = QFrame()
        login_frame.setStyleSheet("background-color: white; border-radius: 20px;")
        login_layout = QVBoxLayout(login_frame)
        login_layout.setContentsMargins(60, 60, 60, 60)
        login_layout.setSpacing(20)

        # Title
        title_label = QLabel("USER LOGIN")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #6C63FF;")
        title_label.setAlignment(Qt.AlignCenter)

        # Username input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username or Email")
        self.username_input.setFixedHeight(40)
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: #f0f0f0;
                border: none;
                border-radius: 20px;
                padding-left: 15px;
                font-size: 16px;
            }
        """)

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(40)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: #f0f0f0;
                border: none;
                border-radius: 20px;
                padding-left: 15px;
                font-size: 16px;
            }
        """)

        # Options layout
        options_layout = QHBoxLayout()
        self.remember_checkbox = QCheckBox("Remember me")
        self.remember_checkbox.setStyleSheet("font-size: 14px;")
        forgot_password_label = QLabel('<a href="#">Forgot password?</a>')
        forgot_password_label.setStyleSheet("font-size: 14px; color: #6C63FF;")
        forgot_password_label.setOpenExternalLinks(True)
        forgot_password_label.setCursor(QCursor(Qt.PointingHandCursor))
        options_layout.addWidget(self.remember_checkbox)
        options_layout.addStretch()
        options_layout.addWidget(forgot_password_label)

        # Login button
        self.login_button = QPushButton("LOGIN")
        self.login_button.setFixedHeight(45)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6C63FF, stop:1 #A084E8);
                color: white;
                border: none;
                border-radius: 22px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5A54D1;
            }
        """)
        self.login_button.clicked.connect(self.open_main_window)

        # Google login button
        self.google_login_button = QPushButton("LOGIN WITH GOOGLE")
        self.google_login_button.setFixedHeight(45)
        self.google_login_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #6C63FF;
                border: 2px solid #6C63FF;
                border-radius: 22px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f2f2f2;
            }
        """)
        self.google_login_button.clicked.connect(self.open_google_login)

        # Assemble login layout
        login_layout.addWidget(title_label)
        login_layout.addWidget(self.username_input)
        login_layout.addWidget(self.password_input)
        login_layout.addLayout(options_layout)
        login_layout.addWidget(self.login_button)
        login_layout.addWidget(self.google_login_button)

        scroll_layout.addWidget(login_frame)
        scroll_area.setWidget(scroll_container)
        right_layout.addWidget(scroll_area)

        # Add frames to main layout
        main_layout.addWidget(left_frame, 3)
        main_layout.addWidget(right_frame, 2)


    def resizeEvent(self, event):
        super().resizeEvent(event)
        if not self.image_label.pixmap().isNull():
            pixmap = QPixmap("./View/svgs/wmremove-transformed.jpeg")
            height = self.image_label.height()
            scaled_pixmap = pixmap.scaledToHeight(height, Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)

    def open_main_window(self):
        user_email = "eitan@"
        os.system(f"python ./View/main.py {user_email}")
        self.close()

    def open_google_login(self):
        self.start_local_server()
        webbrowser.open(AUTH_URL)
        while not self.server.auth_code_received:
            self.server.handle_request()
        auth_code = self.server.auth_code
        self.exchange_code_for_token(auth_code)

    def start_local_server(self):
        self.server = HTTPServer(("localhost", 5025), OAuthHandler)
        self.server.auth_code_received = False
        server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        server_thread.start()

    def exchange_code_for_token(self, auth_code):
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": auth_code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        response = requests.post(token_url, data=data)
        if response.status_code == 200:
            tokens = response.json()
            id_token = tokens.get("id_token")
            self.get_user_info(id_token)
        else:
            print("Login failed! Try again.")

    def get_user_info(self, id_token):
        user_info_url = "https://oauth2.googleapis.com/tokeninfo"
        response = requests.get(user_info_url, params={"id_token": id_token})
        if response.status_code == 200:
            user_info = response.json()
            user_email = user_info.get("email", "Unknown email")
            os.system(f"python ./View/main.py {user_email}")
            self.close()
        else:
            print("Failed to retrieve user info")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
