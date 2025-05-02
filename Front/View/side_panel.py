from buttons import *
from cards import *
class SidePanel(Card):
    # Create a signal for navigation
    navigation_requested = Signal(str)
    def __init__(self):
        super().__init__()
        
        self.setStyleSheet("""
            background-color: #2f2f2f;
            /* גורם למרחב להיות רק מצד ימין של הפאנל */
            padding-right: 50px;
        """)
        
        # נשתמש בגריד במקום שורות כדי לשלוט בדיוק בהצבה
        grid_layout = QGridLayout(self)
        grid_layout.setContentsMargins(0, 80, 50, 10)  # שוליים שמאליים רחבים יותר
        grid_layout.setHorizontalSpacing(10)
        grid_layout.setVerticalSpacing(10)
        
        # לוגו למעלה
        logo_pixmap = QSvgPixmap("./View/svgs/invert-Photoroom.svg")
        scaled_pixmap = logo_pixmap.scaled(300, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        logo_label = QLabel()
        logo_label.setObjectName("logo_label")
        logo_label.setPixmap(scaled_pixmap)

        logo_label.setStyleSheet("""
        margin-top: -130px;
        margin-left: -30px;
    """)
        logo_label.setFixedSize(scaled_pixmap.size())

        # הכנסת הלוגו ומרכוז שלו
        #grid_layout.addWidget(tesla_label, 0, 0, 1, 2, Qt.AlignmentFlag.AlignTop)
        grid_layout.addWidget(logo_label, 0, 0, 1, 2, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)


        # הכפתורים ממש בצד שמאל
        reports_button = SidePanelButton(
            "./View/svgs/reports.svg",
            "My Stocks",
            toggled=True,
        )
        # מקם בעמודה 0 (הכי שמאלית)
        grid_layout.addWidget(reports_button, 1, 0, Qt.AlignmentFlag.AlignLeft)
        # הוסף מרווח ריק בעמודה 1 כדי לדחוף את הכפתור שמאלה
        grid_layout.setColumnStretch(1, 1)
        reports_button.clicked.connect(lambda: self.navigation_requested.emit("My Stocks"))
        
        # כפתור שני
        activities_button = SidePanelButton(
            "./View/svgs/activities.svg",
            "Stock Info",
        )
        grid_layout.addWidget(activities_button, 2, 0, Qt.AlignmentFlag.AlignLeft)
        activities_button.clicked.connect(lambda: self.navigation_requested.emit("Stocks Info"))
        
        # הוספת מרווח אנכי
        spacer = QWidget()
        spacer.setFixedHeight(88)  # 60 + 28 מהקוד המקורי
        grid_layout.addWidget(spacer, 3, 0)
        
        # כפתור שלישי
        get_started_button = SidePanelButton(
            "./View/svgs/get_started.svg",
            "ChatBot",
        )
        grid_layout.addWidget(get_started_button, 4, 0, Qt.AlignmentFlag.AlignLeft)
        get_started_button.clicked.connect(lambda: self.navigation_requested.emit("ChatBot"))
        
        # הכפתורים עצמם אולי צריכים סגנון נוסף
        for button in [reports_button, activities_button, get_started_button]:
            button.setStyleSheet(button.styleSheet() + """
                /* הזזה שמאלה בתוך הכפתור עצמו */
                text-align: left;
                padding-left: 0px;
                margin-left: 0px;
            """)
        
        # מרווח בתחתית
        grid_layout.setRowStretch(5, 1)
        
if __name__ == "__main__":
    import os
    os.system("python main.py")