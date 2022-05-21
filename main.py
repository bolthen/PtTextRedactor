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
    T9.init_T9('WordsData.txt')
    initialise_window()

    '''
    data = set()
    words_regex = re.compile(r'[A-Za-zА-Яа-я]{2,}')
    with open('WordsData.txt', 'r', encoding='UTF-8') as f:
        for i, k, in enumerate(f.readlines()):
            words = words_regex.findall(k)
            for j in words:
                data.add(j.lower())

    while True:
        w = str(input())
        print(get_close_matches(w, data, 10))
        '''
