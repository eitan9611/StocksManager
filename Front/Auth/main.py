import sys
import webbrowser
import requests
import urllib.parse
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import os   
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PySide6.QtGui import QPixmap
# from PySide6.QtSvg import QGraphicsSvgItem
from PySide6.QtGui import QPainter

from PySide6.QtWidgets import QGraphicsScene, QGraphicsView
from PySide6.QtSvgWidgets import QGraphicsSvgItem


# Google OAuth settings
CLIENT_ID = "694671541821-spb05gl88fh798oh4vd1o6nn4ughdm2t.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = "http://localhost:5025/callback"
AUTH_URL = f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=openid email"

class OAuthHandler(BaseHTTPRequestHandler):
    """Handles the OAuth callback request"""

    def do_GET(self):
        """Extract authorization code from the request"""
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)

        if "code" in params:
            auth_code = params["code"][0]
            self.server.auth_code = auth_code  # Store it in the server instance

            # Send response to the user
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
                            setTimeout(function() {
                                alert('Authorization successful. You can close this window.');
                            }, 1000);
                        </script>
                    </head>
                    <body>
                        <h2>Authorization successful. You can close this window.</h2>
                    </body>
                </html>
            """)
            self.server.auth_code_received = True




### worked!
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Stock4U - Login")
        self.setGeometry(100, 100, 800, 400)  # Adjusted window size for better layout

        # Create the main layout (two columns)
        main_layout = QHBoxLayout()

       # Left part - SVG image using QGraphicsSvgItem 
        scene = QGraphicsScene()
        pixmap = QPixmap("./View/svgs/wmremove-transformed.jpeg")

        # 🔥 להקטין את הפיקסמאפ לפני שמציגים
        scaled_pixmap = pixmap.scaled(800, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        label = QLabel()
        label.setPixmap(scaled_pixmap)

        main_layout.addWidget(label)


        # # view.setRenderHint(view.RenderHints.Antialiasing)  # Optional: Better rendering quality
        # view.setRenderHint(QPainter.Antialiasing)
        # # view.setRenderHint(view.RenderHints.SmoothPixmapTransform)
        # view.setRenderHint(QPainter.SmoothPixmapTransform)

        # view.setSceneRect(scene.itemsBoundingRect())  # Important: set the scene rect properly
        # view.fitInView(scene.itemsBoundingRect(), Qt.KeepAspectRatio)  # Make the SVG fit nicely
        # view.scale(1, 2)  # אם אתה רוצה לראות ממש גדול

        # view.setMinimumSize(400, 400)  # Size of the widget (can be adjusted)

        # main_layout.addWidget(view, 1)


        # Right part - Website title and button
        right_layout = QVBoxLayout()

        self.title_label = QLabel("Welcome to Stock4U")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")

        self.login_button = QPushButton("Login with Google")
        self.login_button.setFixedSize(200, 40)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.login_button.clicked.connect(self.open_google_login)

        self.user_info_label = QLabel("")
        self.user_info_label.setAlignment(Qt.AlignCenter)

        # Adding spacers for layout
        right_layout.addStretch()  # Add space before the title
        right_layout.addWidget(self.title_label)
        right_layout.addSpacing(20)  # Add space between title and button
        right_layout.addWidget(self.login_button, alignment=Qt.AlignCenter)
        right_layout.addSpacing(20)  # Add space between button and user info label
        right_layout.addWidget(self.user_info_label)
        right_layout.addStretch()  # Add space after user info label

        # Add the right part layout
        main_layout.addLayout(right_layout, 1)  # Add the right part with proportional sizing (1)

        self.setLayout(main_layout)

    def open_google_login(self):
        """Open Google OAuth login in a browser and start local server"""
        self.start_local_server()

        webbrowser.open(AUTH_URL)

        # Wait until the auth code is received
        while not self.server.auth_code_received:
            self.server.handle_request()

        auth_code = self.server.auth_code
        self.exchange_code_for_token(auth_code)

    def start_local_server(self):
        """Start a local HTTP server to capture the OAuth callback"""
        self.server = HTTPServer(("localhost", 5025), OAuthHandler)
        self.server.auth_code_received = False

        # Run the server in a separate thread
        server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        server_thread.start()

    def exchange_code_for_token(self, auth_code):
        """Exchange authorization code for an access token and ID token"""
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
            self.label.setText("Login failed! Try again.")

    def get_user_info(self, id_token):
        """Extract user info from ID token"""
        user_info_url = "https://oauth2.googleapis.com/tokeninfo"
        response = requests.get(user_info_url, params={"id_token": id_token})

        if response.status_code == 200:
            user_info = response.json()
            user_email = user_info.get("email", "Unknown email")
            os.system(f"python ./View/main.py {user_email}")
            #close the login window
            self.close()
            #user_email = user_info.get("email", "Unknown email")
            #self.user_info_label.setText(f"Logged in as: {user_email}")
        else:
            self.label.setText("Failed to retrieve user info")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
