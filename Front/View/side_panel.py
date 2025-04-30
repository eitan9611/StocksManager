from buttons import *
from cards import *


class SidePanel(Card):
    # Create a signal for navigation
    navigation_requested = Signal(str)

    def __init__(self):
        super().__init__()
        
        self.setStyleSheet("background-color: #303030;")

        main_lay = QVBoxLayout(self)

        tesla_pixmap = QSvgPixmap("./View/svgs/logo.svg")
        # הוספת שורת הגדלה לגודל הרצוי (למשל 150x150 פיקסלים)
        scaled_pixmap = tesla_pixmap.scaled(200,200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

        tesla_label = QLabel()
        tesla_label.setObjectName("tesla_label")
        tesla_label.setPixmap(scaled_pixmap)  # שים את התמונה המוגדלת בלייבל

        main_lay.addStretch(1)
        main_lay.addWidget(tesla_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        main_lay.addStretch(2)


        reports_button = SidePanelButton(
            "./View/svgs/reports.svg",
            "My Stocksss",
            toggled=True,
        )
        reports_button.clicked.connect(lambda: self.navigation_requested.emit("My Stocks"))
        main_lay.addWidget(reports_button)
        """
        library_button = SidePanelButton(
            "./svgs/library.svg",
            "Buy And Sell",
        )
        library_button.clicked.connect(lambda: self.navigation_requested.emit("Buy And Sell"))
        main_lay.addWidget(library_button)
        """
        """
        people_button = SidePanelButton(
            "./svgs/people.svg",
            "My Stocks",
        )
        people_button.clicked.connect(lambda: self.navigation_requested.emit("My Stocks"))
        main_lay.addWidget(people_button)
        """
        activities_button = SidePanelButton(
            "./View/svgs/activities.svg",
            "Stock Info",
            
        )
        activities_button.clicked.connect(lambda: self.navigation_requested.emit("Stocks Info"))
        main_lay.addWidget(activities_button)

        main_lay.addSpacing(60)
        """
        supported = QLabel("Supported")
        supported.setObjectName("supported")
        main_lay.addWidget(supported)
        """

        main_lay.addSpacing(28)

        get_started_button = SidePanelButton(
            "./View/svgs/get_started.svg",
            "ChatBot",
        )
        get_started_button.clicked.connect(lambda: self.navigation_requested.emit("ChatBot"))
        main_lay.addWidget(get_started_button)
        """
        settings_button = SidePanelButton(
            "./svgs/settings.svg",
            "settings",
        )
        settings_button.clicked.connect(lambda: self.navigation_requested.emit("Settings"))
        main_lay.addWidget(settings_button)
        """

        main_lay.addStretch()


if __name__ == "__main__":
    import os

    os.system("python main.py")