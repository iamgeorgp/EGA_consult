import sys
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QSpacerItem, QSizePolicy, QSizePolicy, QDesktopWidget, QMessageBox, QComboBox, QTextEdit, QTableWidget, QHBoxLayout, QSplitter, QScrollArea, QFileDialog, QTableWidgetItem, QApplication, QDateEdit
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import csv
import sqlite3
from PIL import Image, ImageDraw, ImageFont
import os

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
            self.show_error_message()


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

        self.database_selected = False

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


    def add_data_screen(self):
        self.add_data_window = QWidget()
        
        
        
        # main add data window layout
        main_layout = QVBoxLayout()

        # init  layout of adding data
        add_data_in_table = QHBoxLayout()

        # init of box clumns
        company_layout = QVBoxLayout()
        client_layout = QVBoxLayout()
        type_service_layout = QVBoxLayout()
        service_layout = QVBoxLayout()
        manager_layout = QVBoxLayout()

        # Add column "Company Table"
        company_label = QLabel('Company Table')
        company_input_label = QLabel('Enter name')
        self.company_input = QLineEdit()
        company_add_button = QPushButton('Add')
        company_add_button.clicked.connect(self.add_company)

        company_layout.addWidget(company_label)
        company_layout.addWidget(company_input_label)
        company_layout.addWidget(self.company_input)
        company_layout.addWidget(company_add_button)

        # add column "Client Table"
        client_label = QLabel('Сlient Table')
        client_input_layout = QHBoxLayout()

        client_company_choose_layout = QVBoxLayout()
        client_company_choose_label = QLabel("Choose Company")
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
        client_name_input_label = QLabel("Enter name")
        self.client_name_input = QLineEdit()
        client_name_input_layout.addWidget(client_name_input_label)
        client_name_input_layout.addWidget(self.client_name_input)

        client_city_input_layout = QVBoxLayout()
        client_city_input_label = QLabel("Enter city")
        self.client_city_input = QLineEdit()
        client_city_input_layout.addWidget(client_city_input_label)
        client_city_input_layout.addWidget(self.client_city_input)
        
        client_address_input_layout = QVBoxLayout()
        client_address_input_label = QLabel("Enter address")
        self.client_address_input = QLineEdit()
        client_address_input_layout.addWidget(client_address_input_label)
        client_address_input_layout.addWidget(self.client_address_input)
        
        client_phone_input_layout = QVBoxLayout()
        client_phone_input_label = QLabel("Enter phone")
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
        type_service_input_label = QLabel('Enter name')
        self.type_service_input = QLineEdit()
        type_service_add_button = QPushButton('Add')
        type_service_add_button.clicked.connect(self.add_type_service)

        type_service_layout.addWidget(type_service_label)
        type_service_layout.addWidget(type_service_input_label)
        type_service_layout.addWidget(self.type_service_input)
        type_service_layout.addWidget(type_service_add_button)

        # Add column "Service Table"
        service_label = QLabel('Service Table')

        service_input_layout = QHBoxLayout()

        choose_type_service_layout = QVBoxLayout()
        choose_type_service_label = QLabel('Choose Type Service')
        choose_type_service = QComboBox()
        choose_type_service_layout.addWidget(choose_type_service_label)
        choose_type_service_layout.addWidget(choose_type_service)

        service_name_layout = QVBoxLayout()
        service_name_label = QLabel('Enter name')
        service_name_input = QLineEdit()
        service_name_layout.addWidget(service_name_label)
        service_name_layout.addWidget(service_name_input)
        
        service_add_button = QPushButton('Add')

        service_input_layout.addLayout(choose_type_service_layout)
        service_input_layout.addLayout(service_name_layout)

        service_layout.addWidget(service_label)
        service_layout.addLayout(service_input_layout)
        service_layout.addWidget(service_add_button)

        

        manager_label = QLabel("Manager Table")
        manager_input_layout = QHBoxLayout()

        manager_name_layout = QVBoxLayout()
        manager_name_label = QLabel("Enter Name")
        manager_name_input = QLineEdit()
        manager_name_layout.addWidget(manager_name_label)
        manager_name_layout.addWidget(manager_name_input)

        manager_phone_layout = QVBoxLayout()
        manager_phone_label = QLabel("Enter Phone")
        manager_phone_input = QLineEdit()
        manager_phone_layout.addWidget(manager_phone_label)
        manager_phone_layout.addWidget(manager_phone_input)

        manager_input_layout.addLayout(manager_name_layout)
        manager_input_layout.addLayout(manager_phone_layout)

        manager_add_button = QPushButton('Add')

        manager_layout.addWidget(manager_label)
        manager_layout.addLayout(manager_input_layout)
        manager_layout.addWidget(manager_add_button)

        add_data_in_table.addLayout(company_layout)
        add_data_in_table.addLayout(client_layout)
        add_data_in_table.addLayout(type_service_layout)
        add_data_in_table.addLayout(service_layout)
        add_data_in_table.addLayout(manager_layout)

        main_layout.addLayout(add_data_in_table)


        self.add_data_window.setLayout(main_layout)
        self.add_data_window.show()

    def add_company(self) -> None:
        company_name = self.company_input.text()
        print(company_name)
        if company_name != '':
            try:
                conn = sqlite3.connect('app_files\\EGA_database.db')
                cursor = conn.cursor()

                cursor.execute("SELECT * FROM Company WHERE companyname = ?", (company_name,))
                existing_company = cursor.fetchone()

                if existing_company:
                    QMessageBox.warning(self.sql_window, 'Existing company', 'Company with this name already exists.')
                else:
                    cursor.execute("INSERT INTO Company (companyid, companyname) SELECT COALESCE(MAX(companyid), 0) + 1, ? FROM Company", (company_name,))
                    conn.commit()
                    self.client_company_choose.addItem(company_name)
                    QMessageBox.information(self.sql_window, 'Success', 'Company added successfully.')

                conn.close()
            except sqlite3.Error as e:
                QMessageBox.warning(self.sql_window, 'Query execution error', f'Error: {str(e)}')
    
        self.company_input.clear()
        self.add_data_window.raise_()

    def add_client(self) -> None:
        client_name = self.client_name_input.text()
        client_city = self.client_city_input.text()
        client_address = self.client_address_input.text()
        client_phone = self.client_phone_input.text()
        client_company_name = self.client_company_choose.currentText()

        if client_name != '' and client_city != '' and client_address != '' and client_phone != '':
            try:
                conn = sqlite3.connect('app_files\\EGA_database.db')
                cursor = conn.cursor()

                cursor.execute("SELECT * FROM Clients WHERE clientname = ?", (client_name,))
                existing_company = cursor.fetchone()
                if existing_company:
                    QMessageBox.warning(self.sql_window, 'Existing client', 'Client with this name already exists.')
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
                    QMessageBox.information(self.sql_window, 'Success', 'Company added successfully.')
            except sqlite3.Error as e:
                QMessageBox.warning(self, 'Query execution error', f'Error: {str(e)}')
        conn.close()         
        self.client_name_input.clear()
        self.client_city_input.clear()
        self.client_address_input.clear()
        self.client_phone_input.clear()
        self.add_data_window.raise_()

    def add_type_service(self) -> None:
        type_service = self.type_service_input.text()
        print(type_service)
        if type_service != '':
            try:
                conn = sqlite3.connect('app_files\\EGA_database.db')
                cursor = conn.cursor()

                cursor.execute("SELECT * FROM typeservice WHERE typeservicename = ?", (type_service,))
                existing_company = cursor.fetchone()

                if existing_company:
                    QMessageBox.warning(self.sql_window, 'Existing company', 'Company with this name already exists.')
                else:
                    cursor.execute("INSERT INTO typeservice (typeserviceid, typeservicename) SELECT COALESCE(MAX(typeserviceid), 0) + 1, ? FROM typeservice", (type_service,))
                    conn.commit()
                    QMessageBox.information(self.sql_window, 'Success', 'Company added successfully.')

                conn.close()
            except sqlite3.Error as e:
                QMessageBox.warning(self.sql_window, 'Query execution error', f'Error: {str(e)}')
    
        self.type_service_input.clear()
        self.add_data_window.raise_()

    def load_contract_image(self) -> None:
        """
        Function to load a contract image based on the contract number input.

        Retrieves the contract number input and saves the corresponding image file.
        Displays success or error messages based on the process outcome.
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
            cursor.execute(f"select signingdate, contractid, service,  companyname, clientname, clientphone, startdate, enddate, paydate, price from contracts join TypeService using(TypeServiceID) join service using(serviceid) join company using(companyid) join clients using(clientid) join managers using(managerid) where contractid = '{contract_number}'")
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
        Function to update the contents of the second_combo box based on the selected action from the action_combo_box.

        Retrieves the currently selected action from the action_combo_box and clears the contents of the second_combo.
        If the selected action exists in the second_combos dictionary attribute, it populates the second_combo
        with the corresponding items from the second_combos dictionary.
        """
         
        selected_action = self.action_combo_box.currentText()
        self.second_combo.clear()

        if selected_action in self.second_combos:
            self.second_combo.addItems(self.second_combos[selected_action])

    def update_sql_script(self) -> None:
        # Clear and populate the second drop-down list depending on the selected action in the first list
        
        selected_action = self.action_combo_box.currentText()
        selected_word = self.second_combo.currentText()
        
        if selected_action == "Contracts report":
            self.sql_input.setPlainText("SELECT\n\t* \nFROM Contracts;")
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
            self.sql_input.setPlainText("SELECT \n\tTypeServiceID, TypeService, AVG(TotalPrice) AS AvgMonthPrice\nFROM\n\t(SELECT \n\t\tstrftime('%Y-%m', SigningDate) AS YearMonth, TypeServiceID, SUM(Price) AS TotalPrice \n\tFROM Contracts \n\tGROUP BY YearMonth, TypeServiceID) AS Subquery\nJOIN TypeService USING(TypeServiceID)\nGROUP BY TypeServiceID;")

        
        if selected_action == "List of clients grouped by city":
            self.sql_input.setPlainText(f"SELECT \n\t* \nFROM Clients WHERE City = '{selected_word}';")

        if selected_action == "List of individual service contracts":
            self.sql_input.setPlainText(f"SELECT \n\t*\nFROM Contracts\nJOIN Service USING(ServiceID)\nWHERE Service ='{selected_word}';")
        if selected_action == "List of contracts grouped by type of service for the past year":
            self.sql_input.setPlainText(f"SELECT \n\t*\nFROM Contracts\nJOIN Service USING(ServiceID)\nJOIN TypeService USING(TypeServiceID)\nWHERE TypeService ='{selected_word}' AND strftime('%Y', SigningDate) = strftime('%Y', 'now', '-1 year');")
                



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
        Function to execute an SQL script, display its results in a table, and handle potential errors.

        Retrieves the SQL script from the text input, executes it on the database, and displays the results in a table.
        Handles potential SQLite errors and shows a warning message box if an error occurs during execution.
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
        Function to download data from QTableWidget and save it to a CSV file.

        Retrieves data from the QTableWidget, prompts the user to select a location to save as a CSV file,
        and writes the table data into the CSV file. Shows success or error message boxes based on the outcome.
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

    def show_error_message(self):
        """
        Function to display a warning message about login errors.

        Shows a QMessageBox with a warning message indicating invalid login or password. Prompts the user to try again.
        """
        QMessageBox.warning(self, 'Login error', 'Invalid login or password. Try again.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_app = LoginApp()
    login_app.show()
    sys.exit(app.exec_())
