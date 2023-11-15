import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QTextEdit, QTableWidget, QTableWidgetItem, QSplitter
from PyQt5.QtGui import QPixmap
import sys
from PyQt5.QtWidgets import QApplication, QComboBox, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QTextEdit, QTableWidget, QTableWidgetItem, QSplitter, QScrollArea
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QMessageBox, QTextEdit, QTableWidget, QTableWidgetItem, QSplitter, QScrollArea, QComboBox, QDesktopWidget
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class LoginApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Login App')
        self.setGeometry(100, 100, 800, 600)
        
        self.setStyleSheet('''
            * {
                font-family: Arial, sans-serif;
                font-size: 12pt;
            }
            QWidget {
                background-color: #f0f0f0;
            }
            QLineEdit, QTextEdit, QComboBox {
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 8px 12px;
                border-radius: 4px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 12px;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLabel {
                color: #333;
            }
        ''')

        self.login_label = QLabel('Логин:')
        self.password_label = QLabel('Пароль:')

        self.login_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_input.setText('admin')
        self.password_input.setText('admin')

        self.login_button = QPushButton('Войти')
        self.login_button.clicked.connect(self.check_credentials)

        vbox = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()

        hbox1.addWidget(self.login_label)
        hbox1.addWidget(self.login_input)
        hbox2.addWidget(self.password_label)
        hbox2.addWidget(self.password_input)

        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addWidget(self.login_button)

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
                background-color: #f0f0f0;
                                      border: 1px solid #ccc;
                border-radius: 4px;
            }
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 8px 12px;
                border-radius: 4px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 12px;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLabel {
                color: #333;
            }
        ''')

        # Создание кнопок над блоком ввода SQL-скрипта
        combo_box = QComboBox()
        combo_box.addItem("Option 1")
        combo_box.addItem("Option 2")
        combo_box.addItem("Option 3")

        button2 = QPushButton('Button 2')
        button3 = QPushButton('Button 3')
        button4 = QPushButton('Button 4')
        button5 = QPushButton('Button 5')

        self.sql_label = QLabel('Введите SQL-скрипт:')
        self.sql_input = QTextEdit()
        self.execute_button = QPushButton('Выполнить')
        self.result_table = QTableWidget()  # Используем QTableWidget для отображения результатов

        vbox_buttons = QHBoxLayout()  # Горизонтальный контейнер для кнопок
        vbox_buttons.addWidget(combo_box)
        vbox_buttons.addWidget(button2)
        vbox_buttons.addWidget(button3)
        vbox_buttons.addWidget(button4)
        vbox_buttons.addWidget(button5)

        outer_splitter = QSplitter(Qt.Horizontal)
        inner_splitter = QSplitter(Qt.Vertical)

        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_layout.addLayout(vbox_buttons)  # Добавляем кнопки в вертикальный контейнер
        left_layout.addWidget(self.sql_label)
        left_layout.addWidget(self.sql_input)
        left_layout.addWidget(self.execute_button)
        left_layout.addWidget(self.result_table)
        left_widget.setLayout(left_layout)

        inner_splitter.addWidget(left_widget)
        inner_splitter.addWidget(self.result_table)

        outer_splitter.addWidget(inner_splitter)

        right_widget = QWidget()
        right_layout = QVBoxLayout()

        image_label = QLabel()
        pixmap = QPixmap('generated_data/shema2.jpg')
        image_label.setPixmap(pixmap)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(image_label)

        right_layout.addWidget(scroll_area)
        right_widget.setLayout(right_layout)

        outer_splitter.addWidget(right_widget)

        vbox = QVBoxLayout()
        vbox.addWidget(outer_splitter)

        self.execute_button.clicked.connect(self.execute_sql_script)

        self.sql_window.setLayout(vbox)
        self.sql_window.show()

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

    def show_error_message(self):
        QMessageBox.warning(self, 'Ошибка входа', 'Неверный логин или пароль. Попробуйте снова.')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_app = LoginApp()
    login_app.show()
    sys.exit(app.exec_())
