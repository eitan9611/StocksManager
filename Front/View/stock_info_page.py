from View.commons import *
from Model.ExampleModel import ApiClient

from Present.TradePresent import *
from Present.StockPresent import *



class StockInfoPage(QFrame):
    email = ""
    def __init__(self, email):
        super().__init__()
        self.email = email

        # Initialize API client
        self.api_client = ApiClient()

        # Create main layout
        main_layout = QVBoxLayout(self)

        # Create header
        header = QLabel("Stock Information")
        header.setObjectName("header")
        main_layout.addWidget(header)

        # Create search area
        search_layout = QHBoxLayout()

        # Stock symbol input
        self.stock_input = QLineEdit()
        self.stock_input.setPlaceholderText("Enter stock symbol (e.g., AAPL, TSLA)")
        self.stock_input.returnPressed.connect(self.search_stock)
        search_layout.addWidget(self.stock_input, 1)

        # Search button
        self.search_button = QPushButton("Search")
        self.search_button.setObjectName("action_button")
        self.search_button.setMinimumHeight(40)
        self.search_button.clicked.connect(self.search_stock)
        search_layout.addWidget(self.search_button)

        # Buy Stock button
        buy_stock_button = QPushButton("Buy Stock")
        buy_stock_button.setObjectName("action_button")
        buy_stock_button.setMinimumHeight(40)
        buy_stock_button.clicked.connect(self.on_buy_stock)
        search_layout.addWidget(buy_stock_button)

        # Sell Stock button
        sell_stock_button = QPushButton("Sell Stock")
        sell_stock_button.setObjectName("action_button")
        sell_stock_button.setMinimumHeight(40)
        sell_stock_button.clicked.connect(self.on_sell_stock)
        search_layout.addWidget(sell_stock_button)

        main_layout.addLayout(search_layout)

        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(separator)

        # Status label for loading/error states
        self.status_label = QLabel("")
        self.status_label.setObjectName("status_label")
        self.status_label.setVisible(False)
        main_layout.addWidget(self.status_label)

        # Stock info area with image and text in horizontal layout
        stock_top_layout = QHBoxLayout()

        # Stock image area
        self.stock_image_frame = QFrame()
        self.stock_image_frame.setFixedSize(150, 150)
        self.stock_image_frame.setObjectName("stock_image_frame")
        self.stock_image_layout = QVBoxLayout(self.stock_image_frame)

        self.stock_image = QLabel()
        self.stock_image.setAlignment(Qt.AlignCenter)
        self.stock_image.setObjectName("stock_image")
        self.stock_image.setText("No Image")
        self.stock_image_layout.addWidget(self.stock_image)

        stock_top_layout.addWidget(self.stock_image_frame)

        # Basic stock information
        basic_info_layout = QVBoxLayout()
        self.stock_name = QLabel("Stock Name: ")
        self.stock_price = QLabel("Current Price: ")
        self.stock_change = QLabel("Change: ")
        self.market_cap = QLabel("Market Cap: ")
        self.pe_ratio = QLabel("P/E Ratio: ")
        self.dividend_yield = QLabel("Dividend Yield: ")

        for label in [self.stock_name, self.stock_price, self.stock_change,
                      self.market_cap, self.pe_ratio, self.dividend_yield]:
            label.setObjectName("stock_info_label")
            basic_info_layout.addWidget(label)

        stock_top_layout.addLayout(basic_info_layout, 1)
        main_layout.addLayout(stock_top_layout)

        # Create a horizontal layout for description and graph
        description_graph_layout = QHBoxLayout()

        # Company description (left side, smaller)
        description_group = QGroupBox("Company Description")
        description_group.setMaximumWidth(300)  # Limit width to make it smaller
        description_group.setObjectName("company_description")
        description_layout = QVBoxLayout(description_group)

        self.stock_description = QTextEdit()
        self.stock_description.setReadOnly(True)
        self.stock_description.setPlaceholderText("Company description will appear here...")
        self.stock_description.setMaximumHeight(300)  # Match the height of the graph
        description_layout.addWidget(self.stock_description)

        description_graph_layout.addWidget(description_group)

        # Stock price history graph (right side)
        graph_group = QGroupBox("Stock Price History")
        graph_layout = QVBoxLayout(graph_group)

        # Add buttons to select timeframe
        timeframe_layout = QHBoxLayout()

        # Timeframe selection
        timeframe_layout.addWidget(QLabel("Timeframe:"))

        self.timeframe_group = QButtonGroup(self)

        self.day_button = QPushButton("Day")
        self.day_button.setCheckable(True)
        self.day_button.setChecked(True)
        self.day_button.clicked.connect(self.update_graph)
        self.timeframe_group.addButton(self.day_button)
        timeframe_layout.addWidget(self.day_button)

        self.week_button = QPushButton("Week")
        self.week_button.setCheckable(True)
        self.week_button.clicked.connect(self.update_graph)
        self.timeframe_group.addButton(self.week_button)
        timeframe_layout.addWidget(self.week_button)

        self.month_button = QPushButton("Month")
        self.month_button.setCheckable(True)
        self.month_button.clicked.connect(self.update_graph)
        self.timeframe_group.addButton(self.month_button)
        timeframe_layout.addWidget(self.month_button)

        self.year_button = QPushButton("Year")
        self.year_button.setCheckable(True)
        self.year_button.clicked.connect(self.update_graph)
        self.timeframe_group.addButton(self.year_button)
        timeframe_layout.addWidget(self.year_button)

        timeframe_layout.addStretch()
        graph_layout.addLayout(timeframe_layout)

        # Create graph placeholder
        self.graph_frame = QFrame()
        self.graph_frame.setMinimumHeight(300)
        self.graph_frame.setObjectName("graph_frame")
        self.graph_frame.setStyleSheet("background-color: #f9f9f9; border: 1px solid #ddd;")

        self.graph_layout = QVBoxLayout(self.graph_frame)
        self.graph_placeholder = QLabel("Stock price history graph will be displayed here")
        self.graph_placeholder.setAlignment(Qt.AlignCenter)
        self.graph_layout.addWidget(self.graph_placeholder)

        graph_layout.addWidget(self.graph_frame)
        description_graph_layout.addWidget(graph_group, 1)  # Give graph more stretch

        # Add the horizontal layout to the main layout
        main_layout.addLayout(description_graph_layout)

    def on_buy_stock(self):
        symbol = self.stock_input.text().strip().upper()
        if not symbol:
            self.show_status("Please enter a stock symbol first", error=True)
            return


        self.show_status(f"Processing purchase of {symbol}...", error=False)

        # TODO: Replace with actual quantity
        success, answer = handle_buy_stock(self.email, symbol, 1)

        QTimer.singleShot(1500, lambda: self.show_status(answer, error=not success))

    def on_sell_stock(self):
        symbol = self.stock_input.text().strip().upper()
        if not symbol:
            self.show_status("Please enter a stock symbol first", error=True)
            return

        self.show_status(f"Processing sale of {symbol}...", error=False)

        # TODO: Replace with actual quantity
        success, answer = handle_sell_stock(self.email, symbol, 1)

        QTimer.singleShot(1500, lambda: self.show_status(answer, error=not success))

    def search_stock(self):
        symbol = self.stock_input.text().strip().upper()
        if not symbol:
            self.show_status("Please enter a stock symbol", error=True)
            return

        self.show_status(f"Loading information for {symbol}...", error=False)

        # Use QTimer to avoid freezing UI
        QTimer.singleShot(300, lambda: self.fetch_stock_info(symbol))

    def fetch_stock_info(self, symbol):
        try:
            success, stock_info = getStockDetails(symbol)
            if not success:
                self.show_status(stock_info, error=True)

            else:
                stock_info["price"] = float(stock_info["price"])
                stock_info["change"] = float(stock_info["change"])
                stock_info["change_percent"] = float(stock_info["change_percent"])

                # Update UI with stock info
                self.stock_name.setText(f"Stock Name: {stock_info['name']}")
                self.stock_price.setText(f"Current Price: ${stock_info['price']:.2f}")

                change_color = "green" if stock_info['change'] > 0 else "red"
                change_sign = "+" if stock_info['change'] > 0 else ""
                self.stock_change.setText(
                    f"Change: <span style='color:{change_color}'>{change_sign}{stock_info['change']:.2f} ({change_sign}{stock_info['change_percent']:.2f}%)</span>")

                self.market_cap.setText(f"Market Cap: {stock_info['market_cap']}")
                self.pe_ratio.setText(f"P/E Ratio: {stock_info['pe_ratio']}")
                self.dividend_yield.setText(f"Dividend Yield: {stock_info['dividend_yield']}%")

                # Update stock description
                # self.stock_description.setText(stock_info['description'])

                # Update stock image - In a real implementation, this would fetch the company logo
                # TODO: Replace with actual image fetching logic
                self.update_stock_image(symbol)

                # Update graph
                self.update_graph()

                self.show_status("", error=False)
        except Exception as e:
            self.show_status(f"Error fetching stock info: {str(e)}", error=True)


    def show_status(self, message, error=False):
        if not message:
            self.status_label.setVisible(False)
            return

        self.status_label.setVisible(True)
        self.status_label.setText(message)
        self.status_label.setStyleSheet("color: red;" if error else "color: green;")


    def update_stock_image(self, symbol):
        try:
            # Get logo using the stock symbol
            logo_response = getStockLogo(symbol)
            
            # Check if logo_response is valid before proceeding
            if logo_response and hasattr(logo_response, 'content'):
                pixmap = QPixmap()
                pixmap.loadFromData(logo_response.content)
                
                # Scale the logo to fit the frame while maintaining aspect ratio
                pixmap = pixmap.scaled(140, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.stock_image.setPixmap(pixmap)
            else:
                # If no logo found, display text with the symbol
                self.stock_image.setText(symbol)
        except Exception as e:
            print(f"Error displaying logo for {symbol}: {e}")
            self.stock_image.setText(symbol)




        

    def update_graph(self):
        # Get current timeframe selection
        if self.day_button.isChecked():
            timeframe = "day"
        elif self.week_button.isChecked():
            timeframe = "week"
        elif self.month_button.isChecked():
            timeframe = "month"
        else:
            timeframe = "year"

        symbol = self.stock_input.text().strip().upper()
        if not symbol:
            self.graph_placeholder.setText("Please enter a stock symbol to view graph")
            return

        # Update graph placeholder with timeframe information
        self.graph_placeholder.setText(f"Stock price history for {symbol} over the last {timeframe}\n\n" +
                                       "TODO: Implement actual graph visualization using PyQtGraph or Matplotlib")

        # In a real implementation, this would fetch historical data and update the graph
        # TODO: Replace with actual graph implementation

