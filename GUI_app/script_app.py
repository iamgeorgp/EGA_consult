import sys
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QSpacerItem, QSizePolicy, QSizePolicy, QDesktopWidget, QMessageBox, QComboBox, QTextEdit, QTableWidget, QHBoxLayout, QSplitter, QScrollArea, QFileDialog, QTableWidgetItem, QApplication
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import csv
import sqlite3
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
        # self.login_input.setText('admin')
        # self.password_input.setText('admin')

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

        cursor.execute("SELECT DISTINCT service FROM service")
        result_services = cursor.fetchall()
        unique_services = [row[0] for row in result_services]

        cursor.execute("SELECT DISTINCT TypeService FROM typeservice")
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



    def load_contract_image(self) -> None:
        """
        Function to load a contract image based on the contract number input.

        Retrieves the contract number input and saves the corresponding image file.
        Displays success or error messages based on the process outcome.
        """

        contract_number = self.contract_number_input.text() # Select number of contract
        if contract_number.isdigit():   # Check for digit
            file_path, _ = QFileDialog.getSaveFileName(self, 'Save file', f"contract_{contract_number}.jpg", "Images (*.jpg *.png)")
            if file_path:
                # Scaning dir for contratcs
                source_file_path = f"app_files\\scan_contract\\contract_{contract_number}.jpg"
                if os.path.exists(source_file_path):
                    try:
                        os.makedirs(os.path.dirname(file_path), exist_ok=True)
                        with open(source_file_path, 'rb') as src_file, open(file_path, 'wb') as dest_file:
                            dest_file.write(src_file.read())
                        QMessageBox.information(self, 'success', f"Contract image {contract_number} has been successfully saved")
                    except Exception as e:
                        QMessageBox.warning(self, 'Error', f"Failed to save file: {e}")
                else:
                    QMessageBox.warning(self, 'Error', f"Contract image {contract_number} not found")
        else:
            QMessageBox.warning(self, 'Error', 'Enter contract number (number)')




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
