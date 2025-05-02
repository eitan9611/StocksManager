from side_panel import *
from body import Body
from chatbot_page import ChatBotPage
from stock_info_page import StockInfoPage


class AnalyticsDashoard(QFrame):
    def __init__(self,email):
        super().__init__()

        self.setWindowTitle("Analytics Dashboard")
        self.setFixedSize(CODING_WIDTH, CODING_HEIGHT)

        # setup widgets
        main_lay = QHBoxLayout(self)
        main_lay.setContentsMargins(0, 0, 0, 0)

        self.side_panel = SidePanel()
        main_lay.addWidget(self.side_panel)

        # Create a stacked widget to hold different pages
        self.page_stack = QStackedWidget()
        main_lay.addWidget(self.page_stack)

        # Create and add pages to the stack
        self.body = Body(email)
        self.page_stack.addWidget(self.body)

        self.stock_info_page = StockInfoPage(email)
        self.stock_info_page.stock_bought.connect(self.body.refresh_table)

        self.page_stack.addWidget(self.stock_info_page)

        self.chatbot_page = ChatBotPage()
        self.page_stack.addWidget(self.chatbot_page)

        # Connect navigation signals from side panel
        self.side_panel.navigation_requested.connect(self.change_page)

        # Create a map of page names to their index in the stack
        self.page_map = {
            "My Stocks": 0,  # Body is at index 0
            "Stocks Info": 1,  # Stock info page at index 1
            "ChatBot": 2  # Chat bot page at index 2
        }

    def change_page(self, page_name):
        """Change the current page based on the button clicked in the side panel"""
        print(f"Changing to page: {page_name}")

        if page_name in self.page_map:
            self.page_stack.setCurrentIndex(self.page_map[page_name])
            self.setWindowTitle(f"Analytics Dashboard - {page_name}")
        else:
            # For pages not yet implemented
            print(f"Page '{page_name}' not implemented yet")

    def showEvent(self, event: QShowEvent) -> None:
        return super().showEvent(event)