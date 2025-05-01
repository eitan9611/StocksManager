from View.commons import *
from PySide6.QtWidgets import QCompleter
from Present.TradePresent import *
from Present.StockPresent import *
import pandas as pd
from PySide6.QtWidgets import QCompleter
import pyqtgraph as pg
import numpy as np
from PySide6.QtCore import Qt, QPointF


class StockInfoPage(QFrame):
    email = ""
    def __init__(self, email):
        super().__init__()
        self.email = email

        # Initialize API client

        # Create main layout
        main_layout = QVBoxLayout(self)

        # Create header
        header = QLabel("Stock Information")
        header.setObjectName("header")
        main_layout.addWidget(header)

        # Create search area
        search_layout = QHBoxLayout()

        # Stock symbol input with border frame
        input_frame = QFrame()
        input_frame.setObjectName("input_frame")
        input_frame.setStyleSheet("""
            QFrame#input_frame {
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 4px;
                background-color: white;
            }
        """)
        input_layout = QVBoxLayout(input_frame)
        input_layout.setContentsMargins(4, 4, 4, 4)

        self.stock_input = QLineEdit()
        self.stock_input.setPlaceholderText("Enter stock symbol (e.g., AAPL, TSLA)")
        self.stock_input.returnPressed.connect(self.search_stock)

        # שליפת מניות
        sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
        symbols = sp500['Symbol'].tolist()

        # קומפליטר
        completer = QCompleter(symbols)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.stock_input.setCompleter(completer)

        input_layout.addWidget(self.stock_input)

        search_layout.addWidget(input_frame, 1)

        # Search button
        self.search_button = QPushButton("Search")
        self.search_button.setObjectName("action_button")
        self.search_button.setMinimumHeight(40)
        self.search_button.clicked.connect(self.search_stock)
        search_layout.addWidget(self.search_button)

        # Buy Stock button

        # Buy-Sell buttons with quantity control

        self.buy_quantity = 1
        self.sell_quantity = 1

        # Buy button
        self.buy_button = QPushButton(f"Buy Stock (x{self.buy_quantity})")
        self.buy_button.setObjectName("action_button")
        self.buy_button.setMinimumHeight(40)
        self.buy_button.clicked.connect(self.on_buy_stock)
        search_layout.addWidget(self.buy_button)

        # Arrows for Buy
        self.buy_up_button = QToolButton()
        self.buy_up_button.setArrowType(Qt.UpArrow)
        self.buy_up_button.clicked.connect(self.increase_buy_quantity)
        search_layout.addWidget(self.buy_up_button)

        self.buy_down_button = QToolButton()
        self.buy_down_button.setArrowType(Qt.DownArrow)
        self.buy_down_button.clicked.connect(self.decrease_buy_quantity)
        search_layout.addWidget(self.buy_down_button)

        # Sell button
        self.sell_button = QPushButton(f"Sell Stock (x{self.sell_quantity})")
        self.sell_button.setObjectName("action_button")
        self.sell_button.setMinimumHeight(40)
        self.sell_button.clicked.connect(self.on_sell_stock)
        search_layout.addWidget(self.sell_button)

        # Arrows for Sell
        self.sell_up_button = QToolButton()
        self.sell_up_button.setArrowType(Qt.UpArrow)
        self.sell_up_button.clicked.connect(self.increase_sell_quantity)
        search_layout.addWidget(self.sell_up_button)

        self.sell_down_button = QToolButton()
        self.sell_down_button.setArrowType(Qt.DownArrow)
        self.sell_down_button.clicked.connect(self.decrease_sell_quantity)
        search_layout.addWidget(self.sell_down_button)


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
        
        current_text = self.stock_description.toPlainText()
        self.stock_description.setPlaceholderText(current_text)

        self.stock_description.setMaximumHeight(300)  # Match the height of the graph
        description_layout.addWidget(self.stock_description)

        description_graph_layout.addWidget(description_group)

        # Stock price history graph (right side)
        graph_group = QGroupBox("Stock Price History")
        graph_group.setObjectName("graph_group")
        graph_group.setStyleSheet("""
            QGroupBox#graph_group {
                background-color: #f8f9fa;
                border: 1px solid #dde0e3;
                border-radius: 8px;
            }
            QGroupBox#graph_group::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #3d5a80;
                font-weight: bold;
            }
        """)
        graph_layout = QVBoxLayout(graph_group)

        # Add buttons to select timeframe
        timeframe_layout = QHBoxLayout()

        # Timeframe selection
        timeframe_label = QLabel("Timeframe:")
        timeframe_label.setStyleSheet("font-weight: bold; color: #3d5a80;")
        timeframe_layout.addWidget(timeframe_label)

        self.timeframe_group = QButtonGroup(self)

        # Create a common style for the timeframe buttons
        button_style = """
            QPushButton {
                background-color: #e0e0e0;
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 5px 10px;
                font-weight: bold;
                color: #495057;
            }
            QPushButton:checked {
                background-color: #3d5a80;
                color: white;
            }
            QPushButton:hover {
                background-color: #dee2e6;
            }
        """

        self.day_button = QPushButton("Day")
        self.day_button.setCheckable(True)
        self.day_button.setChecked(True)
        self.day_button.clicked.connect(self.update_graph)
        self.day_button.setStyleSheet(button_style)
        self.timeframe_group.addButton(self.day_button)
        timeframe_layout.addWidget(self.day_button)

        self.week_button = QPushButton("Week")
        self.week_button.setCheckable(True)
        self.week_button.clicked.connect(self.update_graph)
        self.week_button.setStyleSheet(button_style)
        self.timeframe_group.addButton(self.week_button)
        timeframe_layout.addWidget(self.week_button)

        self.month_button = QPushButton("Month")
        self.month_button.setCheckable(True)
        self.month_button.clicked.connect(self.update_graph)
        self.month_button.setStyleSheet(button_style)
        self.timeframe_group.addButton(self.month_button)
        timeframe_layout.addWidget(self.month_button)

        self.year_button = QPushButton("Year")
        self.year_button.setCheckable(True)
        self.year_button.clicked.connect(self.update_graph)
        self.year_button.setStyleSheet(button_style)
        self.timeframe_group.addButton(self.year_button)
        timeframe_layout.addWidget(self.year_button)

        timeframe_layout.addStretch()
        graph_layout.addLayout(timeframe_layout)

        # Create graph placeholder - replaced with actual PyQtGraph widget
        self.graph_frame = QFrame()
        self.graph_frame.setMinimumHeight(300)
        self.graph_frame.setObjectName("graph_frame")
        self.graph_layout = QVBoxLayout(self.graph_frame)
        
        # Initialize the PyQtGraph plot widget with custom stylesheet
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('#f8f9fa')  # Light background color
        self.plot_widget.getPlotItem().layout.setRowFixedHeight(4, 35)
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        
        # Style the plot axes and labels
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        
        axis_pen = pg.mkPen(color='#495057', width=1.5)
        label_style = {'color': '#3d5a80', 'font-size': '12pt', 'font-weight': 'bold'}
        
        # Style the axes
        for axis in ['left', 'bottom']:
            ax = self.plot_widget.getAxis(axis)
            ax.setPen(axis_pen)
            ax.setTextPen(pg.mkPen('#495057'))
            ax.setTickFont(font)
            ax.setStyle(tickLength=10)
        
        self.graph_layout.addWidget(self.plot_widget)
        
        # Initialize the data point and curve
        self.data_curve = None
        self.data_points = None
        self.value_label = None
        
        graph_layout.addWidget(self.graph_frame)
        description_graph_layout.addWidget(graph_group, 1)  # Give graph more stretch

        # Add the horizontal layout to the main layout
        main_layout.addLayout(description_graph_layout)
        
        # Initialize hover point with a nicer style
        self.hover_point = pg.ScatterPlotItem(
            size=12, 
            brush=pg.mkBrush(61, 90, 128, 200),  # Match our theme color with some transparency
            pen=pg.mkPen('w', width=2)  # White border for better visibility
        )
        self.plot_widget.addItem(self.hover_point)
        
        # Disable mouse panning/zooming to make the graph static
        self.plot_widget.setMouseEnabled(x=False, y=False)
        self.plot_widget.hideButtons()  # Hide the auto-scale button

    def on_buy_stock(self):
        symbol = self.stock_input.text().strip().upper()
        quantity = self.buy_quantity

        if not symbol:
            self.show_status("Please enter a stock symbol first", error=True)
            return

        self.show_status(f"Processing purchase of {quantity} shares of {symbol}...", error=False)

        success, answer = handle_buy_stock(self.email, symbol, quantity)

        QTimer.singleShot(1500, lambda: self.show_status(answer, error=not success))



    def on_sell_stock(self):
        symbol = self.stock_input.text().strip().upper()
        quantity = self.sell_quantity

        if not symbol:
            self.show_status("Please enter a stock symbol first", error=True)
            return

        self.show_status(f"Processing sale of {quantity} shares of {symbol}...", error=False)

        success, answer = handle_sell_stock(self.email, symbol, quantity)

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
                self.dividend_yield.setText(f"Dividend Yield: {stock_info['dividend_yield']}")

                # Update stock image - In a real implementation, this would fetch the company logo
                self.update_stock_image(symbol)

                success_desc, company_description = getCompanyDescription(symbol)
                if success_desc:
                    self.stock_description.setText(company_description)
                else:
                    self.stock_description.setText(f"No description available for {symbol}.")

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
            logo_response = get_company_logo(symbol)
            
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

    def get_stock_data(self, timeframe):
        symbol = self.stock_input.text().strip().upper()
        
        if not symbol:
            # Handle empty symbol
            return [0], [0]
        
        if timeframe == "day":
            x_values, y_values = get_prices_today(symbol)
            x_indices = list(range(len(x_values)))  # map hours to indices
            return x_indices, y_values
        
        elif timeframe == "week":
            x_values, y_values = get_prices_last_week(symbol)
            if not x_values:  # Check if list is empty
                return [0], [0]
            x_indices = list(range(len(x_values)))
            return x_indices, y_values
            
        elif timeframe == "month":
            x_values, y_values = get_prices_last_month(symbol)
            if not x_values:  # Check if list is empty
                return [0], [0]
            x_indices = list(range(len(x_values)))
            return x_indices, y_values
        
        else:  # year
            x_values, y_values = get_prices_last_year(symbol)
            if not x_values:  # Check if list is empty
                return [0], [0]
            x_indices = list(range(len(x_values)))
            return x_indices, y_values

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
            # Clear the plot and add a message
            self.plot_widget.clear()
            self.plot_widget.getPlotItem().getViewBox().setDefaultPadding(0.1)
            self.plot_widget.setTitle("Please enter a stock symbol to view graph")
            return

        # Get data based on timeframe
        x_data, y_data = self.get_stock_data(timeframe)
        
        # Clear previous plot
        self.plot_widget.clear()
        
        # Reset value label and hover point
        self.value_label = None
        
        # Set fixed y-axis range with padding
        y_min = min(y_data) * 0.995
        y_max = max(y_data) * 1.005
        self.plot_widget.setYRange(y_min, y_max, padding=0)

        # Set fixed x-axis range with padding
        if x_data:
            self.plot_widget.setXRange(min(x_data) - 0.5, max(x_data) + 0.5, padding=0)
        
        # Set axis labels and title with custom styling
        title_html = f"<span style='font-size: 16pt; font-weight: bold; color: #3d5a80;'>{symbol} Stock Price - {timeframe.capitalize()}</span>"
        self.plot_widget.setTitle(title_html)
        
        # Set styles for left axis (price)
        left_axis = self.plot_widget.getAxis('left')
        left_axis.setLabel('Price ($)', **{'color': '#3d5a80', 'font-size': '12pt'})
        
        # Set x-axis label and ticks based on timeframe
        bottom_axis = self.plot_widget.getAxis('bottom')
        bottom_axis.setHeight(40)
        
        if timeframe == "day":
            bottom_axis.setLabel('Hour', **{'color': '#3d5a80', 'font-size': '12pt'})
            # Set tick labels for hours
            ticks = [(i, f"{i}:00") for i in range(24)]
            bottom_axis.setTicks([ticks])
            
        elif timeframe == "week":
            bottom_axis.setLabel('Day', **{'color': '#3d5a80', 'font-size': '12pt'})
            # Set tick labels for days
            days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            ticks = [(i, days[i]) for i in range(7)]
            bottom_axis.setTicks([ticks])
            
        elif timeframe == "month":
            bottom_axis.setLabel('Week', **{'color': '#3d5a80', 'font-size': '12pt'})
            # Set tick labels for weeks
            ticks = [(i, f"Week {i+1}") for i in range(4)]
            bottom_axis.setTicks([ticks])
            
        else:  # year
            bottom_axis.setLabel('Month', **{'color': '#3d5a80', 'font-size': '12pt'})
            # Set tick labels for months
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            ticks = [(i, months[i]) for i in range(12)]
            bottom_axis.setTicks([ticks])
        
        # Add fill area under the curve
        fill_color = pg.mkBrush(61, 90, 128, 30)  # Match theme color with transparency
        fill = pg.FillBetweenItem(
            pg.PlotCurveItem(x_data, y_data),
            pg.PlotCurveItem(x_data, [y_min] * len(x_data)),
            fill_color
        )
        self.plot_widget.addItem(fill)
        
        # Create a gradient pen for a more professional look
        gradient = QLinearGradient(0, 0, 0, 1)
        gradient.setCoordinateMode(QGradient.ObjectMode)
        gradient.setColorAt(0, QColor(61, 90, 128))  # Top color - our theme blue
        gradient.setColorAt(1, QColor(98, 148, 166))  # Bottom color - lighter blue
        
        brush = QBrush(gradient)
        pen = pg.mkPen(color=QColor(61, 90, 128), width=3)
        
        # Create the plot line with the gradient pen
        self.data_curve = self.plot_widget.plot(x_data, y_data, pen=pen)
        
        # Add data points
        scatter = pg.ScatterPlotItem(
            x=x_data, 
            y=y_data, 
            size=8, 
            brush=pg.mkBrush(255, 255, 255), 
            pen=pg.mkPen(QColor(61, 90, 128), width=2),
            symbol='o'
        )
        self.plot_widget.addItem(scatter)
        
        # Store the data points
        self.data_points = {'x': x_data, 'y': y_data}
        
        # Recreate hover point with a nicer style
        self.hover_point = pg.ScatterPlotItem(
            size=12, 
            brush=pg.mkBrush(61, 90, 128, 200),  
            pen=pg.mkPen('w', width=2)  
        )
        self.plot_widget.addItem(self.hover_point)
        
        # Set up tooltip label for hover information - reconnect every time
        self.plot_widget.scene().sigMouseMoved.connect(self.mouse_moved)
        
        # Store current timeframe for mouse_moved method
        self.current_timeframe = timeframe

    def mouse_moved(self, pos):
        if self.data_points is None:
            return
            
        # Convert position to plot coordinates
        plot_item = self.plot_widget.getPlotItem()
        vb = plot_item.getViewBox()
        if vb is None:
            return
            
        mouse_point = vb.mapSceneToView(pos)
        x, y = mouse_point.x(), mouse_point.y()
        
        # Check if mouse is within the data range (x-axis)
        x_min = min(self.data_points['x'])
        x_max = max(self.data_points['x'])
        
        # Only process if mouse is within x-range with some padding
        if x < x_min - 0.5 or x > x_max + 0.5:
            # Hide tooltip when outside data range
            self.hover_point.setData([], [])
            if hasattr(self, 'value_label') and self.value_label is not None:
                self.value_label.setVisible(False)
            return
        
        # Find the nearest point in our data
        if len(self.data_points['x']) > 0:
            # Get x-range to create an adaptive threshold
            x_range = max(self.data_points['x']) - min(self.data_points['x'])
            threshold = max(1.0, x_range * 0.1)  # 10% of x-range or at least 1.0
            
            # Consider only x-distance for finding nearest point
            nearest_index = None
            min_distance = float('inf')
            
            for i in range(len(self.data_points['x'])):
                dx = abs(x - self.data_points['x'][i])
                if dx < min_distance:
                    min_distance = dx
                    nearest_index = i
                    
            nearest_x = self.data_points['x'][nearest_index]
            nearest_y = self.data_points['y'][nearest_index]
            
            # Only show tooltip if mouse is close enough to a data point on x-axis
            if min_distance < threshold:
                # Update position of hover point
                self.hover_point.setData([nearest_x], [nearest_y])
                
                # Get current timeframe for proper labeling
                if self.day_button.isChecked():
                    timeframe = "day"
                    time_label = f"Hour: {int(nearest_x)}:00"
                elif self.week_button.isChecked():
                    timeframe = "week"
                    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
                    time_label = f"Day: {days[int(nearest_x)]}"
                elif self.month_button.isChecked():
                    timeframe = "month"
                    time_label = f"Week: {int(nearest_x) + 1}"
                else:  # year
                    timeframe = "year"
                    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                    time_label = f"Month: {months[int(nearest_x)]}"
                
                # Create tooltip with nicer styling
                if not hasattr(self, 'value_label') or self.value_label is None:
                    self.value_label = pg.TextItem(
                        html=f"""
                        <div style='background-color: rgba(255, 255, 255, 0.85); 
                                padding: 5px; 
                                border: 1px solid #3d5a80; 
                                border-radius: 3px;'>
                            <span style='color: #3d5a80; font-weight: bold;'>{time_label}</span><br>
                            <span style='color: #2c3e50;'>Price: <b>${nearest_y:.2f}</b></span>
                        </div>
                        """,
                        anchor=(0, 1)
                    )
                    self.plot_widget.addItem(self.value_label)
                else:
                    self.value_label.setHtml(f"""
                    <div style='background-color: rgba(255, 255, 255, 0.85); 
                            padding: 5px; 
                            border: 1px solid #3d5a80; 
                            border-radius: 3px;'>
                        <span style='color: #3d5a80; font-weight: bold;'>{time_label}</span><br>
                        <span style='color: #2c3e50;'>Price: <b>${nearest_y:.2f}</b></span>
                    </div>
                    """)
                    
                # Position the tooltip slightly above and to the right of the data point
                # Adjust label position to stay within viewbox
                # Adjust label position to stay within viewbox properly
                offset_x = 0.1
                offset_y = 0.3

                # Get current view range
                view_range = vb.viewRange()
                x_range, y_range = view_range[0], view_range[1]

                # Default label position: top-right of the point
                label_x = nearest_x + offset_x
                label_y = nearest_y + offset_y

                # Estimate size of the tooltip
                self.value_label.setPos(0, 0)  # temporarily to (0, 0) to measure
                label_rect = self.value_label.boundingRect()
                label_width = label_rect.width()
                label_height = label_rect.height()

                # Now check and adjust for edges
                # Right side
                if label_x + label_width > x_range[1]:
                    label_x = nearest_x - offset_x - label_width

                # Left side
                if label_x < x_range[0]:
                    label_x = x_range[0] + 0.1

                # Top side
                if label_y + label_height > y_range[1]:
                    label_y = nearest_y - offset_y - label_height

                # Bottom side
                if label_y < y_range[0]:
                    label_y = y_range[0] + 0.1

                # Now set the corrected position
                self.value_label.setPos(label_x, label_y)
                self.value_label.setVisible(True)

            else:
                # Hide tooltip when not near a data point
                self.hover_point.setData([], [])
                if hasattr(self, 'value_label') and self.value_label is not None:
                    self.value_label.setVisible(False)


    def increase_buy_quantity(self):
        self.buy_quantity += 1
        self.buy_button.setText(f"Buy Stock (x{self.buy_quantity})")

    def decrease_buy_quantity(self):
        if self.buy_quantity > 1:
            self.buy_quantity -= 1
            self.buy_button.setText(f"Buy Stock (x{self.buy_quantity})")

    def increase_sell_quantity(self):
        self.sell_quantity += 1
        self.sell_button.setText(f"Sell Stock (x{self.sell_quantity})")

    def decrease_sell_quantity(self):
        if self.sell_quantity > 1:
            self.sell_quantity -= 1
            self.sell_button.setText(f"Sell Stock (x{self.sell_quantity})")
