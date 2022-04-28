import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMenu, \
    QMenuBar


class Redactor(QMainWindow):
    _WINDOW_WIDTH = 1000
    _WINDOW_HEIGHT = 800

    def __init__(self):
        super(Redactor, self).__init__()

        desktop = QApplication.desktop()
        x = desktop.width()
        y = desktop.height()

        self.setWindowTitle("Текстовый редактор")
        self.setGeometry(x // 2 - Redactor._WINDOW_WIDTH // 2,
                         y // 2 - Redactor._WINDOW_HEIGHT // 2,
                         Redactor._WINDOW_WIDTH,
                         Redactor._WINDOW_HEIGHT)

        self.text_edit = QtWidgets.QTextEdit(self)

        self.setCentralWidget(self.text_edit)
        self.font = QFont()  # создаём объект шрифта
        self.font.setFamily("Rubik")  # название шрифта
        self.font.setPointSize(20)  # размер шрифта
        self.font.setUnderline(True)  # подчёркивание

        self.text_edit.setFont(self.font)
        text_color = QColor(255, 0, 0, 255)
        background_color = QColor()
        background_color.setRgb(0, 255, 0, 255)
        self.text_edit.setTextColor(text_color)
        self.text_edit.setTextBackgroundColor(background_color)
        self.create_menu_bar()

    def create_menu_bar(self):
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)
        file_menu = QMenu("Файл", self)
        self.menu_bar.addMenu(file_menu)
        file_menu.addAction("Открыть", self.action_clicked)
        file_menu.addAction("Сохранить", self.action_clicked)

    @QtCore.pyqtSlot()
    def action_clicked(self):
        action = self.sender()
        action_text = action.text()
        print(action_text)
        if action_text == "Открыть":
            file_name = QFileDialog.getOpenFileName()[0]
            try:
                with open(file_name, 'r') as f:
                    data = f.read()
                    self.text_edit.setText(data)
            except FileNotFoundError:
                print("Such file does not exist")
        elif action_text == "Сохранить":
            file_name = QFileDialog.getSaveFileName()[0]
            try:
                with open(file_name, 'w') as f:
                    data = self.text_edit.toPlainText()
                    f.write(data)
            except FileNotFoundError:
                print("Such file does not exist")


def initialise_window():
    app = QApplication(sys.argv)
    redactor = Redactor()

    redactor.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    initialise_window()
