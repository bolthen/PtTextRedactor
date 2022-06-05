import sys

from PyQt5.QtWidgets import QApplication
from RedactorModel import RedactorModel
from RedactorController import RedactorController


def initialise_window():
    app = QApplication(sys.argv)
    model = RedactorModel()
    RedactorController(model)
    sys.exit(app.exec_())


if __name__ == '__main__':
    initialise_window()
