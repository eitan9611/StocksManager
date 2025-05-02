from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
                               QHBoxLayout, QLineEdit, QCheckBox, QFrame, QScrollArea)
from PySide6.QtGui import QPixmap, QCursor
from PySide6.QtCore import Qt, QTimer
import urllib.parse
import webbrowser
import threading
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import sys
import subprocess

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
            
    def log_message(self, format, *args):
        # Suppress log messages to keep console clean
        pass


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
        
        # Set default style to avoid QPainter issues
        self.setStyleSheet("background-color: white;")
        
        # Initialize image path and validate it
        self.image_path = "./View/svgs/wmremove-transformed.jpeg"
        self.image_found = os.path.isfile(self.image_path)
        
        # For debugging
        if not self.image_found:
            print(f"Warning: Image file not found at {self.image_path}")
            print(f"Current working directory: {os.getcwd()}")
            
        self.init_ui()
        
        # Load image after UI is created
        QTimer.singleShot(100, self.load_image)

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Left side (image or fallback)
        left_frame = QFrame()
        left_frame.setMinimumWidth(400)
        
        # Set fallback color in case image isn't found
        left_frame.setStyleSheet("background-color: black;")

        left_layout = QVBoxLayout(left_frame)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)
        
        self.image_label = QLabel()
        
        # Initialize with text that will be replaced by image if loading succeeds
        self.image_label.setText("Stock4U")
        self.image_label.setStyleSheet("font-size: 36px; color: white; padding: 50px;")
        self.image_label.setAlignment(Qt.AlignCenter)
        
        left_layout.addWidget(self.image_label)

        # Right side (form with scroll)
        right_frame = QFrame()
        right_layout = QVBoxLayout(right_frame)
        right_layout.setContentsMargins(0, 0, 0, 0)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: white; }")

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
        
    def load_image(self):
        """Load the image after UI initialization to avoid QPainter errors"""
        try:
            if not self.image_found:
                print("Image not found, skipping load")
                return
                
            pixmap = QPixmap(self.image_path)
            if not pixmap.isNull():
                self.image_label.setPixmap(pixmap.scaled(
                    self.image_label.width(), 
                    self.image_label.height(),
                    Qt.KeepAspectRatioByExpanding,
                    Qt.SmoothTransformation
                ))
                self.image_label.setScaledContents(True)
                # Clear the text and styling since we have an image
                self.image_label.setText("")
                self.image_label.setStyleSheet("")
            else:
                print(f"Failed to load image: pixmap is null")
        except Exception as e:
            print(f"Error loading image: {e}")
            
    def resizeEvent(self, event):
        """Handle resize events and update image scaling"""
        super().resizeEvent(event)
        # If we have an image and UI is fully initialized, rescale it
        if hasattr(self, 'image_label') and hasattr(self.image_label, 'pixmap') and self.image_label.pixmap() and not self.image_label.pixmap().isNull():
            try:
                current_pixmap = self.image_label.pixmap()
                scaled_pixmap = current_pixmap.scaled(
                    self.image_label.width(),
                    self.image_label.height(),
                    Qt.KeepAspectRatioByExpanding,
                    Qt.SmoothTransformation
                )
                self.image_label.setPixmap(scaled_pixmap)
            except Exception as e:
                print(f"Error in resizeEvent: {e}")

    def open_main_window(self):
        user_email = self.username_input.text() or "eitan@"
        try:
            print("Opening main window...")
            # Try multiple possible paths for main.py
            possible_paths = [
                "./View/main.py",
                "View/main.py",
                "../View/main.py",
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "View", "main.py"),
                os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "View", "main.py")
            ]
            
            main_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    main_path = path
                    print(f"Found main.py at: {path}")
                    break
            
            if not main_path:
                print("Warning: Could not find main.py, using default path")
                main_path = "./View/main.py"
                
            # Use subprocess with Popen to open main.py in a non-blocking way
            print(f"Starting subprocess with: {sys.executable} {main_path} {user_email}")
            subprocess.Popen([sys.executable, main_path, user_email])
            
            """print("Scheduling window close...")
            # Schedule window close after a short delay to ensure subprocess starts
            QTimer.singleShot(500, lambda: self.close())
            
            # Make sure we exit if window doesn't close properly
            QTimer.singleShot(1000, lambda: QApplication.quit())"""
            
        except Exception as e:
            print(f"Error opening main window: {e}")

    def open_google_login(self): 
        try:
            print("Starting OAuth login process...")
            self.server = HTTPServer(("localhost", 5025), OAuthHandler)
            self.server.auth_code_received = False
            self.server.auth_code = None
            
            # Start server in a separate thread
            server_thread = threading.Thread(target=self.run_server, daemon=True)
            server_thread.start()
            
            # Open browser for authentication
            webbrowser.open(AUTH_URL)
        except Exception as e:
            print(f"Error in Google login: {e}")

    def run_server(self):
        try:
            print("OAuth server started and waiting for auth code...")
            while not hasattr(self.server, 'auth_code_received') or not self.server.auth_code_received:
                self.server.handle_request()
                
            # Once auth code received, exchange for token
            auth_code = self.server.auth_code
            self.server.server_close()
            print("Auth code received, exchanging for token...")
            
            if auth_code:
                self.exchange_code_for_token(auth_code)
        except Exception as e:
            print(f"Server error: {e}")

    def exchange_code_for_token(self, auth_code):
        try:
            token_url = "https://oauth2.googleapis.com/token"
            data = {
                "code": auth_code,
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uri": REDIRECT_URI,
                "grant_type": "authorization_code",
            }
            print("Exchanging auth code for token...")
            response = requests.post(token_url, data=data)
            if response.status_code == 200:
                tokens = response.json()
                id_token = tokens.get("id_token")
                print("Token exchange successful")
                self.get_user_info(id_token)
            else:
                print(f"Login failed! Status code: {response.status_code}")
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"Token exchange error: {e}")

    def get_user_info(self, id_token):
        try:
            user_info_url = "https://oauth2.googleapis.com/tokeninfo"
            print("Getting user info from token...")
            response = requests.get(user_info_url, params={"id_token": id_token})
            if response.status_code == 200:
                user_info = response.json()
                user_email = user_info.get("email", "Unknown email")
                print(f"User authenticated: {user_email}")
                
                # Try multiple possible paths for main.py
                possible_paths = [
                    "./View/main.py",
                    "View/main.py",
                    "../View/main.py",
                    os.path.join(os.path.dirname(os.path.abspath(__file__)), "View", "main.py"),
                    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "View", "main.py")
                ]
                
                main_path = None
                for path in possible_paths:
                    if os.path.exists(path):
                        main_path = path
                        print(f"Found main.py at: {path}")
                        break
                
                if not main_path:
                    print("Warning: Could not find main.py, using default path")
                    main_path = "./View/main.py"
                
                # Launch main window with the user's email
                print(f"Starting main window: {sys.executable} {main_path} {user_email}")
                subprocess.Popen([sys.executable, main_path, user_email])
                
                # Since we're in a different thread, use QTimer to safely close the window
                print("Scheduling window close...")
                QTimer.singleShot(0, self.close)
                QTimer.singleShot(500, QApplication.quit)
            else:
                print(f"Failed to retrieve user info. Status code: {response.status_code}")
        except Exception as e:
            print(f"User info error: {e}")


if __name__ == "__main__":
    
    # Create application
    app = QApplication(sys.argv)
    
    # Create and show login window
    window = LoginWindow()
    window.show()
    
    # Start event loop and exit properly
    exit_code = app.exec()
    print("Application exiting with code:", exit_code)
    sys.exit(exit_code)