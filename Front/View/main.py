import sys
from PyQt5.QtCore import Qt  # Import Qt
from main_page import *

class Application(QApplication):
    def __init__(self, email) -> None:
        super().__init__([])

        self.win = AnalyticsDashoard(email)  # Pass the email if needed
        self.win.setWindowFlags(Qt.WindowStaysOnTopHint)  # Keep window on top
        self.win.show()

        self.setStyleSheet(STYLE_QSS)

# Retrieve email from command-line arguments
if __name__ == "__main__":
    user_email = sys.argv[1] if len(sys.argv) > 1 else None  # Get argument or set to None
    app = Application(user_email)
    print(f"User email: {user_email}")
    app.exec()
