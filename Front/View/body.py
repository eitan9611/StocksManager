from dialogs import *
from cards import *
import sys
import os
from main import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Model.ExampleModel import ApiClient
from Present.TradePresent import *
from Present.UserPresent import *



class BodyContentFrame(ScrollableFrame):
    email = ""
    def __init__(self,email):
        super().__init__()
        self.email = email

        # Initialize API client
        self.api_client = ApiClient()

        main_lay = self.frameLayout()
        main_lay.setSpacing(21)

        top_lay = QHBoxLayout()
        main_lay.addLayout(top_lay)

        """
        time_frame_dropdown = DropdownButton(
            "Timeframe:",
            "This Month",
            dialog_class=TimeFrameDialog,
        )
        top_lay.addWidget(time_frame_dropdown)

        people_dropdown = DropdownButton(
            "People:",
            "All",
            dialog_class=PeopleFrameDialog,
        )
        top_lay.addWidget(people_dropdown)
        """

        """
        topic_dropdown = DropdownButton(
            "Topic:",
            "All",
        )
        top_lay.addWidget(topic_dropdown)
        """

        # Add simplified account balance card at the top
        balance_frame = self.create_balance_account(email)
        main_lay.addWidget(balance_frame)

        content_lay = QGridLayout()
        content_lay.setSpacing(24)
        main_lay.addLayout(content_lay)

        small_cards_lay = QVBoxLayout()
        small_cards_lay.setSpacing(17)
        content_lay.addLayout(small_cards_lay, 0, 0)

        # Fetch dashboard stats from API
        # TODO: Replace with actual API call
        self.dashboard_stats = self.api_client.get_dashboard_stats()

        # Define card details using data from API
        small_card_details = (
            dict(
                title="Active Users",
                value=f"<a style='font-size: 26px; font-weight: bold;'>{self.dashboard_stats['active_users']['count']}</a><a style='font-size: 19px; font-weight: 700; color: rgba(0, 0, 0, .5);'>/{self.dashboard_stats['active_users']['total']}</a>",
                default_value_style=False,
            ),
            dict(
                title="Questions Answered",
                value=f"{self.dashboard_stats['questions_answered']:,}",
            ),
            dict(
                title="Av. Session Length",
                value=self.dashboard_stats['avg_session_length'],
            ),
            dict(
                title="Starting Knowledge",
                value=f"{self.dashboard_stats['starting_knowledge']}%",
                have_graph=True,
            ),
            dict(
                title="Current Knowledge",
                value=f"{self.dashboard_stats['current_knowledge']}%",
                have_graph=True,
            ),
            dict(
                title="Knowledge Gain",
                value=f"+{self.dashboard_stats['knowledge_gain']}%",
                have_graph=True,
            ),
        )

        row, col = 0, 0
        for index, small_card_detail in enumerate(small_card_details):
            if index and not index % 3:
                row += 1
                col = 0

            if not col:
                _small_cards_lay = QHBoxLayout()
                small_cards_lay.addLayout(_small_cards_lay)

            small_card = SmallCard(**small_card_detail)
            _small_cards_lay.addWidget(small_card)

            col += 1

        # Create purchase history table and place it in the right side where ActivityCard was
        self.purchase_table = self.create_purchase_table()

        # Create a frame to hold the table with a title
        table_frame = QFrame()
        table_layout = QVBoxLayout(table_frame)

        # Add title to the table frame
        table_title = QLabel("Purchase History")
        table_title.setObjectName("section_header")
        table_layout.addWidget(table_title)

        # Add the table to the frame
        table_layout.addWidget(self.purchase_table)

        # Add the table frame to the content layout where ActivityCard was
        content_lay.addWidget(table_frame, 0, 1)

        # Add profit/loss graph section with header
        graph_section = QLabel("Profit/Loss Analysis")
        graph_section.setObjectName("section_header")
        main_lay.addWidget(graph_section)

        # Create profit/loss graph
        self.profit_loss_graph = self.create_profit_loss_graph()
        main_lay.addWidget(self.profit_loss_graph)

        main_lay.addStretch()

    def create_user_profile(self):
        """Create a user profile section displaying the email"""
        profile_frame = QFrame()
        profile_frame.setObjectName("user_profile_frame")

        # Main layout
        layout = QHBoxLayout(profile_frame)

        # User avatar (circle with initials or icon)
        avatar = QFrame()
        avatar.setFixedSize(40, 40)
        avatar.setObjectName("user_avatar")
        avatar_layout = QVBoxLayout(avatar)
        avatar_layout.setContentsMargins(0, 0, 0, 0)

        # Get initials from email
        initials = ''.join([c[0].upper() for c in user_email.split('@')[0].split('.')])[:2]
        initials_label = QLabel(initials)
        initials_label.setObjectName("user_initials")
        initials_label.setAlignment(Qt.AlignCenter)
        avatar_layout.addWidget(initials_label)

        layout.addWidget(avatar)

        # User email and welcome message
        user_info = QVBoxLayout()
        welcome = QLabel(userStatus(self.email))
        welcome.setObjectName("welcome_label")

        email = QLabel(user_email)
        email.setObjectName("user_email_label")

        user_info.addWidget(welcome)
        user_info.addWidget(email)
        layout.addLayout(user_info)

        # Add settings button
        layout.addStretch()
        settings_btn = QPushButton("Settings")
        settings_btn.setObjectName("user_settings_button")
        layout.addWidget(settings_btn)

        return profile_frame
    def create_balance_account(self,email):
        """Create a simplified account balance display with just the header and amount"""
        # Create a container frame
        balance_frame = QFrame()
        balance_frame.setObjectName("balance_account_frame")
        balance_frame.setStyleSheet("""
            QFrame#balance_account_frame {
                background-color: white;
                border-radius: 15px;
                margin-bottom: 20px;
                padding: 20px;
            }
        """)

        # Main layout
        layout = QVBoxLayout(balance_frame)

        # Add user email display at the top
        email_layout = QHBoxLayout()

        # User icon
        user_icon = QLabel()
        user_icon.setPixmap(QSvgPixmap("./View/svgs/user.svg")) #, width=24, height=24))
        email_layout.addWidget(user_icon)

        # User email label
        email_label = QLabel(userStatus(self.email))
        email_label.setStyleSheet("""
            font-size: 16px;
            font-weight: 500;
            color: #4c4c4c;
            margin-left: 8px;
        """)
        email_layout.addWidget(email_label)

        email_layout.addStretch()
        layout.addLayout(email_layout)

        # Add some space between email and balance
        layout.addSpacing(15)

        # Balance header - using UPPERCASE as requested
        balance_header = QLabel("ACCOUNT BALANCE")
        balance_header.setObjectName("section_header")
        layout.addWidget(balance_header)

        # Current balance amount
        balance = "$" + str(getBalance(self.email))
        balance_amount = QLabel(balance)
        balance_amount.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: #1B59F8;
            margin-top: 5px;
        """)
        layout.addWidget(balance_amount)

        layout.addStretch()

        return balance_frame

    def create_purchase_table(self):
        # Create table for purchase history
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["Date", "Stock", "Quantity", "Price", "Total"])

        sample_data = format_trades_for_view(self.email)
        """sample_data = [
            ["2025-03-01", "AAPL", "10", "$174.25", "$1,742.50", "$1,810.30"],
            ["2025-03-05", "MSFT", "5", "$410.75", "$2,053.75", "$2,115.25"],
            ["2025-03-10", "TSLA", "3", "$178.33", "$534.99", "$510.15"],
            ["2025-03-15", "GOOGL", "2", "$176.44", "$352.88", "$380.26"],
            ["2025-03-20", "AMZN", "7", "$182.41", "$1,276.87", "$1,320.15"],
            ["2025-03-25", "META", "8", "$486.18", "$3,889.44", "$4,125.60"],
            ["2025-03-30", "NVDA", "4", "$905.33", "$3,621.32", "$3,850.44"]
        ]"""

        if sample_data[0][0] == "Error":
            #TODO - replace with message on screen
            print(f"{sample_data[0][1]:}")

        else:
            table.setRowCount(len(sample_data))

            for row, (type_, date, stock, quantity, price, total) in enumerate(sample_data):
                table.setItem(row, 0, QTableWidgetItem(date))
                table.setItem(row, 1, QTableWidgetItem(stock))
                table.setItem(row, 2, QTableWidgetItem(quantity))


                # Highlight current value based on profit/loss
                price_item = QTableWidgetItem(price)
                total_item = QTableWidgetItem(total)

                # Set color based on profit/loss
                if type_ == 1:  # 0 for buy, 1 for sell
                    price_item.setForeground(QColor("green"))
                    total_item.setForeground(QColor("green"))
                else:
                    price_item.setForeground(QColor("red"))
                    total_item.setForeground(QColor("red"))

                table.setItem(row, 3, price_item)
                table.setItem(row, 4, total_item)

            # Set table properties
            table.setAlternatingRowColors(True)
            table.setSortingEnabled(True)
            table.resizeColumnsToContents()
            table.setSelectionBehavior(QAbstractItemView.SelectRows)

            # Set a fixed height to match the space available
            table.setMinimumHeight(300)

        return table

    def create_profit_loss_graph(self):
        # Create a frame to hold the graph
        frame = QFrame()
        layout = QVBoxLayout(frame)

        # Add timeframe selection
        timeframe_layout = QHBoxLayout()
        timeframe_label = QLabel("Timeframe:")

        day_button = QPushButton("Day")
        day_button.setCheckable(True)
        day_button.setChecked(True)

        week_button = QPushButton("Week")
        week_button.setCheckable(True)

        month_button = QPushButton("Month")
        month_button.setCheckable(True)

        year_button = QPushButton("Year")
        year_button.setCheckable(True)

        # Add buttons to button group for exclusive selection
        timeframe_group = QButtonGroup(frame)
        timeframe_group.addButton(day_button)
        timeframe_group.addButton(week_button)
        timeframe_group.addButton(month_button)
        timeframe_group.addButton(year_button)

        timeframe_layout.addWidget(timeframe_label)
        timeframe_layout.addWidget(day_button)
        timeframe_layout.addWidget(week_button)
        timeframe_layout.addWidget(month_button)
        timeframe_layout.addWidget(year_button)
        timeframe_layout.addStretch()

        layout.addLayout(timeframe_layout)

        # Add a label to simulate a graph (in a real implementation, this would be replaced with an actual graph widget)
        label = QLabel("Profit/Loss Graph")
        label.setObjectName("graph_placeholder")
        label.setAlignment(Qt.AlignCenter)
        label.setMinimumHeight(300)
        label.setStyleSheet("background-color: #f9f9f9; border: 1px solid #ddd;")

        # In a real implementation, you would replace this with a graph widget like PyQtGraph or Matplotlib
        label.setText(
            "This placeholder represents a profit/loss graph showing the customer's performance over time.\n\n"
            "TODO: Implement actual graphing functionality using PyQtGraph or Matplotlib")

        layout.addWidget(label)

        return frame

    def refresh_data(self):
        """Refresh dashboard data from the API"""
        # TODO: Implement refresh functionality to update cards with new data
        self.dashboard_stats = self.api_client.get_dashboard_stats()
        # Update cards with new data


class Body(QFrame):
    def __init__(self,email):
        super().__init__()

        main_lay = QVBoxLayout(self)

        top_lay = QHBoxLayout()
        main_lay.addLayout(top_lay)

        reports = QLabel("Reports")
        reports.setObjectName("reports")
        top_lay.addWidget(reports)

        top_lay.addStretch()

        download_pixmap = QLabel()
        download_pixmap.setPixmap(
            QSvgPixmap(
                "./View/svgs/download.svg",
                color="#4c4c4c",
            )
        )
        download_pixmap.setObjectName("download_pixmap")
        top_lay.addWidget(download_pixmap)

        download = QLabel("Download")
        download.setObjectName("download")
        top_lay.addWidget(download)

        main_lay.addSpacing(37)

        top_hline = HLine()
        main_lay.addWidget(top_hline)

        main_lay.addSpacing(28)

        body_content_frame = BodyContentFrame(email)
        main_lay.addWidget(body_content_frame, 1)

        main_lay.addStretch()


if __name__ == "__main__":
    import os

    os.system("python main.py")