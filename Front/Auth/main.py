import sys
import webbrowser
import requests
import urllib.parse
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import os

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

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login with Google")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.label = QLabel("Click below to login with Google")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.login_button = QPushButton("Login with Google")
        self.login_button.clicked.connect(self.open_google_login)
        layout.addWidget(self.login_button)

        self.user_info_label = QLabel("")
        layout.addWidget(self.user_info_label)

        self.setLayout(layout)

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
