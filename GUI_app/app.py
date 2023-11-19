


import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import csv
import sqlite3
import os

class LoginApp(QWidget):
    def __init__(self):
        """
        Инициализация окна приложения для входа.

        Создает окно для ввода учетных данных с использованием стилей для виджетов,
        настройки размеров окна и создания элементов управления, таких как логотип,
        поля для ввода логина и пароля, кнопка входа, а также кнопка "Забыли пароль?".
        Привязывает функции к событиям нажатия кнопок для выполнения соответствующих действий.
        """
        
        super().__init__()
        
        # Установка стилей для виджетов
        self.setStyleSheet('''
            /* Общие стили для всех виджетов */
            * {
                font-family: Roboto, Arial, sans-serif;
                font-size: 13pt;
            }
            QWidget {
                background-color: #ffffff;
            }
            QLineEdit, QTextEdit, QComboBox {
                background-color: #ffffff;
                border: 1px solid #005bbd; /* Синий контур */
                border-radius: 5px; /* Скругление углов */
                padding: 5px;
            }
            QLineEdit:hover, QTextEdit:hover, QComboBox:hover {
                border: 1px solid #2980b9; /* Плавное выделение при наведении */
            }
            /* Стили для кнопок */
            QPushButton {
                background-color: #005bbd; /* Основной цвет синий */
                border: 2px solid #005bbd; /* Контур с кнопкой */
                border-radius: 20px; /* Задаем большое скругление для округлых кнопок */
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
                background-color: #2980b9; /* Плавное изменение цвета при наведении */
            }
            /* Стили для текста */
            QLabel {
                color: #333;
            }
            /* Стили для кнопки "Забыли пароль?" */
            QPushButton#forgetPasswordButton {
                background-color: white;
                color: #005bbd; /* Голубой цвет текста */
                border: 0px solid #3498db; /* Синий контур */
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton#forgetPasswordButton:hover {
                background-color: #f0f0f0; /* Цвет фона при наведении */
            }
        ''')
        self.setWindowIcon(QIcon('data\EGA_logo.jpg'))
        # Настройка основного окна
        self.setWindowTitle('Login App')
        self.setFixedSize(380, 530)

        # Создание логотипа
        self.logo_label = QLabel()
        pixmap = QPixmap('D:\Repositories\EGA_consult\data\EGA_logo.jpg')
        pixmap_resized = pixmap.scaled(300, 300, aspectRatioMode=Qt.KeepAspectRatio)
        self.logo_label.setPixmap(pixmap_resized)
        self.logo_label.setAlignment(Qt.AlignCenter)

        # Создание виджетов для ввода данных и кнопок
        self.login_label = QLabel('Login:')
        self.password_label = QLabel('Password:')
        self.login_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton('Sign in')
        self.forget_password_button = QPushButton('Forgot password?', objectName='forgetPasswordButton')

        # Установка текста по умолчанию для поля ввода логина и пароля
        # self.login_input.setText('admin')
        # self.password_input.setText('admin')

        # Привязка функций к событиям нажатия кнопок
        self.login_button.clicked.connect(self.check_credentials)
        self.forget_password_button.clicked.connect(self.show_forgot_password)

        # Создание вертикального контейнера
        vbox = QVBoxLayout()
        vbox.addWidget(self.logo_label)
        vbox.addWidget(self.login_label)
        vbox.addWidget(self.login_input)
        vbox.addWidget(self.password_label)
        vbox.addWidget(self.password_input)
        vbox.addWidget(self.login_button)
        vbox.addWidget(self.forget_password_button)

        # Добавление пустого пространства внизу окна
        spacer = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox.addItem(spacer)

        self.setLayout(vbox)



    
    def showEvent(self, event):
        """
        Переопределение метода showEvent для обработки события отображения окна.

        Вызывается при отображении окна. Вызывает метод для позиционирования окна по центру экрана.
        """
        super().showEvent(event)
        self.centerWindow()  # Вызов метода для позиционирования окна по центру



    def centerWindow(self):
        """
        Располагает окно по центру экрана.

        Получает размер экрана, размеры окна и рассчитывает центральное положение окна.
        Устанавливает позицию окна по центру экрана.
        """
        # Получаем размер экрана
        screen = QDesktopWidget().screenGeometry()
        width, height = screen.width(), screen.height()

        # Получаем размеры окна
        window_width, window_height = self.width(), self.height()

        # Рассчитываем центральное положение окна
        x_position = (width - window_width) // 2
        y_position = (height - window_height) // 2

        # Устанавливаем позицию окна по центру экрана
        self.move(x_position, y_position)

    def check_credentials(self):
        """
        Проверяет введенные учетные данные.

        Получает логин и пароль из соответствующих полей ввода.
        Если логин и пароль совпадают с 'admin', открывает окно SQL-скриптов.
        В противном случае отображает сообщение об ошибке.
        """
        login = self.login_input.text()
        password = self.password_input.text()

        # Проверка учетных данных на соответствие
        if login == 'admin' and password == 'admin':
        # Открываем окно SQL-скриптов при успешном входе
            self.open_sql_screen()
            self.close()  # Закрываем окно входа при успешном входе
        else:
            # Отображаем сообщение об ошибке в случае неверных учетных данных
            self.show_error_message()


    def show_forgot_password(self):
        """
        Отображает окно сообщения с информацией о восстановлении пароля.

        Вызывает диалоговое окно с информацией о том, как сбросить пароль.
        """
        message = QMessageBox()  # Создание объекта диалогового окна
        message.setWindowTitle("Forgot Password")  # Установка заголовка окна
        message.setText("Contact technical support at support@egaconsult.com to reset your password.")  # Установка текста сообщения
        message.setIcon(QMessageBox.Information)  # Установка иконки сообщения
        message.setStandardButtons(QMessageBox.Ok)  # Установка стандартной кнопки для подтверждения
        message.exec_()  # Отображение диалогового окна


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

        # Предопределение возможных списков
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

        # Создание выпадающих списков для выбора sql-скрпитов
        # Первый список
        self.action_combo_box = QComboBox()
        self.action_combo_box.addItems(actions)
        self.action_combo_box.currentIndexChanged.connect(self.update_second_combo)
        self.action_combo_box.currentIndexChanged.connect(self.update_sql_script)
        # Второй выпадающий списко (если он возможен)
        self.second_combo = QComboBox()
        self.second_combo.addItems([])  
        self.second_combo.currentIndexChanged.connect(self.update_sql_script)

        # Подключение к базе данных
        conn = sqlite3.connect('D:\Repositories\EGA_consult\databases\EGA_database.db')
        cursor = conn.cursor()

        # Выполнение запросов для заполнения значений выпадающего второго списка действительными данными
        cursor.execute("SELECT DISTINCT City FROM Clients")
        result = cursor.fetchall()
        cities = [row[0] for row in result]

        cursor.execute("SELECT DISTINCT service FROM service")
        result_services = cursor.fetchall()
        unique_services = [row[0] for row in result_services]

        cursor.execute("SELECT DISTINCT TypeService FROM typeservice")
        result = cursor.fetchall()
        unique_type_services = [row[0] for row in result]

        # Закрытие соединения с базой данных
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


        # Создание заголовка редактора SQL
        self.sql_label = QLabel('Enter an SQL script or select an action:')
        self.sql_label.setStyleSheet('''QWidget {

        font-size: 26px;

    }''')
        # Создание окна ввода SQL скрипта
        self.sql_input = QTextEdit()
        self.sql_input.setPlaceholderText("SQL-script: SELECT ...")
      
        self.sql_input.setStyleSheet('''QWidget {
        background-color: #ffffff;
        border: 1px solid #ccc;
        border-radius: 4px;
        font-size: 20px;
        font-family: consolas;
                                     padding: 8px 16px;
                                                 font-size: 18px;
    }''')
        # Создание кнопки запуска SQL скрипта
        self.execute_button = QPushButton('RUN')
        # Создание табличного окна вывода результата скрипта SQL
        self.result_table = QTableWidget()  # Используем QTableWidget для отображения результатов
        self.result_table.setStyleSheet('''QWidget {
        background-color: #ffffff;
        border: 1px solid #ccc;
        border-radius: 4px;
        font-size: 16px;
        font-family: consolas;
    }''')

        horizontal_layout  = QHBoxLayout()

        self.contract_number_input = QLineEdit()
        self.contract_number_input.setPlaceholderText("Number of Contract")
        self.contract_number_input.setStyleSheet('''QWidget {
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

        # Создание кнопки загрузки результата SQL скрипта в формате .csv
        download_button = QPushButton('Download to CSV') 
        download_button.clicked.connect(self.download_csv)

        # Создание виджетов верхнего и нижнего левых блоков 
        upper_left_widget = QWidget()
        down_left_widget = QWidget()

        # Создание лэйаутов верхнего и нижнего левых блоков 
        upper_left_layout = QVBoxLayout()
        down_left_layout = QVBoxLayout()

        # Верхний лейаут состоит из заголовка, двух выпадающих списков, блока ввода скрипта и кнопки его запуска
        upper_left_layout.addWidget(self.sql_label)
        upper_left_layout.addWidget(self.action_combo_box)
        upper_left_layout.addWidget(self.second_combo)
        upper_left_layout.addWidget(self.sql_input)
        upper_left_layout.addWidget(self.execute_button)

        # Нижний лейаут состоит из блока вывода скрипта, кнопки загрузки csv и контракта
        down_left_layout.addWidget(self.result_table)
        down_left_layout.addWidget(download_button)
        down_left_layout.addLayout(horizontal_layout)

        # Заполнение виджетов
        upper_left_widget.setLayout(upper_left_layout)
        down_left_widget.setLayout(down_left_layout)


        
        # Добавление левых блоков к горизонтальному разделителю
        inner_splitter.addWidget(upper_left_widget)
        inner_splitter.addWidget(down_left_widget)

        
        # Определение правого блока
        right_widget = QWidget()
        right_widget.setStyleSheet('''QWidget {
        background-color: #ffffff;
        border: 1px solid #ccc;
        border-radius: 4px;
    }''')
        right_layout = QVBoxLayout()

        # Опредление изображения схемы
        image_label = QLabel()
        pixmap = QPixmap('D:\Repositories\EGA_consult\generated_data\shema22.jpg')
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)

        # Создания скролла для схемы базы
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(image_label)

        # Добавление блоков правого виджета
        right_layout.addWidget(scroll_area)
        right_widget.setLayout(right_layout)

        # Добавления блоков к вертикальному разделителю
        outer_splitter.addWidget(inner_splitter)
        outer_splitter.addWidget(right_widget)

        # Создание бокс для общий блоков и кнопки выхода
        vbox = QVBoxLayout()
        vbox.addWidget(outer_splitter)
        self.execute_button.clicked.connect(self.execute_sql_script)
        back_to_login_button = QPushButton('Back to Login')
        back_to_login_button.clicked.connect(self.confirm_exit)  # Подтверждение выхода
        vbox.addWidget(back_to_login_button)
        self.sql_window.setLayout(vbox)

        # На весь экран
        self.sql_window.showFullScreen()



    def load_contract_image(self):
        contract_number = self.contract_number_input.text()
        if contract_number.isdigit():
            file_path, _ = QFileDialog.getSaveFileName(self, 'Save file', f"contract_{contract_number}.jpg", "Images (*.jpg *.png)")
            if file_path:
                source_file_path = f"generated_data/scan_contract/contract_{contract_number}.jpg"
                if os.path.exists(source_file_path):
                    try:
                        os.makedirs(os.path.dirname(file_path), exist_ok=True)
                        # копирование файла по выбранному пути
                        with open(source_file_path, 'rb') as src_file, open(file_path, 'wb') as dest_file:
                            dest_file.write(src_file.read())
                        QMessageBox.information(self, 'success', f"Contract image {contract_number} has been successfully saved")
                    except Exception as e:
                        QMessageBox.warning(self, 'Error', f"Failed to save file: {e}")
                else:
                    QMessageBox.warning(self, 'Error', f"Contract image {contract_number} not found")
        else:
            QMessageBox.warning(self, 'Error', 'Enter contract number (number)')




    def update_second_combo(self, index):
        selected_action = self.action_combo_box.currentText()
        self.second_combo.clear()

        if selected_action in self.second_combos:
            self.second_combo.addItems(self.second_combos[selected_action])

    def update_sql_script(self, index):
        # Очистить и заполнить второй выпадающий список в зависимости от выбранного действия в первом списке
        
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
                



    def confirm_exit(self):
        reply = QMessageBox.question(
            self.sql_window,
            'Confirmation of exit',
            'Are you sure you want to go out?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.back_to_login()


    def back_to_login(self):
    # закрываем окно SQL
        self.sql_window.close()

        # открываем окно входа
        self.show()


    def execute_sql_script(self):
        sql_script = self.sql_input.toPlainText()
        
        try:
            conn = sqlite3.connect('D:\Repositories\EGA_consult\databases\EGA_database.db')
            cursor = conn.cursor()
            cursor.execute(sql_script)
            rows = cursor.fetchall()

            # Отображение результатов в виде таблицы с названиями колонок
            if rows:
                columns = [description[0] for description in cursor.description]
                self.result_table.setColumnCount(len(columns))
                self.result_table.setHorizontalHeaderLabels(columns)
                self.result_table.setRowCount(len(rows))

                for i, row in enumerate(rows):
                    for j, cell in enumerate(row):
                        self.result_table.setItem(i, j, QTableWidgetItem(str(cell)))
                # Устанавливаем ширину столбцов по содержимому
                self.result_table.resizeColumnsToContents()
            else:
                self.result_table.clear()  # Очищаем таблицу, если результаты отсутствуют

            conn.close()
        except sqlite3.Error as e:
            QMessageBox.warning(self.sql_window, 'Query execution error', f'Error: {str(e)}')

    # Добавьте функцию для скачивания в CSV
    def download_csv(self):
        # Получите данные из QTableWidget
        table = self.result_table
        rows = table.rowCount()
        columns = table.columnCount()

        if rows > 0 and columns > 0:
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getSaveFileName(self, "Save to CSV", "", "CSV Files (*.csv)", options=options)
            if fileName:
                try:
                    with open(fileName, 'w', newline='', encoding='utf-8') as csv_file:
                        csv_writer = csv.writer(csv_file)

                        # Запись заголовков столбцов
                        headers = [table.horizontalHeaderItem(i).text() for i in range(columns)]
                        csv_writer.writerow(headers)

                        # Запись данных
                        for row in range(rows):
                            row_data = [table.item(row, col).text() for col in range(columns)]
                            csv_writer.writerow(row_data)

                    QMessageBox.information(self.sql_window, 'Success', 'File saved successfully.')
                except Exception as e:
                    QMessageBox.warning(self.sql_window, 'Error', f'Error saving: {str(e)}')

    def show_error_message(self):
        QMessageBox.warning(self, 'Login error', 'Invalid login or password. Try again.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_app = LoginApp()
    login_app.show()
    sys.exit(app.exec_())
