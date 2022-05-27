import re
import sys
from difflib import get_close_matches

from PyQt5.QtWidgets import QApplication
from RedactorModel import RedactorModel
from RedactorController import RedactorController
from RedactorUtility import T9


def initialise_window():
    app = QApplication(sys.argv)
    model = RedactorModel()
    controller = RedactorController(model)
    sys.exit(app.exec_())


if __name__ == '__main__':
    initialise_window()
