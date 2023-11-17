from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QComboBox

class DynamicComboBoxes(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.first_combo = QComboBox()
        self.second_combo = QComboBox()

        self.first_combo.addItems(['Option 1', 'Option 2', 'Option 3'])
        self.first_combo.currentIndexChanged.connect(self.update_second_combo)

        self.layout.addWidget(self.first_combo)
        self.layout.addWidget(self.second_combo)

        self.setLayout(self.layout)

    def update_second_combo(self, index):
        if index == 0:
            # Очистить предыдущие элементы второго списка и добавить новые элементы
            self.second_combo.clear()
            self.second_combo.addItems(['Sub Option 1', 'Sub Option 2'])
        elif index == 1:
            # Добавить другие элементы второго списка
            self.second_combo.clear()
            self.second_combo.addItems(['Sub Option 3', 'Sub Option 4'])
        elif index == 2:
            # Добавить еще другие элементы второго списка
            self.second_combo.clear()
            self.second_combo.addItems(['Sub Option 5', 'Sub Option 6'])

if __name__ == '__main__':
    app = QApplication([])
    window = DynamicComboBoxes()
    window.show()
    app.exec_()
