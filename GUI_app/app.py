
import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QMessageBox, QTextEdit, QTableWidget, QTableWidgetItem, QSplitter, QScrollArea, QComboBox, QDesktopWidget
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QFileDialog
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import csv

class LoginApp(QWidget):
    def __init__(self):
        super().__init__()        
        self.setStyleSheet('''
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
    QLabel {
        color: #333;
    }
        ''')
        self.setWindowTitle('Login App')
        self.setGeometry(300, 300, 300, 450)
        self.setFixedSize(380, 530)

        self.logo_label = QLabel()
        pixmap = QPixmap('data/EGA_logo.jpg')
        pixmap_resized = pixmap.scaled(300, 300, aspectRatioMode=Qt.KeepAspectRatio)
        self.logo_label.setPixmap(pixmap_resized)
        self.logo_label.setAlignment(Qt.AlignCenter)

        self.login_label = QLabel('Login:')
        self.password_label = QLabel('Password:')
        self.login_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton('Sign in')
        self.forget_password_button = QPushButton('Forgot password?')
        # Стилизация кнопки "Забыли пароль?"
        self.forget_password_button.setStyleSheet('''
            QPushButton {
                background-color: white;
                color: #005bbd; /* Голубой цвет текста */
                border: 0px solid #3498db; /* Синий контур */
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #f0f0f0; /* Цвет фона при наведении */
            }
        ''')

        self.login_input.setText('admin')
        self.password_input.setText('admin')

        self.login_button.clicked.connect(self.check_credentials)
        self.forget_password_button.clicked.connect(self.show_forgot_password)

        vbox = QVBoxLayout()
        vbox.addWidget(self.logo_label)
        vbox.addWidget(self.login_label)
        vbox.addWidget(self.login_input)
        vbox.addWidget(self.password_label)
        vbox.addWidget(self.password_input)
        vbox.addWidget(self.login_button)
        vbox.addWidget(self.forget_password_button)

        # Добавляем пустое пространство внизу окна
        spacer = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox.addItem(spacer)

        self.setLayout(vbox)
    
    def showEvent(self, event):
        # Вызывается при отображении окна
        super().showEvent(event)
        self.centerWindow()  # Вызов метода для позиционирования окна по центру экрана

    def centerWindow(self):
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
        login = self.login_input.text()
        password = self.password_input.text()

        if login == 'admin' and password == 'admin':
            self.open_sql_screen()
            self.close()  # Закрываем окно входа при успешном входе
        else:
            self.show_error_message()
    def show_forgot_password(self):
        message = QMessageBox()
        message.setWindowTitle("Forgot Password")
        message.setText("Contact technical support at support@egaconsult.com to reset your password.")
        message.setIcon(QMessageBox.Information)
        message.setStandardButtons(QMessageBox.Ok)
        message.exec_()

    def open_sql_screen(self):
        self.sql_window = QWidget()
        self.sql_window.setWindowTitle('EGA tool WorkSpace')
        self.sql_window.setGeometry(100, 100, 800, 600)
        self.sql_window.setStyleSheet('''
            * {
                font-family: Arial, sans-serif;
                font-size: 12pt;
            }
            QWidget {
                background-color: #ffffff;
                                      border: 1px solid #ccc;
                border-radius: 4px;
            }
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
            QLabel {
                color: #333;
            }
QComboBox {
        border: 1px solid #ccc;
        border-radius: 4px;
        padding: 2px 15px 2px 5px;
        font-size: 12px;
        color: #333;
        background-color: #fff;
        selection-background-color: #e0e0e0;
    }
    QComboBox:drop-down {
        width: 20px;
    }
    QComboBox::drop-down::down-arrow {
        image: url(down_arrow.png);
    }
        ''')



        self.layout = QVBoxLayout()

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

        self.action_combo_box = QComboBox()
        self.action_combo_box.addItems(actions)
        self.action_combo_box.currentIndexChanged.connect(self.update_second_combo)
        self.action_combo_box.currentIndexChanged.connect(self.update_sql_script)
        self.second_combo = QComboBox()
        self.second_combo.addItems([])  # Пустой список при инициализации
        self.second_combo.currentIndexChanged.connect(self.update_sql_script)

        # Подключение к базе данных
        conn = sqlite3.connect('databases/EGA_database.db')
        cursor = conn.cursor()

        # Выполнение запроса на получение уникальных значений из поля 'city'
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
        self.open_file_button = QPushButton('Выбрать файл базы данных')
        self.open_file_button.clicked.connect(self.get_file_path)
        self.sql_label = QLabel('Enter an SQL script or select an action:')
        self.sql_input = QTextEdit()
        self.execute_button = QPushButton('RUN')
        self.result_table = QTableWidget()  # Используем QTableWidget для отображения результатов



        outer_splitter = QSplitter(Qt.Horizontal)
        inner_splitter = QSplitter(Qt.Vertical)
        download_button = QPushButton('Скачать в CSV') 
        download_button.clicked.connect(self.download_csv)
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.sql_label)
        left_layout.addWidget(self.open_file_button)
        left_layout.addWidget(self.action_combo_box)
        left_layout.addWidget(self.second_combo)
        left_layout.addWidget(self.sql_input)
        left_layout.addWidget(self.execute_button)
        # left_layout.addWidget(self.result_table)
        # left_layout.addWidget(download_button)

        niz_widget = QWidget()
        niz_layout = QVBoxLayout()
        niz_layout.addWidget(self.result_table)
        niz_layout.addWidget(download_button)
        niz_widget.setLayout(niz_layout)
        left_widget.setLayout(left_layout)

        inner_splitter.addWidget(left_widget)
        inner_splitter.addWidget(niz_widget)

        outer_splitter.addWidget(inner_splitter)

        right_widget = QWidget()
        right_layout = QVBoxLayout()

        image_label = QLabel()
        pixmap = QPixmap('generated_data/shema22.jpg')
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(image_label)

        right_layout.addWidget(scroll_area)
        right_widget.setLayout(right_layout)

        outer_splitter.addWidget(right_widget)

        vbox = QVBoxLayout()
        vbox.addWidget(outer_splitter)

        self.execute_button.clicked.connect(self.execute_sql_script)

        back_to_login_button = QPushButton('Back to Login')
        back_to_login_button.clicked.connect(self.confirm_exit)  # Подтверждение выхода

        vbox.addWidget(back_to_login_button)
        self.sql_window.setLayout(vbox)
        self.sql_window.showFullScreen()

    def get_file_path(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self.sql_window, "Выберите файл базы данных", "", "Database Files (*.db)", options=options)
        if file_name:
            # print("Выбранный файл базы данных:", file_name)
            self.open_file_button.setText(f"Выбран файл: {file_name}")

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
            self.sql_input.setPlainText("SELECT * FROM Contracts;")
            self.second_combo.clear()
        if selected_action == "Three most important customers (those who brought the most profit)":
            self.sql_input.setPlainText("SELECT ClientID, ClientName, SUM(Price) AS TotalProfit FROM Contracts JOIN Clients USING(ClientID) GROUP BY ClientID ORDER BY TotalProfit DESC LIMIT 3;")
        if selected_action == "Choose action":
            self.sql_input.setPlainText(" ")
            self.second_combo.clear()
        if selected_action == "List of employees sorted in reverse order according to the value of the contract amount":
            self.second_combo.clear()
            self.sql_input.setPlainText("select  ManagerID, ManagerName, SUM(Contracts.Price) AS TotalContractPrice from Managers Join Contracts USING(managerid) GROUP BY managerid order by TotalContractPrice DESC ")
        if selected_action == "Average monthly amount of contracts for services of each type":
            self.sql_input.setPlainText("SELECT TypeServiceID, TypeService, AVG(TotalPrice) AS AvgMonthPrice FROM (SELECT strftime('%Y-%m', SigningDate) AS YearMonth, TypeServiceID, SUM(Price) AS TotalPrice FROM Contracts GROUP BY YearMonth, TypeServiceID) AS Subquery JOIN TypeService USING(TypeServiceID) GROUP BY TypeServiceID;")

        
        if selected_action == "List of clients grouped by city":
            self.sql_input.setPlainText(f"SELECT * FROM Clients WHERE City = '{selected_word}';")

        if selected_action == "List of individual service contracts":
            self.sql_input.setPlainText(f"SELECT * from Contracts JOIN Service USING(ServiceID) where Service ='{selected_word}';")
        if selected_action == "List of contracts grouped by type of service for the past year":
            self.sql_input.setPlainText(f"SELECT * from Contracts JOIN Service USING(ServiceID) JOIN TypeService USING(TypeServiceID) where TypeService ='{selected_word}' AND strftime('%Y', SigningDate) = strftime('%Y', 'now', '-1 year');")
                



    def confirm_exit(self):
        reply = QMessageBox.question(
            self.sql_window,
            'Подтверждение выхода',
            'Точно хотите выйти?',
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
            conn = sqlite3.connect('databases/EGA_database.db')
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
            QMessageBox.warning(self.sql_window, 'Ошибка выполнения запроса', f'Ошибка: {str(e)}')

    # Добавьте функцию для скачивания в CSV
    def download_csv(self):
        # Получите данные из QTableWidget
        table = self.result_table
        rows = table.rowCount()
        columns = table.columnCount()

        if rows > 0 and columns > 0:
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getSaveFileName(self, "Сохранить в CSV", "", "CSV Files (*.csv)", options=options)
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

                    QMessageBox.information(self.sql_window, 'Успех', 'Файл успешно сохранен.')
                except Exception as e:
                    QMessageBox.warning(self.sql_window, 'Ошибка', f'Ошибка сохранения: {str(e)}')

    def populate_sql_script(self, index):
        selected_action = self.action_combo_box.currentText()

        # Предположим, у вас есть словарь с SQL скриптами для каждого действия
        sql_scripts = {
        "Choose action": "",
        "List of clients by city": "SELECT \n\tCity,\n\tGROUP_CONCAT(ClientName) AS ClientsList\nFROM\n\tClients\nGROUP BY\n\tCity\nORDER BY\n\tCity;",
        "Contracts report": "-- DESCENDING ON SIGNING DATE\n\nSELECT\n\t*\nFROM\n\tContracts\nORDER BY\n\tSigningDate DESC",
        "Список контрактов по отдельной услуге": "3",
        # ... и так далее ...
        }

        if selected_action in sql_scripts:
            sql_script = sql_scripts[selected_action]
            self.sql_input.setPlainText(sql_script)
    def show_error_message(self):
        QMessageBox.warning(self, 'Ошибка входа', 'Неверный логин или пароль. Попробуйте снова.')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_app = LoginApp()
    login_app.show()
    sys.exit(app.exec_())
