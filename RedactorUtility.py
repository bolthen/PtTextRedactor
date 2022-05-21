import re
from PyQt5 import QtWidgets
from PyQt5 import QtGui


class Bar:
    def __init__(self, name: str, bar, UI_elements: str):
        self.bar_name = name
        self.UI_elements = UI_elements
        self.parent_bar = bar

    def add_UI_elements(self, redactor):
        for UI_element in self.UI_elements.split(', '):
            if UI_element == 'Sep':
                self.parent_bar.addSeparator()
            elif UI_element in redactor.qwidget_name_to_qwidget:
                self.parent_bar.addWidget(
                    redactor.qwidget_name_to_qwidget[UI_element])
            elif UI_element in redactor.qaction_name_to_qaction:
                self.parent_bar.addAction(
                    redactor.qaction_name_to_qaction[UI_element])
            else:
                continue


class T9:
    data = set()
    _words_regex = re.compile(r'[A-Za-zА-Яа-я]{2,}')

    @staticmethod
    def update_t9_words_data(file):
        for i, k, in enumerate(file.readlines()):
            words = T9._words_regex.findall(k)
            for j in words:
                T9.data.add(j.lower())
                T9.data.add(j.title())


class Find(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.parent = parent
        self.lastStart = 0
        self.init_UI()

    def init_UI(self):
        findButton = QtWidgets.QPushButton("Find", self)
        findButton.clicked.connect(self.find)
        self.findField = QtWidgets.QTextEdit(self)
        self.findField.resize(250, 50)
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.findField, 1, 0, 1, 4)
        layout.addWidget(findButton, 2, 1, 1, 2)
        self.setGeometry(300, 300, 360, 250)
        self.setWindowTitle("Find")
        self.setLayout(layout)

    def find(self):
        text = self.parent.text_edit.toPlainText()
        query = self.findField.toPlainText()
        self.lastStart = text.find(query, self.lastStart + 1)
        if self.lastStart >= 0:
            end = self.lastStart + len(query)
            self.moveCursor(self.lastStart, end)
        else:
            self.lastStart = 0
            self.parent.text_edit.moveCursor(QtGui.QTextCursor.End)

    def moveCursor(self, start, end):
        cursor = self.parent.text_edit.textCursor()
        cursor.setPosition(start)
        cursor.movePosition(QtGui.QTextCursor.Right,
                            QtGui.QTextCursor.KeepAnchor, end - start)
        self.parent.text_edit.setTextCursor(cursor)
