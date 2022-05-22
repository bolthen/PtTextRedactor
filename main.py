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
    try:
        with open('WordsData.txt', 'r', encoding='UTF-8') as f:
            T9.update_t9_words_data(f)
    except FileNotFoundError:
        pass

    initialise_window()
