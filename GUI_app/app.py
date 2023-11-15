import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QTextEdit, QTableWidget, QTableWidgetItem, QSplitter
from PyQt5.QtGui import QPixmap


class LoginApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Login App')
        self.setGeometry(100, 100, 800, 600)

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
        self.sql_window.setWindowTitle('SQL Script')
        self.sql_window.setGeometry(100, 100, 1800, 1000)

        self.sql_label = QLabel('Введите SQL-скрипт:')
        self.sql_input = QTextEdit()
        self.execute_button = QPushButton('Выполнить')
        self.result_table = QTableWidget()  # Используем QTableWidget для отображения результатов

        splitter = QSplitter()
        splitter.setOrientation(0)  # Устанавливаем вертикальную ориентацию для Splitter'а
        splitter.setSizes([1200, 700])  # Устанавливаем начальные размеры блоков

        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.sql_label)
        left_layout.addWidget(self.sql_input)
        left_layout.addWidget(self.execute_button)
        left_layout.addWidget(self.result_table)
        left_widget.setLayout(left_layout)

        image_label = QLabel()  # Добавляем QLabel для отображения изображения
        pixmap = QPixmap('generated_data/schema.jpg')
        pixmap = pixmap.scaledToWidth(700)  # Изменяем размер изображения по ширине
        image_label.setPixmap(pixmap)

        hbox = QHBoxLayout()
        hbox.addWidget(left_widget)
        hbox.addWidget(image_label)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        splitter.setLayout(vbox)

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
