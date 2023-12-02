import sys
from PyQt5.QtWidgets import QWidget, QLabel, QCalendarWidget, QDesktopWidget,QFrame, QLineEdit,  QPushButton, QVBoxLayout, QSpacerItem, QSizePolicy, QSizePolicy, QDesktopWidget, QMessageBox, QComboBox, QTextEdit, QTableWidget, QHBoxLayout, QSplitter, QScrollArea, QFileDialog, QTableWidgetItem, QApplication, QDateEdit
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QDate
import csv
import sqlite3
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

class LoginApp(QWidget):
    def __init__(self):
        """
        Initializes the login application window.

        Creates a window for entering credentials using widget styles,
        customize the size of the window, and create controls such as a logo,
        login and password fields, a login button, and a "Forgot Password?" button.
        Binds functions to button press events to perform appropriate actions.
        """
        
        super().__init__()
        
        # Selecting styles for widgets
        self.setStyleSheet('''
            /* main styles */
            * {
                font-family: Roboto, Arial, sans-serif;
                font-size: 13pt;
            }
            QWidget {
                background-color: #ffffff;
            }
            QLineEdit, QTextEdit, QComboBox {
                background-color: #ffffff;
                border: 1px solid #005bbd; /* blue border */
                border-radius: 5px; /* rounded border */
                padding: 5px;
            }
            QLineEdit:hover, QTextEdit:hover, QComboBox:hover {
                border: 1px solid #2980b9; /* color on selecting */
            }

            QPushButton {
                background-color: #005bbd; 
                border: 2px solid #005bbd; 
                border-radius: 20px; 
                color: white;
                border-radius: 5px; /* Скругление углов */
                padding: 8px 8px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 20px;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }

            QLabel {
                color: #333;
            }
 
            QPushButton#forgetPasswordButton {
                background-color: white;
                color: #005bbd; 
                border: 0px solid #3498db; 
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton#forgetPasswordButton:hover {
                background-color: #f0f0f0; 
            }
        ''')
        self.setWindowIcon(QIcon('app_files\\ega_app_logo.png'))
        # setts for main screen
        self.setWindowTitle('Login App')
        self.setFixedSize(380, 530)

        # create logo on login screen
        self.logo_label = QLabel()
        pixmap = QPixmap('app_files\\EGA_logo.jpg')
        pixmap_resized = pixmap.scaled(300, 300, aspectRatioMode=Qt.KeepAspectRatio)
        self.logo_label.setPixmap(pixmap_resized)
        self.logo_label.setAlignment(Qt.AlignCenter)

        # create widgets for buttons and input
        self.login_label = QLabel('Login:')
        self.password_label = QLabel('Password:')
        self.login_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton('Sign in')
        self.forget_password_button = QPushButton('Forgot password?', objectName='forgetPasswordButton')

        # # Default inputs
        self.login_input.setText('admin')
        self.password_input.setText('admin')

        # Connecting buttons with functions
        self.login_button.clicked.connect(self.check_credentials)
        self.forget_password_button.clicked.connect(self.show_forgot_password)

        # Create vertical container
        vbox = QVBoxLayout()
        vbox.addWidget(self.logo_label)
        vbox.addWidget(self.login_label)
        vbox.addWidget(self.login_input)
        vbox.addWidget(self.password_label)
        vbox.addWidget(self.password_input)
        vbox.addWidget(self.login_button)
        vbox.addWidget(self.forget_password_button)
        
        # add space above
        spacer = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox.addItem(spacer)

        self.setLayout(vbox)



    
    def showEvent(self, event):
        """
        Overrides the showEvent method to handle the window display event.

        Called when the window is displayed. Calls the method to position the window in the center of the screen.
        """
        super().showEvent(event)
        self.centerWindow()  



    def centerWindow(self):
        """
        Locates the window in the center of the screen.

        Gets the screen size, window dimensions and calculates the center position of the window.
        Sets the window position to the center of the screen.
        """
        # Get screen size
        screen = QDesktopWidget().screenGeometry()
        width, height = screen.width(), screen.height()
        window_width, window_height = self.width(), self.height()

        # Calculate the center
        x_position = (width - window_width) // 2
        y_position = (height - window_height) // 2

        # Set position
        self.move(x_position, y_position)


    def check_credentials(self):
        """
        Verifies the entered credentials.

        Gets login and password from the corresponding input fields.
        If the login and password match 'admin', opens the SQL scripts window.
        Otherwise, displays an error message.
        """
        login = self.login_input.text()
        password = self.password_input.text()

        # Check the login and password
        if login.strip() == 'admin' and password.strip() == 'admin':
        # Open the SQL scripts window on successful login
            self.open_sql_screen()
            self.close()  
        else:
            # Displaying an error message in case of invalid credentials
            QMessageBox.warning(self, 'Login error', 'Invalid login or password. Try again.')


    def show_forgot_password(self):
        """
        Displays a message window with information about password recovery.

        Opens a dialog box with information on how to reset the password.
        """
        message = QMessageBox()  # Creating a dialog box object
        message.setWindowTitle("Forgot Password")  # Setting the window title
        message.setText("Contact technical support at support@egaconsult.com to reset your password.")  # Setting the message text
        message.setIcon(QMessageBox.Information)  # Installing the message icon
        message.setStandardButtons(QMessageBox.Ok)  # Setting the standard confirmation button
        message.exec_()  # Displaying the dialog box


    def open_sql_screen(self):
        self.sql_window = QWidget()
        # Window lable
        self.sql_window.setWindowTitle('EGA tool WorkSpace')
        self.sql_window.setStyleSheet('''
        * {
            font-family: Arial, sans-serif;
            font-size: 16pt;
        }
        QWidget {
            background-color: #ffffff;
            font-size: 18pt;
            border-radius: 4px;
        }
        QPushButton {
            background-color: #005bbd;
            border: 2px solid #005bbd;
            border-radius: 5px; /* Скругление углов */
            color: white;
            padding: 8px 16px;
            text-align: center;
            text-decoration: none;
            font-size: 18px;
            cursor: pointer;
        }
        QPushButton:hover {
            background-color: #2980b9;
            border-radius: 5px; /* Скругление углов */
        }
        QLabel {
            color: #333;
        }
        QComboBox {
            border: 1px solid #ccc;
            border-radius: 4px;
            font-size: 18px;
            color: #333;
            background-color: #fff;
            selection-background-color: #e0e0e0;
        }
        QComboBox:drop-down {
            width: 14px;
        }
        QComboBox::drop-down::down-arrow {
            image: url(down_arrow.png);
        }
        ''')

        # Predestination of possible lists
        actions = [
            "Choose action",
            "List of clients grouped by city",
            "Contracts report",
            "List of individual service contracts",
            "List of contracts grouped by type of service for the past year",
            "Three most important customers (those who brought the most profit)",
            "List of employees sorted in reverse order according to the value of the contract amount",
            "Average monthly amount of contracts for services of each type"
        ]
        
        # Creating drop-down lists for selecting sql scripts
        # First list
        self.action_combo_box = QComboBox()
        self.action_combo_box.addItems(actions)
        self.action_combo_box.currentIndexChanged.connect(self.update_second_combo)
        self.action_combo_box.currentIndexChanged.connect(self.update_sql_script)
        # Second drop-down list (if possible)
        self.second_combo = QComboBox()
        self.second_combo.addItems([])  
        self.second_combo.currentIndexChanged.connect(self.update_sql_script)

        # Connecting to the database
        conn = sqlite3.connect('app_files\\EGA_database.db')
        print(conn)
        cursor = conn.cursor()

        # Executing queries to fill in the values of the second drop-down list with valid data
        cursor.execute("SELECT DISTINCT City FROM Clients")
        result = cursor.fetchall()
        cities = [row[0] for row in result]

        cursor.execute("SELECT DISTINCT servicename FROM service")
        result_services = cursor.fetchall()
        unique_services = [row[0] for row in result_services]

        cursor.execute("SELECT DISTINCT TypeServicename FROM typeservice")
        result = cursor.fetchall()
        unique_type_services = [row[0] for row in result]

        # Closing the database connection
        conn.close()

        # Set dict to drop-down list
        self.second_combos = {
            "Choose action":[],
            "List of clients grouped by city": cities,
            "Contracts report": [],
            "List of individual service contracts": unique_services,
            'List of contracts grouped by type of service for the past year': unique_type_services,
            'Three most important customers (those who brought the most profit)': [],
            'List of employees sorted in reverse order according to the value of the contract amount': [],
            'Average monthly amount of contracts for services of each type': []
        }

        
        # Creating the SQL Editor header
        self.sql_label = QLabel('Enter an SQL script or select an action:')
        self.sql_label.setStyleSheet('''QWidget { font-size: 26px; }''')
        # Creating an SQL script input window
        self.sql_input = QTextEdit()
        self.sql_input.setPlaceholderText("SQL-script: SELECT ...")
      
        self.sql_input.setStyleSheet(
            '''QWidget {
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 20px;
                font-family: consolas;
                padding: 8px 16px;
                font-size: 18px;
            }''')
        # Creating an SQL script launch button
        self.execute_button = QPushButton('RUN')
        # Creating a tabular window for the output of the SQL script result
        self.result_table = QTableWidget()  # Using QTableWidget to display the results
        self.result_table.setStyleSheet(
            '''QWidget {
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 16px;
                font-family: consolas;
            }''')
        
        horizontal_layout  = QHBoxLayout()

        self.contract_number_input = QLineEdit()
        self.contract_number_input.setPlaceholderText("Number of Contract")
        self.contract_number_input.setStyleSheet(
            '''QWidget {
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 18px;
            }''')
        
        horizontal_layout.addWidget(self.contract_number_input)

        spacer = QSpacerItem(20, 20)
        horizontal_layout.addItem(spacer)

        self.load_image_button = QPushButton('Download scan of contract')
        self.load_image_button.clicked.connect(self.load_contract_image)
        horizontal_layout.addWidget(self.load_image_button)

        

        outer_splitter = QSplitter(Qt.Horizontal)
        inner_splitter = QSplitter(Qt.Vertical)

        # Creating a button for loading the result of an SQL script in the format .csv
        download_button = QPushButton('Download to CSV') 
        download_button.clicked.connect(self.download_csv)

        # Creating widgets of the upper and lower left blocks 
        upper_left_widget = QWidget()
        down_left_widget = QWidget()

        # Creating layouts of the upper and lower left blocks
        upper_left_layout = QVBoxLayout()
        down_left_layout = QVBoxLayout()

        upper_left_button_layout = QHBoxLayout()
        change_button = QPushButton('Change Data') 
        change_button.clicked.connect(self.update_data_screen)
        add_button = QPushButton('Add Data')
        add_button.clicked.connect(self.add_data_screen)
        delete_button = QPushButton('Delete Data')

        upper_left_button_layout.addWidget(change_button)
        upper_left_button_layout.addWidget(add_button)
        upper_left_button_layout.addWidget(delete_button)

        upper_left_layout.addLayout(upper_left_button_layout)
        # The upper layout consists of a header, two drop-down lists, a script input block and a start button
        upper_left_layout.addWidget(self.sql_label)
        upper_left_layout.addWidget(self.action_combo_box)
        upper_left_layout.addWidget(self.second_combo)
        upper_left_layout.addWidget(self.sql_input)
        upper_left_layout.addWidget(self.execute_button)

        # The lower layout consists of a script output block, a csv upload button, and a contract
        down_left_layout.addWidget(self.result_table)
        down_left_layout.addWidget(download_button)
        down_left_layout.addLayout(horizontal_layout)

        # Filling in widgets
        upper_left_widget.setLayout(upper_left_layout)
        down_left_widget.setLayout(down_left_layout)


        
        # Adding left blocks to the horizontal divider
        inner_splitter.addWidget(upper_left_widget)
        inner_splitter.addWidget(down_left_widget)

        
        # Defining the right block
        right_widget = QWidget()
        right_widget.setStyleSheet(
            '''QWidget {
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 4px;
            }''')
        right_layout = QVBoxLayout()

        # Definition of the diagram image
        image_label = QLabel()
        pixmap = QPixmap('app_files\\shema22.jpg')
        image_label.setPixmap(pixmap)
        # image_label.setFixedSize(pixmap.size())
        image_label.setAlignment(Qt.AlignCenter)

        # Creating a scroll for the database schema
        scroll_area = QScrollArea()
        scroll_area.setWidget(image_label)
        scroll_area.setWidgetResizable(True)
        

        # Adding blocks of the right widget
        right_layout.addWidget(scroll_area)
        right_widget.setLayout(right_layout)

        # Adding blocks to the vertical separator
        outer_splitter.addWidget(inner_splitter)
        outer_splitter.addWidget(right_widget)

        # Creating a box for shared blocks and exit buttons
        vbox = QVBoxLayout()
        vbox.addWidget(outer_splitter)
        self.execute_button.clicked.connect(self.execute_sql_script)
        back_to_login_button = QPushButton('Back to Login')
        back_to_login_button.clicked.connect(self.confirm_exit) 
        vbox.addWidget(back_to_login_button)
        self.sql_window.setLayout(vbox)

        # Full screen
        self.sql_window.showFullScreen()



    def update_data_screen(self):
        """
        Change data in database window.

        Creates an oversized window for modifying existing values of database table fields. 
        The window is divided into several frames for each database table.
        """
        
        self.update_data_window = QWidget() # Main update window widget
        self.update_data_window.setWindowTitle('Update Data') # Label of window 
        update_main_layout = QVBoxLayout()  # main add data window layout

        # Drop-down widget to choose dates for contract
        self.update_contract_signing_date_choose = QDateEdit()
        self.update_contract_start_date_choose = QDateEdit()
        self.update_contract_end_date_choose = QDateEdit()
        self.update_contract_pay_date_choose = QDateEdit()
        
        self.update_contract_price_choose = QLineEdit() # Price of contract
        
        
        
        desktop = QDesktopWidget()
        # Get the dimensions of the user's home screen
        screen_size = desktop.screenGeometry()
        # Width and height of the main user screen
        width = screen_size.width()
        height = screen_size.height()
        self.update_data_window.setFixedWidth(width)
        
        # First line layout of update window
        line1 = QHBoxLayout()
        
        # 1. Company table frame
        update_company_frame = QFrame()
        update_company_frame.setStyleSheet('''                    
            QFrame {
                border: 1px solid #ccc;
                font-size: 12pt;
                border-radius: 5px;
                background-color: #ffffff
            }
            QLabel {
                font-size: 12pt;
                border: none;
            }
            QLineEdit {
                border: 2px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
                                    min-width: 80px;
            }
            QComboBox {
                border: 2px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
                color: #333;
                background-color: #fff;
                selection-background-color: #e0e0e0;
            }
            QPushButton {
                background-color: #005bbd;
                border: 2px solid #005bbd;
                border-radius: 5px;
                color: white;
                text-align: center
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        ''')
        update_company_layout = QVBoxLayout()   # company table layout
        update_company_label = QLabel("Company table")
        update_company_input_layout = QHBoxLayout() # Company all input layout
        update_company_choose_layout = QVBoxLayout()    # Company previous name layout
        update_company_choose_label = QLabel("Prev name")
        self.update_company_choose = QComboBox() # ComboBox in Company table
        self.update_client_company_choose = QComboBox() # ComboBox in client table
        self.update_contract_company_choose = QComboBox()   # ComboBox in contract table
        update_company_choose_layout.addWidget(update_company_choose_label)
        update_company_choose_layout.addWidget(self.update_company_choose)
        # Adding items into ComboBoxes of company name for all frames
        try:
            conn = sqlite3.connect('app_files\\EGA_database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT companyname FROM Company")
            companies = cursor.fetchall()
            for company in companies:
                self.update_company_choose.addItem(company[0])
                self.update_client_company_choose.addItem(company[0])
                self.update_contract_company_choose.addItem(company[0])
            conn.close()
        except sqlite3.Error as e:
            print(f"Error: {str(e)}")
        
        update_company_edit_layout = QVBoxLayout() #Layout for company new name input
        update_company_edit_label = QLabel("New name")
        self.update_company_edit = QLineEdit()
        update_company_edit_layout.addWidget(update_company_edit_label)
        update_company_edit_layout.addWidget(self.update_company_edit)
        update_company_button = QPushButton('Change')
        update_company_button.clicked.connect(self.update_company_table)
        # Set all object into Company table layout
        update_company_input_layout.addLayout(update_company_choose_layout)
        update_company_input_layout.addLayout(update_company_edit_layout)
        update_company_layout.addWidget(update_company_label)
        update_company_layout.addLayout(update_company_input_layout)
        update_company_layout.addWidget(update_company_button)
        # Set layout in Company table frame
        update_company_frame.setLayout(update_company_layout)




        # 2. Client table frame
        update_client_frame = QFrame()
        update_client_frame.setStyleSheet('''                    
            QFrame {
                border: 1px solid #ccc;
                font-size: 12pt;
                border-radius: 5px;
                background-color: #ffffff
            }
            QLabel {
                font-size: 12pt;
                border: none;
            }
            QLineEdit {
                border: 2px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
                                    min-width: 80px;
            }
            QComboBox {
                border: 2px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
                color: #333;
                background-color: #fff;
                selection-background-color: #e0e0e0;
            }
            QPushButton {
                background-color: #005bbd;
                border: 2px solid #005bbd;
                border-radius: 5px;
                color: white;
                text-align: center
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        ''')
        update_client_layout = QVBoxLayout() # Main client frame layoyt
        update_client_label = QLabel('Client Table')
        update_client_button = QPushButton('Change')
        update_client_button.clicked.connect(self.update_client_table)
        update_client_input_layout = QHBoxLayout() # Main Layout for client input in client frame
        update_client_name_layout = QVBoxLayout() # Layout of revious client name 
        update_client_name_label = QLabel('Prev Name')
        self.update_client_name_choose = QComboBox() # ComboBox of client name for client table
        self.update_contract_client_choose = QComboBox()    # ComboBox of client name for contract table
        # # Adding items into ComboBoxes of client name for all frames
        try:
            conn = sqlite3.connect('app_files\\EGA_database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT clientname FROM clients")
            clientnames = cursor.fetchall()
            for clientname in clientnames:
                self.update_client_name_choose.addItem(clientname[0])
                self.update_contract_client_choose.addItem(clientname[0])
            conn.close()
        except sqlite3.Error as e:
            print(f"Error: {str(e)}")
        
        self.update_client_name_choose.currentIndexChanged.connect(self.on_client_changed)  # Func of client name changing 
        update_client_name_layout.addWidget(update_client_name_label)
        update_client_name_layout.addWidget(self.update_client_name_choose)

        update_client_company_layout = QVBoxLayout() # Layout of client company name in client frame
        update_client_company_label = QLabel("Company")
        # Set current company name for chosen client
        try:
            conn = sqlite3.connect('app_files\\EGA_database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT companyname FROM Company join clients using(companyid) where clientname = ?", (self.update_client_name_choose.currentText(),))
            curent_company = cursor.fetchone()[0]
            self.update_client_company_choose.setCurrentText(curent_company)
            conn.close()
        except sqlite3.Error as e:
            print(f"Error: {str(e)}")
        update_client_company_layout.addWidget(update_client_company_label)
        update_client_company_layout.addWidget(self.update_client_company_choose)

        update_client_new_name_layout = QVBoxLayout() #
        update_client_new_name_label = QLabel('New cleint name')
        self.update_client_new_name_input = QLineEdit()
        update_client_new_name_layout.addWidget(update_client_new_name_label)
        update_client_new_name_layout.addWidget(self.update_client_new_name_input)

        update_client_city_layout = QVBoxLayout()
        update_client_city_label = QLabel('City')
        self.update_client_city = QLineEdit()
        update_client_city_layout.addWidget(update_client_city_label)
        update_client_city_layout.addWidget(self.update_client_city)

        update_client_address_layout = QVBoxLayout()
        update_client_adress_label = QLabel('Address')
        self.update_client_address = QLineEdit()
        update_client_address_layout.addWidget(update_client_adress_label)
        update_client_address_layout.addWidget(self.update_client_address)

        update_client_phone_layout = QVBoxLayout()
        update_client_phone_label = QLabel('Phone')
        self.update_client_phone = QLineEdit()
        update_client_phone_layout.addWidget(update_client_phone_label)
        update_client_phone_layout.addWidget(self.update_client_phone)

        update_client_input_layout.addLayout(update_client_name_layout)
        update_client_input_layout.addLayout(update_client_company_layout) 
        update_client_input_layout.addLayout(update_client_new_name_layout)
        update_client_input_layout.addLayout(update_client_city_layout)
        update_client_input_layout.addLayout(update_client_address_layout)
        update_client_input_layout.addLayout(update_client_phone_layout)

        update_client_layout.addWidget(update_client_label)
        update_client_layout.addLayout(update_client_input_layout)
        update_client_layout.addWidget(update_client_button)
        update_client_frame.setLayout(update_client_layout)


        

        line1.addWidget(update_company_frame)
        line1.addWidget(update_client_frame)



        line2 = QHBoxLayout()

        update_type_service_frame = QFrame()
        update_type_service_frame.setStyleSheet('''                    
            QFrame {
                border: 1px solid #ccc;
                font-size: 12pt;
                border-radius: 5px;
                background-color: #ffffff
            }
            QLabel {
                font-size: 12pt;
                border: none;
            }
            QLineEdit {
                border: 2px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
                                    min-width: 80px;
            }
            QComboBox {
                border: 2px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
                color: #333;
                background-color: #fff;
                selection-background-color: #e0e0e0;
            }
            QPushButton {
                background-color: #005bbd;
                border: 2px solid #005bbd;
                border-radius: 5px;
                color: white;
                text-align: center
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        ''')
        update_type_service_label = QLabel('Type service tabel')
        update_type_service_layout = QVBoxLayout()
        update_type_service_button = QPushButton('Change')
        update_type_service_button.clicked.connect(self.update_type_service_table)

        update_type_service_input_layout = QHBoxLayout()

        update_type_service_choose_layout = QVBoxLayout()
        update_type_service_choose_label = QLabel('Prev name')
        self.update_type_service_choose = QComboBox()
        self.update_service_type_service_choose = QComboBox()
        self.update_contract_type_service_choose = QComboBox()
        try:
            conn = sqlite3.connect('app_files\\EGA_database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT typeservicename FROM typeservice")
            typeservicenames = cursor.fetchall()
            for typeservicename in typeservicenames:
                self.update_type_service_choose.addItem(typeservicename[0])
                self.update_service_type_service_choose.addItem(typeservicename[0])
                self.update_contract_type_service_choose.addItem(typeservicename[0])
            conn.close()
        except sqlite3.Error as e:
            print(f"Error: {str(e)}")
        update_type_service_choose_layout.addWidget(update_type_service_choose_label)
        update_type_service_choose_layout.addWidget(self.update_type_service_choose)
        update_type_service_edit_layout = QVBoxLayout()
        update_type_service_edit_lable = QLabel('New name')
        self.update_type_service_edit = QLineEdit()
        update_type_service_edit_layout.addWidget(update_type_service_edit_lable)
        update_type_service_edit_layout.addWidget(self.update_type_service_edit)
        
        update_type_service_input_layout.addLayout(update_type_service_choose_layout)
        update_type_service_input_layout.addLayout(update_type_service_edit_layout)

        update_type_service_layout.addWidget(update_type_service_label)
        update_type_service_layout.addLayout(update_type_service_input_layout)
        update_type_service_layout.addWidget(update_type_service_button)
        update_type_service_frame.setLayout(update_type_service_layout)

        update_service_frame = QFrame()
        update_service_frame.setStyleSheet('''                    
            QFrame {
                border: 1px solid #ccc;
                font-size: 12pt;
                border-radius: 5px;
                background-color: #ffffff
            }
            QLabel {
                font-size: 12pt;
                border: none;
            }
            QLineEdit {
                border: 2px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
                                    min-width: 80px;
            }
            QComboBox {
                border: 2px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
                color: #333;
                background-color: #fff;
                selection-background-color: #e0e0e0;
            }
            QPushButton {
                background-color: #005bbd;
                border: 2px solid #005bbd;
                border-radius: 5px;
                color: white;
                text-align: center
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        ''')
        update_service_label = QLabel("Service table")
        update_service_layout = QVBoxLayout()
        update_service_button = QPushButton("Change")
        update_service_button.clicked.connect(self.update_service_table)
        update_service_input_layout = QHBoxLayout()
        update_service_type_service_choose_layout = QVBoxLayout()
        update_service_type_service_choose_label = QLabel("Type service")
        
        update_service_type_service_choose_layout.addWidget(update_service_type_service_choose_label)
        update_service_type_service_choose_layout.addWidget(self.update_service_type_service_choose)

        update_service_choose_layout = QVBoxLayout()
        update_service_choose_label = QLabel("Prev name")
        self.update_service_choose = QComboBox()
        self.update_contract_service_choose = QComboBox()
        self.update_service_choose.currentIndexChanged.connect(self.on_service_changed)
        try:
            conn = sqlite3.connect('app_files\\EGA_database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT servicename FROM service")
            servicenames = cursor.fetchall()
            for servicename in servicenames:
                self.update_service_choose.addItem(servicename[0])
                self.update_contract_service_choose.addItem(servicename[0])
            cursor.execute("SELECT typeservicename FROM service join typeservice using(typeserviceid) where servicename = ?", (self.update_service_choose.currentText(),))
            curent_typeservice = cursor.fetchone()[0]
            self.update_type_service_choose.setCurrentText(curent_typeservice)
            conn.close()
        except sqlite3.Error as e:
            print(f"Error: {str(e)}")
        update_service_choose_layout.addWidget(update_service_choose_label)
        update_service_choose_layout.addWidget(self.update_service_choose)

        update_service_edit_layout = QVBoxLayout()
        update_service_edit_label = QLabel("New name")
        self.update_service_edit = QLineEdit()
        update_service_edit_layout.addWidget(update_service_edit_label)
        update_service_edit_layout.addWidget(self.update_service_edit)

        update_service_input_layout.addLayout(update_service_choose_layout)
        update_service_input_layout.addLayout(update_service_type_service_choose_layout)
        update_service_input_layout.addLayout(update_service_edit_layout)
        
        update_service_layout.addWidget(update_service_label)
        update_service_layout.addLayout(update_service_input_layout)
        update_service_layout.addWidget(update_service_button)
        update_service_frame.setLayout(update_service_layout)

        line3 = QHBoxLayout()
        update_manager_frame = QFrame()
        update_manager_frame.setStyleSheet('''                    
            QFrame {
                border: 1px solid #ccc;
                font-size: 12pt;
                border-radius: 5px;
                background-color: #ffffff
            }
            QLabel {
                font-size: 12pt;
                border: none;
            }
            QLineEdit {
                border: 2px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
                                    min-width: 80px;
            }
            QComboBox {
                border: 2px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
                color: #333;
                background-color: #fff;
                selection-background-color: #e0e0e0;
            }
            QPushButton {
                background-color: #005bbd;
                border: 2px solid #005bbd;
                border-radius: 5px;
                color: white;
                text-align: center
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        ''')
        update_manager_label = QLabel("Manager table")
        update_manager_layout = QVBoxLayout()
        update_manager_input_layout = QHBoxLayout()
        update_manager_button = QPushButton("Change")
        update_manager_button.clicked.connect(self.update_manager_table)
        update_manager_choose_layout = QVBoxLayout()
        update_manager_choose_label = QLabel("Prev name")
        self.update_manager_choose = QComboBox()
        self.update_contract_manager_choose = QComboBox()
        try:
            conn = sqlite3.connect('app_files\\EGA_database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT managername FROM managers")
            managernames = cursor.fetchall()
            for managername in managernames:
                self.update_manager_choose.addItem(managername[0])
                self.update_contract_manager_choose.addItem(managername[0])
            conn.close()
        except sqlite3.Error as e:
            print(f"Error: {str(e)}")

        update_manager_choose_layout.addWidget(update_manager_choose_label)
        update_manager_choose_layout.addWidget(self.update_manager_choose)
        update_manager_name_edit_layout = QVBoxLayout()
        update_manager_name_edit_label = QLabel("New name")
        self.update_manager_name_edit = QLineEdit()
        update_manager_name_edit_layout.addWidget(update_manager_name_edit_label)
        update_manager_name_edit_layout.addWidget(self.update_manager_name_edit)
        update_manager_phone_edit_layout = QVBoxLayout()
        update_manager_phone_edit_label = QLabel("Phone")
        self.update_manager_phone_edit = QLineEdit()
        update_manager_phone_edit_layout.addWidget(update_manager_phone_edit_label)
        update_manager_phone_edit_layout.addWidget(self.update_manager_phone_edit)

        update_manager_input_layout.addLayout(update_manager_choose_layout)
        update_manager_input_layout.addLayout(update_manager_name_edit_layout)
        update_manager_input_layout.addLayout(update_manager_phone_edit_layout)

        update_manager_layout.addWidget(update_manager_label)
        update_manager_layout.addLayout(update_manager_input_layout)
        update_manager_layout.addWidget(update_manager_button)
        update_manager_frame.setLayout(update_manager_layout)

        update_contract_frame = QFrame()
        update_contract_frame.setStyleSheet('''                    
            QFrame {
                border: 1px solid #ccc;
                font-size: 12pt;
                border-radius: 5px;
                background-color: #ffffff
            }
            QLabel {
                font-size: 12pt;
                border: none;
            }
            QLineEdit {
                border: 2px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
                                    min-width: 80px;
            }
            QComboBox {
                border: 2px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
                color: #333;
                background-color: #fff;
                selection-background-color: #e0e0e0;
            }
            QPushButton {
                background-color: #005bbd;
                border: 2px solid #005bbd;
                border-radius: 5px;
                color: white;
                text-align: center
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        ''')
        update_contract_layout = QVBoxLayout()
        update_contract_label = QLabel("Contract Table")
        self.update_contract_button = QPushButton("Change")
        self.update_contract_button.clicked.connect(self.update_contract)
        update_contract_number_layout = QVBoxLayout()
        update_contract_number_label = QLabel("Number")
        self.update_contract_number_choose = QComboBox()
        self.update_contract_number_choose.currentIndexChanged.connect(self.on_contract_changed)
        try:
            conn = sqlite3.connect('app_files\\EGA_database.db')
            cursor = conn.cursor()
            cursor.execute("select contractid from contracts")
            contractids = cursor.fetchall()
            for contractid in contractids:
                self.update_contract_number_choose.addItem(str(contractid[0]))
            conn.close()
        except sqlite3.Error as e:
            print(f"Error: {str(e)}")
        update_contract_number_layout.addWidget(update_contract_number_label)
        update_contract_number_layout.addWidget(self.update_contract_number_choose)
        update_contract_company_layout = QVBoxLayout()
        update_contract_company_label = QLabel("company name")
        
        update_contract_company_layout.addWidget(update_contract_company_label)
        update_contract_company_layout.addWidget(self.update_contract_company_choose)
        update_contract_client_layout = QVBoxLayout()
        update_contract_client_label = QLabel("Client name")
        
        update_contract_client_layout.addWidget(update_contract_client_label)
        update_contract_client_layout.addWidget(self.update_contract_client_choose)
        update_contract_type_service_layout = QVBoxLayout()
        update_contract_type_service_label = QLabel("Type service name")
        
        update_contract_type_service_layout.addWidget(update_contract_type_service_label)
        update_contract_type_service_layout.addWidget(self.update_contract_type_service_choose)
        update_contract_service_layout = QVBoxLayout()
        update_contract_service_label = QLabel("Service name")
        
        update_contract_service_layout.addWidget(update_contract_service_label)
        update_contract_service_layout.addWidget(self.update_contract_service_choose)
        update_contract_manager_layout = QVBoxLayout()
        update_contract_manager_label = QLabel("Manager name")
        
        update_contract_manager_layout.addWidget(update_contract_manager_label)
        update_contract_manager_layout.addWidget(self.update_contract_manager_choose)
        update_contract_signing_date_layout = QVBoxLayout()
        update_contract_signing_date_label = QLabel("Signing date")
        
        self.update_contract_signing_date_choose.setCalendarPopup(True)
        self.update_contract_signing_date_choose.setDisplayFormat("yyyy-MM-dd")
        update_contract_signing_date_layout.addWidget(update_contract_signing_date_label)
        update_contract_signing_date_layout.addWidget(self.update_contract_signing_date_choose)
        update_contract_start_date_layout = QVBoxLayout()
        update_contract_start_date_label = QLabel("Start date")
        
        self.update_contract_start_date_choose.setCalendarPopup(True)
        self.update_contract_start_date_choose.setDisplayFormat("yyyy-MM-dd")

        update_contract_start_date_layout.addWidget(update_contract_start_date_label)
        update_contract_start_date_layout.addWidget(self.update_contract_start_date_choose)
        update_contract_end_date_layout = QVBoxLayout()
        update_contract_end_date_label = QLabel("End date")
        
        self.update_contract_end_date_choose.setCalendarPopup(True)
        self.update_contract_end_date_choose.setDisplayFormat("yyyy-MM-dd")
        update_contract_end_date_layout.addWidget(update_contract_end_date_label)
        update_contract_end_date_layout.addWidget(self.update_contract_end_date_choose)
        update_contract_pay_date_layout = QVBoxLayout()
        update_contract_pay_date_label = QLabel("Pay date")
        
        self.update_contract_pay_date_choose.setCalendarPopup(True)
        self.update_contract_pay_date_choose.setMinimumWidth(int(width/3)-20)
        self.update_contract_pay_date_choose.setDisplayFormat("yyyy-MM-dd")
        update_contract_pay_date_layout.addWidget(update_contract_pay_date_label)
        update_contract_pay_date_layout.addWidget(self.update_contract_pay_date_choose)
        update_contract_price_layout = QVBoxLayout()
        update_contract_price_label = QLabel("Price")
        
        update_contract_price_layout.addWidget(update_contract_price_label)
        update_contract_price_layout.addWidget(self.update_contract_price_choose)

        contract_line1 = QHBoxLayout()
        contract_line1.addLayout(update_contract_number_layout)
        contract_line1.addLayout(update_contract_company_layout)
        contract_line1.addLayout(update_contract_client_layout)
        contract_line2 = QHBoxLayout()
        contract_line2.addLayout(update_contract_type_service_layout)
        contract_line2.addLayout(update_contract_service_layout)
        contract_line2.addLayout(update_contract_manager_layout)
        contract_line3 = QHBoxLayout()
        contract_line3.addLayout(update_contract_signing_date_layout)
        contract_line3.addLayout(update_contract_start_date_layout)
        contract_line3.addLayout(update_contract_end_date_layout)
        contract_line4 = QHBoxLayout()
        contract_line4.addLayout(update_contract_pay_date_layout)
        contract_line4.addLayout(update_contract_price_layout)

        update_contract_layout.addWidget(update_contract_label)
        update_contract_layout.addLayout(contract_line1)
        update_contract_layout.addLayout(contract_line2)
        update_contract_layout.addLayout(contract_line3)
        update_contract_layout.addLayout(contract_line4)
        update_contract_layout.addWidget(self.update_contract_button)
        update_contract_frame.setLayout(update_contract_layout)

        line2.addWidget(update_type_service_frame)
        line2.addWidget(update_service_frame)
        line3.addWidget(update_manager_frame)


        update_main_layout.addLayout(line1)
        update_main_layout.addLayout(line2)
        update_main_layout.addLayout(line3)

        update_main_layout.addWidget(update_contract_frame)

        self.update_data_window.setLayout(update_main_layout)
        self.update_data_window.show()
    def update_contract(self):
        contract_number = self.update_contract_number_choose.currentText()
        contract_company_name = self.update_contract_company_choose.currentText()
        contract_client_name = self.update_contract_client_choose.currentText()
        contract_type_service_name = self.update_contract_type_service_choose.currentText()
        contract_service_name = self.update_contract_service_choose.currentText()
        contract_manager_name = self.update_contract_manager_choose.currentText()
        contract_signing_date = self.update_contract_signing_date_choose.text()
        contract_start_date = self.update_contract_start_date_choose.text()
        contract_end_date = self.update_contract_end_date_choose.text()
        contract_price_date = self.update_contract_pay_date_choose.text()
        contract_price  = self.update_contract_price_choose.text()
        try:
            conn = sqlite3.connect('app_files\\EGA_database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM company where companyname = ?", (contract_company_name,))
            contract_company_id = cursor.fetchone()[0]
            cursor.execute("SELECT * FROM clients where clientname = ?", (contract_client_name,))
            contract_client_id = cursor.fetchone()[0]
            cursor.execute("SELECT * FROM typeservice where typeservicename = ?", (contract_type_service_name,))
            contract_type_service_id = cursor.fetchone()[0]
            cursor.execute("SELECT * FROM service where servicename = ?", (contract_service_name,))
            contract_service_id = cursor.fetchone()[0]
            cursor.execute("SELECT * FROM managers where managername = ?", (contract_manager_name,))                
            contract_manager_id = cursor.fetchone()[0]

            query = """UPDATE Contracts 
            SET companyid = ?, clientid = ?, typeserviceid = ?, serviceid = ?, signingdate = ?, startdate = ?, enddate = ?, paydate = ?, price = ?, managerid = ?  WHERE contractid = ?"""
            cursor.execute(query, (contract_company_id, contract_client_id, contract_type_service_id, contract_service_id, contract_signing_date, contract_start_date, contract_end_date, contract_price_date, contract_price, contract_manager_id, contract_number))
            conn.commit()  # Сохранение изменений
            conn.close()
            QMessageBox.information(self.update_data_window, 'Success', 'Contract updated successfully.')
        except sqlite3.Error as e:
            QMessageBox.warning(self.update_data_window, 'Query execution error', f'Error: {str(e)}')






    def update_manager_table(self):
        prev_manager_name = self.update_manager_choose.currentText()
        new_manager_name  = self.update_manager_name_edit.text()
        manager_phone = self.update_manager_phone_edit.text()
        if manager_phone != '' and new_manager_name != '':
            try:
                conn = sqlite3.connect('app_files\\EGA_database.db')
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM managers where managername = ?", (prev_manager_name,))
                current_manager_info = cursor.fetchone()
            except sqlite3.Error as e:
                print(f"Error: {str(e)}")
            if new_manager_name == '':
                new_manager_name = prev_manager_name
            if manager_phone == '':
                manager_phone = current_manager_info[2]
            try:
                conn = sqlite3.connect('app_files\\EGA_database.db')
                cursor = conn.cursor()
                query = """UPDATE Managers SET managername = ?, managerphone = ? WHERE managername = ?"""
                cursor.execute(query, (new_manager_name, manager_phone, prev_manager_name))
                conn.commit()  # Сохранение изменений
                conn.close()  # Закрытие соединения с базой данных
                QMessageBox.information(self.update_data_window, 'Success', 'Manager updated successfully.')
                self.update_manager_name_edit.clear()
                self.update_manager_phone_edit.clear()
            except sqlite3.Error as e:
                QMessageBox.warning(self.update_data_window, 'Query execution error', f'Error: {str(e)}')

        

    def update_service_table(self):
        prev_service_name = self.update_service_choose.currentText()
        service_type_service_name = self.update_service_type_service_choose.currentText()
        new_service_name = self.update_service_edit.text()
        if new_service_name == '':
            new_service_name = prev_service_name
        try:
            conn = sqlite3.connect('app_files\\EGA_database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM typeservice where typeservicename = ?", (service_type_service_name,))
            new_typeservice_id = cursor.fetchone()[0]
            
            query = """UPDATE service SET typeserviceid = ?, servicename = ? WHERE servicename = ?"""
            cursor.execute(query, (new_typeservice_id, new_service_name, prev_service_name))

            conn.commit()  # Сохранение изменений
            conn.close()  # Закрытие соединения с базой данных
            QMessageBox.information(self.update_data_window, 'Success', 'Service updated successfully.')
            self.update_service_edit.clear()
            # self.update_client_phone.close()
        except sqlite3.Error as e:
            QMessageBox.warning(self.update_data_window, 'Query execution error', f'Error: {str(e)}')

        
    def update_type_service_table(self):
        prev_type_service_name = self.update_type_service_choose.currentText()
        new_typeservice_name = self.update_type_service_edit.text()
        if new_typeservice_name != '':
            try:
                conn = sqlite3.connect('app_files\\EGA_database.db')
                cursor = conn.cursor()
                query = "UPDATE typeservice SET typeservicename = ? WHERE typeservicename = ?"
                cursor.execute(query, (new_typeservice_name, prev_type_service_name))
                conn.commit()  # Сохранение изменений
                conn.close()  # Закрытие соединения с базой данных
                QMessageBox.information(self.update_data_window, 'Success', 'Type service updated successfully.')
                self.update_type_service_edit.clear()
            except sqlite3.Error as e:
                QMessageBox.warning(self.update_data_window, 'Query execution error', f'Error: {str(e)}')


    def update_client_table(self):
        prev_client_name = self.update_client_name_choose.currentText()
        client_company_name = self.update_client_company_choose.currentText()
        client_new_name = self.update_client_new_name_input.text()
        client_city = self.update_client_city.text()
        client_address = self.update_client_address.text()
        client_phone = self.update_client_phone.text()
        try:
            conn = sqlite3.connect('app_files\\EGA_database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clients where clientname = ?", (prev_client_name,))
            current_client_info = cursor.fetchone()

            print(current_client_info)
            
        except sqlite3.Error as e:
            print(f"Error: {str(e)}")
        if client_new_name == '':
            client_new_name = current_client_info[2]
        if client_city == '':
            client_city = current_client_info[3]
        if client_address == '':
            client_address = current_client_info[4]
        if client_phone == '':
            client_phone = current_client_info[5]
        try:
            cursor.execute("SELECT * FROM company where companyname = ?", (client_company_name,))
            new_company_id = cursor.fetchone()[0]
            conn = sqlite3.connect('app_files\\EGA_database.db')
            cursor = conn.cursor()
            query = """UPDATE Clients SET ClientName = ?, CompanyID = ?, City = ?, Address = ?, ClientPhone = ? WHERE ClientName = ?"""
            cursor.execute(query, (client_new_name, new_company_id, client_city, client_address, client_phone, prev_client_name))

            conn.commit()  # Сохранение изменений
            conn.close()  # Закрытие соединения с базой данных
            QMessageBox.information(self.update_data_window, 'Success', 'Client updated successfully.')
            self.update_client_new_name_input.clear()
            self.update_client_city.clear()
            self.update_client_address.clear()
            self.update_client_new_name_input.clear()
            # self.update_client_phone.close()
        except sqlite3.Error as e:
            QMessageBox.warning(self.update_data_window, 'Query execution error', f'Error: {str(e)}')

    def update_company_table(self):
        """
        Function to update the name of a company in the database.

        Retrieves the new and previous company names from input fields.
        Updates the company name in the database if a new name is provided.

        Args:
        - self: Reference to the current instance of the class.

        Returns:
        - None
        """
        # Get the new and previous company names from input fields and dropdown list
        new_company_name = self.update_company_edit.text()
        prev_company_name = self.update_company_choose.currentText()
        if self.update_company_edit.text() != '':
            try:
                conn = sqlite3.connect('app_files\\EGA_database.db')
                cursor = conn.cursor()
                query = "UPDATE Company SET companyname = ? WHERE companyname = ?"
                cursor.execute(query, (new_company_name, prev_company_name))

                conn.commit()  
                conn.close()  
                QMessageBox.information(self.update_data_window, 'Success', 'Company updated successfully.')
                self.update_company_edit.clear()
                # self.update_data_window.close()
            except sqlite3.Error as e:
                QMessageBox.warning(self.update_data_window, 'Query execution error', f'Error: {str(e)}')

    def on_client_changed(self, index):
        """
        Event handler triggered when the selected client changes.

        Retrieves the currently selected client from the combobox.
        Calls the 'set_client_company' function to update the associated company accordingly.

        Args:
        - self: Reference to the current instance of the class.
        - index: The index of the selected item in the combobox.

        Returns:
        - None
        """
        selected_client = self.update_client_name_choose.currentText()
        self.set_client_company(selected_client)


    def on_service_changed(self, index):
        """
        Event handler triggered when the selected service changes.

        Retrieves the currently selected service from the combobox.
        Calls the 'set_service_typeservice' function to update the associated type of service accordingly.

        Args:
        - self: Reference to the current instance of the class.
        - index: The index of the selected item in the combobox.

        Returns:
        - None
        """
        selected_service = self.update_service_choose.currentText()
        self.set_service_typeservice(selected_service)
    def on_contract_changed(self, index):
        """
        Event handler triggered when the selected contract changes.

        Retrieves the currently selected contract number from the combobox.
        Calls the 'set_contract_value' function to update the associated contract value accordingly.

        Args:
        - self: Reference to the current instance of the class.
        - index: The index of the selected item in the combobox.

        Returns:
        - None
        """
        selected_contract = int(self.update_contract_number_choose.currentText())
        self.set_contract_value(selected_contract)

    def set_contract_value(self, selected_contract):
        try:
            conn = sqlite3.connect('app_files\\EGA_database.db')
            cursor = conn.cursor()

            cursor.execute('''SELECT contractid, CompanyName, ClientName, TypeServiceName, ServiceName, SigningDate, StartDate, EndDate, PayDate, Price, ManagerName 
FROM Contracts 
join company using(companyid)
join clients using(clientid)
join typeservice using(typeserviceid)
join service using(serviceid)
join managers using(managerid) where contractid = ?''', (selected_contract,))
            curent_contract = cursor.fetchall()
            current_company = curent_contract[0][1]
            current_client = curent_contract[0][2]
            current_typeservice = curent_contract[0][3]
            current_service = curent_contract[0][4]
            current_signingdate = curent_contract[0][5]
            curent_startdate = curent_contract[0][6]
            current_enddate = curent_contract[0][7]
            current_paydate = curent_contract[0][8]
            current_price =  curent_contract[0][9]
            current_manager =  curent_contract[0][10]

            self.update_contract_company_choose.setCurrentText(current_company)
            self.update_contract_client_choose.setCurrentText(current_client)
            self.update_contract_type_service_choose.setCurrentText(current_typeservice)
            self.update_contract_service_choose.setCurrentText(current_service)
            self.update_contract_manager_choose.setCurrentText(current_manager)
            self.update_contract_signing_date_choose.setDate(QDate.fromString(current_signingdate, "yyyy-MM-dd"))
            self.update_contract_start_date_choose.setDate(QDate.fromString(curent_startdate, "yyyy-MM-dd"))
            self.update_contract_end_date_choose.setDate(QDate.fromString(current_enddate, "yyyy-MM-dd"))
            self.update_contract_pay_date_choose.setDate(QDate.fromString(current_paydate, "yyyy-MM-dd"))
            # self.update_contract_price_choose.setText(str(current_price))


            print(curent_contract)
            conn.close()
        except sqlite3.Error as e:
            print(f"Error: {str(e)}")
    def set_client_company(self, selected_client):
        """
        Function to set the 'currentText' of a widget based on the selected client.

        Retrieves the company associated with the selected client.
        Sets the 'currentText' of a specific widget to the retrieved company.

        Args:
        - self: Reference to the current instance of the class.
        - selected_client: The name of the selected client.

        Returns:
        - None
        """
        try:
            conn = sqlite3.connect('app_files\\EGA_database.db')
            cursor = conn.cursor()
            # Fetch the company associated with the selected client
            cursor.execute("SELECT companyname FROM Company join clients using(companyid) where clientname = ?", (selected_client,))
            curent_company = cursor.fetchone()[0]
            # Set the 'currentText' of the specified widget to the retrieved company
            self.update_client_company_choose.setCurrentText(curent_company)
            conn.close()
        except sqlite3.Error as e:
            print(f"Error: {str(e)}")

    def set_service_typeservice(self, selected_service):
        """
        Function to set the 'currentText' of a widget based on the selected service.

        Retrieves the type of service associated with the selected service.
        Sets the 'currentText' of a specific widget to the retrieved type of service.

        Args:
        - self: Reference to the current instance of the class.
        - selected_service: The name of the selected service.

        Returns:
        - None
        """
        try:
            conn = sqlite3.connect('app_files\\EGA_database.db')
            cursor = conn.cursor()
            # Fetch the type of service associated with the selected service
            cursor.execute("SELECT typeservicename FROM typeservice join service using(typeserviceid) where servicename = ?", (selected_service,))
            curent_typeservice = cursor.fetchone()[0]
            # Set the 'currentText' of the specified widget to the retrieved type of service
            self.update_service_type_service_choose.setCurrentText(curent_typeservice)
            conn.close()
        except sqlite3.Error as e:
            print(f"Error: {str(e)}")

    def add_data_screen(self):
        self.add_data_window = QWidget()
        self.add_data_window.setWindowTitle('Add Data')
        # Создаем объект QDesktopWidget для получения информации об экране пользователя
        desktop = QDesktopWidget()

        # Получаем размеры главного экрана пользователя
        screen_size = desktop.screenGeometry()

        # Ширина и высота главного экрана пользователя
        width = screen_size.width()
        height = screen_size.height()
        self.add_data_window.setFixedWidth(width)
        
        
        
        # main add data window layout
        main_layout = QVBoxLayout()

        # init  layout of adding data
        add_data_in_table = QHBoxLayout()
        add_data_in_table2 = QHBoxLayout()

        # company_widget.setStyleSheet("border: 1px solid #ccc; border-radius: 4px;")
        # init of box clumns
        company_frame = QFrame()
        company_layout = QVBoxLayout(company_frame)
        company_frame.setStyleSheet('''                    
            QFrame {
                border: 1px solid #ccc;
                font-size: 12pt;
                border-radius: 5px;
                background-color: #ffffff
            }
            QLabel {
                font-size: 12pt;
                border: none;
            }
            QLineEdit {
                border: 2px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
                                    min-width: 80px;
            }
            QComboBox {
                border: 2px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
                color: #333;
                background-color: #fff;
                selection-background-color: #e0e0e0;
            }
            QPushButton {
                background-color: #005bbd;
                border: 2px solid #005bbd;
                border-radius: 5px;
                color: white;
                text-align: center
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        ''')
        
        client_frame = QFrame()
        client_layout = QVBoxLayout(client_frame)
        client_frame.setStyleSheet('''                    
            QFrame {
                border: 1px solid #ccc;
                font-size: 12pt;
                border-radius: 5px;
                background-color: #ffffff
            }
            QLabel {
                font-size: 12pt;
                border: none;
            }
            QLineEdit {
                border: 2px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
                                   min-width: 80px;
            }
            QComboBox {
                border: 2px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
                color: #333;
                background-color: #fff;
                selection-background-color: #e0e0e0;
            }
            QPushButton {
                background-color: #005bbd;
                border: 2px solid #005bbd;
                border-radius: 5px;
                color: white;
                text-align: center
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        ''')

        type_service_frame = QFrame()
        type_service_layout = QVBoxLayout(type_service_frame)
        type_service_frame.setStyleSheet('''                    
            QFrame {
                border: 1px solid #ccc;
                font-size: 12pt;
                border-radius: 5px;
                background-color: #ffffff;
                
            }
            QLabel {
                font-size: 12pt;
                border: none;

            }
            QLineEdit {
                border: 2px solid #ccc;
                border-radius: 4px;
                font-size: 14px;

            }
            QComboBox {
                border: 2px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
                color: #333;
                background-color: #fff;
                selection-background-color: #e0e0e0;
            }
            QPushButton {
                background-color: #005bbd;
                border: 2px solid #005bbd;
                border-radius: 5px;
                color: white;
                text-align: center
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        ''')

        service_frame = QFrame()
        service_layout = QVBoxLayout(service_frame)
        service_frame.setStyleSheet('''                    
            QFrame {
                border: 1px solid #ccc;
                font-size: 12pt;
                border-radius: 5px;
                background-color: #ffffff
            }
            QLabel {
                font-size: 12pt;
                border: none;
            }
            QLineEdit {
                border: 2px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
                                    min-width: 80px;
            }
            QComboBox {
                border: 2px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
                color: #333;
                background-color: #fff;
                selection-background-color: #e0e0e0;
            }
            QPushButton {
                background-color: #005bbd;
                border: 2px solid #005bbd;
                border-radius: 5px;
                color: white;
                text-align: center
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        ''')

        manager_frame = QFrame()
        manager_layout = QVBoxLayout(manager_frame)
        manager_frame.setStyleSheet('''                    
            QFrame {
                border: 1px solid #ccc;
                font-size: 12pt;
                border-radius: 5px;
                background-color: #ffffff
            }
            QLabel {
                font-size: 12pt;
                border: none;
            }
            QLineEdit {
                border: 2px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
                                    min-width: 100px;
            }
            QComboBox {
                border: 2px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
                color: #333;
                background-color: #fff;
                selection-background-color: #e0e0e0;
            }
            QPushButton {
                background-color: #005bbd;
                border: 2px solid #005bbd;
                border-radius: 5px;
                color: white;
                text-align: center
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        ''')

        # Add column "Company Table"
        company_label = QLabel('Company Table')
        company_label.setAlignment(Qt.AlignCenter)
        company_input_label = QLabel('Name')
        self.company_input = QLineEdit()
        company_add_button = QPushButton('Add')
        company_add_button.clicked.connect(self.add_company)

        company_layout.addWidget(company_label)
        company_layout.addWidget(company_input_label)
        company_layout.addWidget(self.company_input)
        company_layout.addWidget(company_add_button)

        # add column "Client Table"
        client_label = QLabel('Сlient Table')
        client_label.setAlignment(Qt.AlignCenter)
        client_input_layout = QHBoxLayout()

        client_company_choose_layout = QVBoxLayout()
        client_company_choose_label = QLabel("Company")
        self.client_company_choose = QComboBox()
        try:
            conn = sqlite3.connect('app_files\\EGA_database.db')
            cursor = conn.cursor()

            cursor.execute("SELECT DISTINCT companyname FROM Company")
            companies = cursor.fetchall()

            for company in companies:
                self.client_company_choose.addItem(company[0])

            conn.close()
        except sqlite3.Error as e:
            print(f"Error: {str(e)}")
        
        client_company_choose_layout.addWidget(client_company_choose_label)
        client_company_choose_layout.addWidget(self.client_company_choose)

        client_name_input_layout = QVBoxLayout()
        client_name_input_label = QLabel("Name")
        self.client_name_input = QLineEdit()
        client_name_input_layout.addWidget(client_name_input_label)
        client_name_input_layout.addWidget(self.client_name_input)

        client_city_input_layout = QVBoxLayout()
        client_city_input_label = QLabel("City")
        self.client_city_input = QLineEdit()
        client_city_input_layout.addWidget(client_city_input_label)
        client_city_input_layout.addWidget(self.client_city_input)
        
        client_address_input_layout = QVBoxLayout()
        client_address_input_label = QLabel("Address")
        self.client_address_input = QLineEdit()
        client_address_input_layout.addWidget(client_address_input_label)
        client_address_input_layout.addWidget(self.client_address_input)
        
        client_phone_input_layout = QVBoxLayout()
        client_phone_input_label = QLabel("Phone")
        self.client_phone_input = QLineEdit()
        client_phone_input_layout.addWidget(client_phone_input_label)
        client_phone_input_layout.addWidget(self.client_phone_input)

        

        client_input_layout.addLayout(client_company_choose_layout)
        client_input_layout.addLayout(client_name_input_layout)
        client_input_layout.addLayout(client_city_input_layout)
        client_input_layout.addLayout(client_address_input_layout)
        client_input_layout.addLayout(client_phone_input_layout)

        client_add_button = QPushButton('Add')
        client_add_button.clicked.connect(self.add_client)

        client_layout.addWidget(client_label)
        client_layout.addLayout(client_input_layout)
        client_layout.addWidget(client_add_button)

        # Add column "TypeService Table"
        type_service_label = QLabel('TypeService Table')
        type_service_label.setAlignment(Qt.AlignCenter)
        type_service_input_label = QLabel('Name')
        self.type_service_input = QLineEdit()
        type_service_add_button = QPushButton('Add')
        type_service_add_button.clicked.connect(self.add_type_service)

        type_service_layout.addWidget(type_service_label)
        type_service_layout.addWidget(type_service_input_label)
        type_service_layout.addWidget(self.type_service_input)
        type_service_layout.addWidget(type_service_add_button)

        # Add column "Service Table"
        service_label = QLabel('Service Table')
        service_label.setAlignment(Qt.AlignCenter)
        service_input_layout = QHBoxLayout()

        choose_type_service_layout = QVBoxLayout()
        choose_type_service_label = QLabel('Type Service')
        self.choose_type_service = QComboBox()
        try:
            conn = sqlite3.connect('app_files\\EGA_database.db')
            cursor = conn.cursor()

            cursor.execute("SELECT DISTINCT typeservicename FROM typeservice")
            typeservices = cursor.fetchall()

            for item in typeservices:
                self.choose_type_service.addItem(item[0])

            conn.close()
        except sqlite3.Error as e:
            print(f"Error: {str(e)}")
        choose_type_service_layout.addWidget(choose_type_service_label)
        choose_type_service_layout.addWidget(self.choose_type_service)

        service_name_layout = QVBoxLayout()
        service_name_label = QLabel('Name')
        self.service_name_input = QLineEdit()
        service_name_layout.addWidget(service_name_label)
        service_name_layout.addWidget(self.service_name_input)
        
        service_add_button = QPushButton('Add')
        service_add_button.clicked.connect(self.add_service)

        service_input_layout.addLayout(choose_type_service_layout)
        service_input_layout.addLayout(service_name_layout)

        service_layout.addWidget(service_label)
        service_layout.addLayout(service_input_layout)
        service_layout.addWidget(service_add_button)

        

        manager_label = QLabel("Manager Table")
        manager_label.setAlignment(Qt.AlignCenter)
        manager_input_layout = QHBoxLayout()

        manager_name_layout = QVBoxLayout()
        manager_name_label = QLabel("Name")
        self.manager_name_input = QLineEdit()
        manager_name_layout.addWidget(manager_name_label)
        manager_name_layout.addWidget(self.manager_name_input)

        manager_phone_layout = QVBoxLayout()
        manager_phone_label = QLabel("Phone")
        self.manager_phone_input = QLineEdit()
        manager_phone_layout.addWidget(manager_phone_label)
        manager_phone_layout.addWidget(self.manager_phone_input)

        manager_input_layout.addLayout(manager_name_layout)
        manager_input_layout.addLayout(manager_phone_layout)

        manager_add_button = QPushButton('Add')
        manager_add_button.clicked.connect(self.add_manager)

        manager_layout.addWidget(manager_label)
        manager_layout.addLayout(manager_input_layout)
        manager_layout.addWidget(manager_add_button)

        company_frame.setLayout(company_layout)
        client_frame.setLayout(client_layout)
        type_service_frame.setLayout(type_service_layout)
        service_frame.setLayout(service_layout)
        manager_frame.setLayout(manager_layout)

        add_data_in_table.addWidget(company_frame)
        add_data_in_table.addWidget(client_frame)
        
        add_data_in_table2.addWidget(type_service_frame)
        add_data_in_table2.addWidget(service_frame)
        add_data_in_table2.addWidget(manager_frame)
        
        add_data_in_table.setSpacing(10)
        add_data_in_table2.setSpacing(10)

        add_data_in_contract = QVBoxLayout()
        contract_frame = QFrame()
        contract_frame.setStyleSheet('''                    
            QFrame {
                border: 1px solid #ccc;
                font-size: 8pt;
                border-radius: 5px;
                background-color: #ffffff
            }
            QLabel {
                height: 20px;
                font-size: 12pt;
                border: none;
            }
            QLineEdit {
                border: 2px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
                height: 20px;
                min-width: 100px;
            }
            QComboBox {
                border: 2px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
                color: #333;
                background-color: #fff;
                selection-background-color: #e0e0e0;
                                    
            }
            QPushButton {
                background-color: #005bbd;
                border: 2px solid #005bbd;
                border-radius: 5px;
                color: white;
                text-align: center;
                                     min-width: 80px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        ''')
        contract_layout = QVBoxLayout(contract_frame)
        contract_label = QLabel('Contract Table')
        contract_label.setAlignment(Qt.AlignCenter)
        contract_input_layout = QHBoxLayout()

        contract_company_layout = QVBoxLayout()
        contract_company_label = QLabel("Company")
        self.contract_company_choose = QComboBox()
        try:
            conn = sqlite3.connect('app_files\\EGA_database.db')
            cursor = conn.cursor()

            cursor.execute("SELECT DISTINCT companyname FROM Company order by companyname asc")
            companies = cursor.fetchall()

            for company in companies:
                self.contract_company_choose.addItem(company[0])

            conn.close()
        except sqlite3.Error as e:
            print(f"Error: {str(e)}")
        contract_company_layout.addWidget(contract_company_label)
        contract_company_layout.addWidget(self.contract_company_choose)
        contract_company_layout.addSpacing(40)

        contract_client_layout = QVBoxLayout()
        contract_client_label = QLabel("Client")
        self.contract_client_choose = QComboBox()
        try:
            conn = sqlite3.connect('app_files\\EGA_database.db')
            cursor = conn.cursor()

            cursor.execute("SELECT DISTINCT clientname FROM clients order by clientname asc")
            clients = cursor.fetchall()

            for client in clients:
                self.contract_client_choose.addItem(client[0])

            conn.close()
        except sqlite3.Error as e:
            print(f"Error: {str(e)}")
        contract_client_layout.addWidget(contract_client_label)
        contract_client_layout.addWidget(self.contract_client_choose)
        contract_client_layout.addSpacing(40)

        contract_type_service_layout = QVBoxLayout()
        contract_type_service_label = QLabel("Type service")
        self.contract_type_service_choose = QComboBox()
        try:
            conn = sqlite3.connect('app_files\\EGA_database.db')
            cursor = conn.cursor()

            cursor.execute("SELECT DISTINCT typeservicename FROM typeservice")
            typeservices = cursor.fetchall()

            for typeservice in typeservices:
                self.contract_type_service_choose.addItem(typeservice[0])

            conn.close()
        except sqlite3.Error as e:
            print(f"Error: {str(e)}")
        contract_company_layout.addWidget(contract_type_service_label)
        contract_company_layout.addWidget(self.contract_type_service_choose)
        contract_company_layout.addSpacing(40)

        contract_service_layout = QVBoxLayout()
        contract_service_label = QLabel("Service")
        self.contract_service_choose = QComboBox()
        try:
            conn = sqlite3.connect('app_files\\EGA_database.db')
            cursor = conn.cursor()

            cursor.execute("SELECT DISTINCT servicename FROM service")
            services = cursor.fetchall()

            for service in services:
                self.contract_service_choose.addItem(service[0])

            conn.close()
        except sqlite3.Error as e:
            print(f"Error: {str(e)}")
        contract_client_layout.addWidget(contract_service_label)
        contract_client_layout.addWidget(self.contract_service_choose)
        contract_client_layout.addSpacing(40)

        contract_price_layout = QVBoxLayout()
        contract_price_label = QLabel('Price')
        self.contract_price_input = QLineEdit()
        contract_price_layout.addWidget(contract_price_label)
        contract_price_layout.addWidget(self.contract_price_input)
        contract_price_layout.addSpacing(40)

        contract_manager_label = QLabel('Manager')
        self.contract_manager_choose = QComboBox()
        try:
            conn = sqlite3.connect('app_files\\EGA_database.db')
            cursor = conn.cursor()

            cursor.execute("SELECT DISTINCT managername FROM managers order by managername asc")
            managers = cursor.fetchall()

            for manager in managers:
                self.contract_manager_choose.addItem(manager[0])

            conn.close()
        except sqlite3.Error as e:
            print(f"Error: {str(e)}")
        contract_price_layout.addWidget(contract_manager_label)
        contract_price_layout.addWidget(self.contract_manager_choose)
        contract_price_layout.addSpacing(40)


        contract_signing_date_layout = QVBoxLayout()
        contract_signing_date_label = QLabel("Signing date")
        self.contract_signing_date = QCalendarWidget()
        self.contract_signing_date.setGridVisible(False)
        contract_signing_date_layout.addWidget(contract_signing_date_label)
        contract_signing_date_layout.addWidget(self.contract_signing_date)

        contract_start_date_layout = QVBoxLayout()
        contract_start_date_label = QLabel("Start date")
        self.contract_start_date = QCalendarWidget()
        self.contract_start_date.setGridVisible(False)
        contract_start_date_layout.addWidget(contract_start_date_label)
        contract_start_date_layout.addWidget(self.contract_start_date)

        contract_end_date_layout = QVBoxLayout()
        contract_end_date_label = QLabel("End date")
        self.contract_end_date = QCalendarWidget()
        self.contract_end_date.setGridVisible(False)
        contract_end_date_layout.addWidget(contract_end_date_label)
        contract_end_date_layout.addWidget(self.contract_end_date)


        contract_price_date_layout = QVBoxLayout()
        contract_price_date_label = QLabel("Pay date")
        self.contract_price_date = QCalendarWidget()
        self.contract_price_date.setGridVisible(False)
        contract_price_date_layout.addWidget(contract_price_date_label)
        contract_price_date_layout.addWidget(self.contract_price_date)


        
        contract_add_button = QPushButton('Add')
        contract_add_button.clicked.connect(self.add_contract)

        contract_input_layout.addLayout(contract_company_layout)
        contract_input_layout.addLayout(contract_client_layout)
        # contract_input_layout.addLayout(contract_type_service_layout)
        # contract_input_layout.addLayout(contract_service_layout)
        contract_input_layout.addLayout(contract_price_layout)
        contract_input_layout.addLayout(contract_signing_date_layout)
        contract_input_layout.addLayout(contract_start_date_layout)
        contract_input_layout.addLayout(contract_end_date_layout)
        contract_input_layout.addLayout(contract_price_date_layout)

        
        contract_layout.addWidget(contract_label)
        contract_layout.addLayout(contract_input_layout)
        contract_layout.addWidget(contract_add_button)

        contract_frame.setLayout(contract_layout)
        add_data_in_contract.addWidget(contract_frame)


        main_layout.addLayout(add_data_in_table)
        main_layout.addLayout(add_data_in_table2)
        main_layout.addLayout(add_data_in_contract)

        
        self.add_data_window.setLayout(main_layout)
        
        self.add_data_window.show()


    def add_contract(self) -> None:
        """
        Function to add a new contract to the database.

        Retrieves contract details from input fields and date selectors.
        Validates price data and inserts the contract into the database.

        Args:
        - self: Reference to the current instance of the class.

        Returns:
        - None
        """

        # Get contract details and input data
        company_name = self.contract_company_choose.currentText()
        client_name = self.contract_client_choose.currentText()
        type_service_name = self.contract_type_service_choose.currentText()
        service_name = self.contract_service_choose.currentText()
        manager_name = self.contract_manager_choose.currentText()
        price_sum = self.contract_price_input.text()
        signing_date_str = self.contract_signing_date.selectedDate().toString("yyyy-MM-dd")

        start_date_str = self.contract_start_date.selectedDate().toString("yyyy-MM-dd")
        end_date_str = self.contract_end_date.selectedDate().toString("yyyy-MM-dd")
        pay_date_str = self.contract_price_date.selectedDate().toString("yyyy-MM-dd")
        # signing_date = datetime.strptime(signing_date_str, '%Y-%m-%d')
        

        if price_sum != '' and price_sum.isnumeric():
            conn = sqlite3.connect('app_files\\EGA_database.db')
            cursor = conn.cursor()

            # Fetch the maximum contract ID and increment it for the new contract ID
            cursor.execute("SELECT MAX(contractid) FROM contracts")
            max_contract_id = cursor.fetchone()[0]
            new_contract_id = max_contract_id + 1 if max_contract_id else 1
            # Fetch IDs related to company, client, type of service, service, and manager from their names
            cursor.execute("SELECT companyid FROM company WHERE companyname = ?", (company_name,))
            company_id = cursor.fetchone()[0]

            cursor.execute("SELECT clientid FROM clients WHERE clientname = ?", (client_name,))
            client_id = cursor.fetchone()[0]

            cursor.execute("SELECT typeserviceid FROM typeservice WHERE typeservicename = ?", (type_service_name,))
            typeservice_id = cursor.fetchone()[0]

            cursor.execute("SELECT serviceid FROM service WHERE servicename = ?", (service_name,))
            service_id = cursor.fetchone()[0]

            cursor.execute("SELECT managerid FROM managers WHERE managername = ?", (manager_name,))
            manager_id = cursor.fetchone()[0]
            
            # Insert the new contract into the database
            cursor.execute('''
                INSERT INTO Contracts (ContractID, CompanyID, ClientID, TypeServiceID, ServiceID, SigningDate, StartDate, EndDate, PayDate, Price, ManagerID)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (new_contract_id, company_id, client_id, typeservice_id, service_id, signing_date_str, start_date_str, end_date_str, pay_date_str, price_sum, manager_id))

            conn.commit()
            QMessageBox.information(self.sql_window, 'Success', 'Contract added successfully.')
            conn.close() 

        


    def add_company(self) -> None:
        """
        Function to add a new company to the database.

        Retrieves the company name from an input field.
        Checks if the company already exists in the database.
        If not, adds the company to the database and updates UI elements accordingly.

        Args:
        - self: Reference to the current instance of the class.

        Returns:
        - None
        """
        # Get the company name from the input field
        company_name = self.company_input.text()
        print(company_name)
        if company_name != '':
            try:
                conn = sqlite3.connect('app_files\\EGA_database.db')
                cursor = conn.cursor()
                
                # Check if the company already exists in the database
                cursor.execute("SELECT * FROM Company WHERE companyname = ?", (company_name,))
                existing_company = cursor.fetchone()

                if existing_company:
                    QMessageBox.warning(self.sql_window, 'Existing company', 'Company with this name already exists.')
                else:
                    cursor.execute("INSERT INTO Company (companyid, companyname) SELECT COALESCE(MAX(companyid), 0) + 1, ? FROM Company", (company_name,))
                    conn.commit()
                    self.client_company_choose.addItem(company_name)
                    self.contract_company_choose.addItem(company_name)
                    QMessageBox.information(self.sql_window, 'Success', 'Company added successfully.')

                conn.close()
            except sqlite3.Error as e:
                QMessageBox.warning(self.sql_window, 'Query execution error', f'Error: {str(e)}')

        # Clear the input field after processing
        self.company_input.clear()
        self.add_data_window.raise_()

    
    

    def add_client(self) -> None:
        """
        Function to add a new client to the database.

        Retrieves client details from input fields.
        Checks if the client already exists in the database.
        If not, adds the client to the database and updates UI elements accordingly.

        Args:
        - self: Reference to the current instance of the class.

        Returns:
        - None
        """

        # Get client details from input fields
        client_name = self.client_name_input.text()
        client_city = self.client_city_input.text()
        client_address = self.client_address_input.text()
        client_phone = self.client_phone_input.text()
        client_company_name = self.client_company_choose.currentText()

        if client_name != '' or client_city != '' or client_address != '' or client_phone != '':
            try:
                conn = sqlite3.connect('app_files\\EGA_database.db')
                cursor = conn.cursor()
                # Check if the client already exists in the database
                cursor.execute("SELECT * FROM Clients WHERE clientname = ?", (client_name,))
                existing_company = cursor.fetchone()
                if existing_company:
                    QMessageBox.warning(self.sql_window, 'Existing client', 'Client with this name already exists.')
                    conn.close()    
                else:
                    cursor.execute("SELECT MAX(clientid) FROM clients")
                    max_client_id = cursor.fetchone()[0]
                    print(max_client_id)
                    new_client_id = max_client_id + 1 if max_client_id else 1

                    cursor.execute("SELECT companyid FROM company WHERE companyname = ?", (client_company_name,))
                    company_id = cursor.fetchone()[0]
                    print(company_id)

                    cursor.execute("INSERT INTO clients (clientid, companyid, clientname, address, city, clientphone) VALUES (?, ?, ?, ?, ?, ?)",
                           (new_client_id, company_id, client_name, client_address, client_city, client_phone))
                    conn.commit()
                    self.contract_client_choose.addItem(client_name)
                    QMessageBox.information(self.sql_window, 'Success', 'Client added successfully.')
                    conn.close()    
            except sqlite3.Error as e:
                QMessageBox.warning(self, 'Query execution error', f'Error: {str(e)}')

        # Clear the input fields after processing
        self.client_name_input.clear()
        self.client_city_input.clear()
        self.client_address_input.clear()
        self.client_phone_input.clear()
        self.add_data_window.raise_()

    def add_service(self) -> None:
        """
        Function to add a new service to the database.

        Retrieves the service name and type of service from input fields.
        Checks if the service already exists in the database.
        If not, adds the service to the database and updates UI elements accordingly.

        Args:
        - self: Reference to the current instance of the class.

        Returns:
        - None
        """

        # Get the service name and type of service from input fields
        service_name = self.service_name_input.text()
        type_service_name = self.choose_type_service.currentText()
        
        if service_name != '':
            try:
                conn = sqlite3.connect('app_files\\EGA_database.db')
                cursor = conn.cursor()

                # Check if the service already exists in the database
                cursor.execute("SELECT * FROM service WHERE servicename = ?", (service_name,))
                existing_company = cursor.fetchone()
                if existing_company:
                    QMessageBox.warning(self.sql_window, 'Existing service', 'service with this name already exists.')
                    conn.close()  
                else:
                    # Fetch the maximum service ID and increment it for the new service ID
                    cursor.execute("SELECT MAX(serviceid) FROM service")
                    max_serviceid = cursor.fetchone()[0]
                    print(max_serviceid)
                    new_service_id = max_serviceid + 1 if max_serviceid else 1
                    # Get the type service ID associated with the selected type of service
                    cursor.execute("SELECT typeserviceid FROM typeservice WHERE typeservicename = ?", (type_service_name,))
                    type_service_id = cursor.fetchone()[0]
                    print(type_service_id)
                    # Insert the new service into the database
                    cursor.execute("INSERT INTO service (serviceid, typeserviceid, servicename) VALUES (?, ?, ?)",
                           (new_service_id, type_service_id, service_name))
                    conn.commit()
                    self.contract_service_choose.addItem(service_name)
                    QMessageBox.information(self.sql_window, 'Success', 'Service added successfully.')
                    conn.close() 
            except sqlite3.Error as e:
                QMessageBox.warning(self, 'Query execution error', f'Error: {str(e)}')

            self.service_name_input.clear()
            self.add_data_window.raise_()


    def add_type_service(self) -> None:
        """
        Function to add a new type of service to the database.

        Retrieves the type of service from the input field.
        Checks if the type of service already exists in the database.
        If not, adds the type of service to the database and updates UI accordingly.

        Args:
        - self: Reference to the current instance of the class.

        Returns:
        - None
        """

        # Get the type of service from the input field
        type_service = self.type_service_input.text()
        print(type_service)
        if type_service != '':
            try:
                conn = sqlite3.connect('app_files\\EGA_database.db')
                cursor = conn.cursor()

                # Check if the type of service already exists in the database
                cursor.execute("SELECT * FROM typeservice WHERE typeservicename = ?", (type_service,))
                existing_company = cursor.fetchone()
                if existing_company:
                    QMessageBox.warning(self.sql_window, 'Existing type service', 'Type service with this name already exists.')
                else:
                    cursor.execute("INSERT INTO typeservice (typeserviceid, typeservicename) SELECT COALESCE(MAX(typeserviceid), 0) + 1, ? FROM typeservice", (type_service,))
                    conn.commit()
                    self.contract_service_choose.addItem(type_service)
                    QMessageBox.information(self.sql_window, 'Success', 'Type service added successfully.')
                    self.choose_type_service.addItem(type_service)

                conn.close()
            except sqlite3.Error as e:
                QMessageBox.warning(self.sql_window, 'Query execution error', f'Error: {str(e)}')
        # Clear the input field after processing
        self.type_service_input.clear()
        self.add_data_window.raise_()

    def add_manager(self) -> None:
        """
        Function to add a new manager to the database.

        Retrieves manager name and phone number from input fields.
        Checks if the manager already exists in the database. If not, adds the manager to the database and updates UI accordingly.

        Args:
        - self: Reference to the current instance of the class.

        Returns:
        - None

        Raises:
        - sqlite3.Error: Raised if there's an error during database operations.
        """

        # Retrieve manager name and phone number from input fields
        manager_name = self.manager_name_input.text()
        manager_phone = self.manager_phone_input.text()
        # Check if manager name or phone is provided
        if manager_name != '' or manager_phone != '':
            try:
                conn = sqlite3.connect('app_files\\EGA_database.db')
                cursor = conn.cursor()
                # Check if manager with the same name already exists
                cursor.execute("SELECT * FROM Managers WHERE managername = ?", (manager_name,))
                existing_manager = cursor.fetchone()

                if existing_manager:
                    QMessageBox.warning(self.sql_window, 'Existing manager', 'Manager with this name already exists.')
                else:
                    cursor.execute("INSERT INTO Managers (ManagerID, managername, managerphone) SELECT COALESCE(MAX(ManagerID), 0) + 1, ?, ? FROM Managers", (manager_name, manager_phone))
                    conn.commit()
                    self.contract_manager_choose.addItem(manager_name)
                    QMessageBox.information(self.sql_window, 'Success', 'Manager added successfully.')
                conn.close()
            except sqlite3.Error as e:
                QMessageBox.warning(self.sql_window, 'Query execution error', f'Error: {str(e)}')
        # Clear input fields after processing
        self.manager_name_input.clear()
        self.manager_phone_input.clear()
        self.add_data_window.raise_()

    def load_contract_image(self) -> None:
        """
        Function to load contract details onto a contract template image.

        Retrieves contract details from the database based on the provided contract number.
        Loads a contract template image and writes the contract details onto it.

        Args:
        - self: Reference to the current instance of the class.

        Returns:
        - None

        Raises:
        - sqlite3.Error: Raised if there's an error during database operations.
        """

        contract_number = self.contract_number_input.text() # Select number of contract
        # Loading a contract template
        contract_template = Image.open(f'app_files\\default.jpg')  

        # Выбор шрифта и его размера
        font = ImageFont.truetype('arial.ttf', size=10) 

        # Create an ImageDraw object for image editing
        draw = ImageDraw.Draw(contract_template)

        # Set the position and text for each field
        text_positions = {
            'Signing date': (400, 100),
            'Contract ID': (270, 130),
            'Service': (20, 300),
            'Company name': (20, 320),
            'Client name': (320, 400),
            'Phone number': (320, 420),
            'Start date': (320, 440),
            'End date': (320, 460),
            'Pay date': (320, 480),
            'Price': (320, 500)
        }

        try:
            conn = sqlite3.connect('app_files\\EGA_database.db')
            cursor = conn.cursor()
            cursor.execute(f"select signingdate, contractid, servicename,  companyname, clientname, clientphone, startdate, enddate, paydate, price from contracts join TypeService using(TypeServiceID) join service using(serviceid) join company using(companyid) join clients using(clientid) join managers using(managerid) where contractid = '{contract_number}'")
            rows = cursor.fetchall()
            

            conn.close()
        except sqlite3.Error as e:
            QMessageBox.warning(self.sql_window, 'Query execution error', f'Error: {str(e)}')

        contract_fields = {
            'Signing date': rows[0][0],
            'Contract ID': rows[0][1],
            'Service': rows[0][2],
            'Company name': rows[0][3],
            'Client name': rows[0][4],
            'Phone number': rows[0][5],
            'Start date': rows[0][6],
            'End date': rows[0][7],
            'Pay date': rows[0][8],
            'Price': str(rows[0][9]) + '$'
        }

        # Add the text of specified fields to the image
        for field, position in text_positions.items():
            if field in contract_fields:
                draw.text(position, f"{field}: {contract_fields[field]}", font=font, fill='black')

        # Saving the modified image to a file with a unique name for each line
        # Compression with quality parameter added
        # contract_template.save(f'{gen_data_directory}\contract_{fields["Contract ID"]}.jpg', quality=80)  
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save file', f"contract_{contract_number}.jpg", "Images (*.jpg *.png)")
        contract_template.save(f'{file_path}', quality=80)  

        # contract_number = self.contract_number_input.text() # Select number of contract
        # if contract_number.isdigit():   # Check for digit
        #     file_path, _ = QFileDialog.getSaveFileName(self, 'Save file', f"contract_{contract_number}.jpg", "Images (*.jpg *.png)")
        #     if file_path:
        #         # Scaning dir for contratcs
        #         source_file_path = f"app_files\\scan_contract\\contract_{contract_number}.jpg"
        #         if os.path.exists(source_file_path):
        #             try:
        #                 os.makedirs(os.path.dirname(file_path), exist_ok=True)
        #                 with open(source_file_path, 'rb') as src_file, open(file_path, 'wb') as dest_file:
        #                     dest_file.write(src_file.read())
        #                 QMessageBox.information(self, 'success', f"Contract image {contract_number} has been successfully saved")
        #             except Exception as e:
        #                 QMessageBox.warning(self, 'Error', f"Failed to save file: {e}")
        #         else:
        #             QMessageBox.warning(self, 'Error', f"Contract image {contract_number} not found")
        # else:
        #     QMessageBox.warning(self, 'Error', 'Enter contract number (number)')




    def update_second_combo(self) -> None:
        """
        Function to update the content of the second combo box based on the selected action in the first combo box.

        Retrieves the selected action from the first combo box and clears the content of the second combo box.
        If the selected action is present in the dictionary of second combos, updates the content of the second combo box accordingly.

        Args:
        - self: Reference to the current instance of the class.

        Returns:
        - None
        """
         
        selected_action = self.action_combo_box.currentText()
        self.second_combo.clear()
        # Check if the selected action exists in the dictionary of second combos
        if selected_action in self.second_combos:
            self.second_combo.addItems(self.second_combos[selected_action])

    def update_sql_script(self) -> None:
        """
        Function to update SQL scripts based on the selected action and word in combo boxes.

        Retrieves the selected action and word from combo boxes.
        Updates the SQL script displayed in a text field based on the selected action and word.

        Args:
        - self: Reference to the current instance of the class.

        Returns:
        - None
        """
        # Clear and populate the second drop-down list depending on the selected action in the first list
        
        selected_action = self.action_combo_box.currentText()
        selected_word = self.second_combo.currentText()
        # Update the SQL script based on the selected action and word
        if selected_action == "Contracts report":
            self.sql_input.setPlainText('''SELECT ContractID, clients.CompanyID, CompanyName, ClientID, ClientName, service.TypeServiceID, TypeServiceName, ServiceID, ServiceName, SigningDate, StartDate, EndDate, PayDate, Price, ManagerID, ManagerName 
FROM Contracts 
join company using(companyid)
join clients using(clientid)
join typeservice using(typeserviceid)
join service using(serviceid)
join managers using(managerid)''')
            self.second_combo.clear()
        if selected_action == "Three most important customers (those who brought the most profit)":
            self.sql_input.setPlainText("SELECT \n\tClientID, ClientName, SUM(Price) AS TotalProfit\nFROM Contracts\nJOIN Clients USING(ClientID)\nGROUP BY ClientID\nORDER BY TotalProfit DESC\nLIMIT 3;")
        if selected_action == "Choose action":
            self.sql_input.setPlainText(" ")
            self.second_combo.clear()
        if selected_action == "List of employees sorted in reverse order according to the value of the contract amount":
            self.second_combo.clear()
            self.sql_input.setPlainText("SELECT  \n\tManagerID, ManagerName, SUM(Contracts.Price) AS TotalContractPrice\nFROM Managers\nJOIN Contracts USING(ManagerID)\nGROUP BY ManagerID\nORDER BY TotalContractPrice DESC ")
        if selected_action == "Average monthly amount of contracts for services of each type":
            self.sql_input.setPlainText("SELECT \n\tTypeServiceID, TypeServiceName, AVG(TotalPrice) AS AvgMonthPrice\nFROM\n\t(SELECT \n\t\tstrftime('%Y-%m', SigningDate) AS YearMonth, TypeServiceID, SUM(Price) AS TotalPrice \n\tFROM Contracts \n\tGROUP BY YearMonth, TypeServiceID) AS Subquery\nJOIN TypeService USING(TypeServiceID)\nGROUP BY TypeServiceID;")

        
        if selected_action == "List of clients grouped by city":
            self.sql_input.setPlainText("SELECT city, sum(price) as Sum, count(*) as Amount \nFROM Clients join contracts using(clientid) group by city;")
            self.second_combo.clear()
        if selected_action == "List of individual service contracts":
            self.sql_input.setPlainText(f"SELECT \n\t*\nFROM Contracts\nJOIN Service USING(ServiceID)\nWHERE ServiceName ='{selected_word}';")
        if selected_action == "List of contracts grouped by type of service for the past year":
            self.sql_input.setPlainText(f"SELECT \n\t*\nFROM Contracts\nJOIN Service USING(ServiceID)\nJOIN TypeService USING(TypeServiceID)\nWHERE TypeServiceName ='{selected_word}' AND strftime('%Y', SigningDate) = strftime('%Y', 'now', '-1 year');")
                



    def confirm_exit(self) -> None:
        """
        Function to display a confirmation message box for exiting the application.

        Displays a QMessageBox to confirm the user's intention to exit the application.
        If the user selects 'Yes,' the function triggers the back_to_login method.
        """

        reply = QMessageBox.question(
            self.sql_window,
            'Confirmation of exit',
            'Are you sure you want to go out?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.back_to_login()


    def back_to_login(self) -> None:
        """
        Function to navigate back to the login window from the SQL window.

        Closes the SQL window and displays the login window.
        """
        self.sql_window.close()
        self.show()


    def execute_sql_script(self) -> None:
        """
        Function to execute an SQL script entered in a text field and display the results in a QTableWidget.

        Retrieves the SQL script from the text field, executes it against the database, and displays the results in a table.
        Displays column names and rows of data in a QTableWidget.

        Args:
        - self: Reference to the current instance of the class.

        Returns:
        - None
        """

        sql_script = self.sql_input.toPlainText()
        try:
            conn = sqlite3.connect('app_files\\EGA_database.db')
            cursor = conn.cursor()
            cursor.execute(sql_script)
            rows = cursor.fetchall()

            # Display results as a table with column names
            if rows:
                columns = [description[0] for description in cursor.description]
                self.result_table.setColumnCount(len(columns))
                self.result_table.setHorizontalHeaderLabels(columns)
                self.result_table.setRowCount(len(rows))
                
                for i, row in enumerate(rows):
                    for j, cell in enumerate(row):
                        self.result_table.setItem(i, j, QTableWidgetItem(str(cell)))
                # Set column widths by content
                self.result_table.resizeColumnsToContents()
            else:
                self.result_table.clear()  # Clear the table if there are no results

            conn.close()
        except sqlite3.Error as e:
            QMessageBox.warning(self.sql_window, 'Query execution error', f'Error: {str(e)}')

    
    def download_csv(self):
        """
        Function to download data from QTableWidget as a CSV file.

        Retrieves data from the QTableWidget and saves it as a CSV file.
        Displays a dialog for the user to choose the file location to save the CSV file.

        Args:
        - self: Reference to the current instance of the class.

        Returns:
        - None
        """

        # Get data from QTableWidget
        table = self.result_table
        rows = table.rowCount()
        columns = table.columnCount()
        # Check results
        if rows > 0 and columns > 0:
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getSaveFileName(self, "Save to CSV", "", "CSV Files (*.csv)", options=options)
            if fileName:
                try:
                    with open(fileName, 'w', newline='', encoding='utf-8') as csv_file:
                        csv_writer = csv.writer(csv_file)
                        # Write column headings
                        headers = [table.horizontalHeaderItem(i).text() for i in range(columns)]
                        csv_writer.writerow(headers)
                        # Recording data
                        for row in range(rows):
                            row_data = [table.item(row, col).text() for col in range(columns)]
                            csv_writer.writerow(row_data)
                    QMessageBox.information(self.sql_window, 'Success', 'File saved successfully.')
                except Exception as e:
                    QMessageBox.warning(self.sql_window, 'Error', f'Error saving: {str(e)}')

        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_app = LoginApp()
    login_app.show()
    sys.exit(app.exec_())
