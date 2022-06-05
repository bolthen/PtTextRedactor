import re
from typing import TextIO
from difflib import get_close_matches
import chardet
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMessageBox
import os.path


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
    view = None

    @staticmethod
    def get_similar_words(word):
        return get_close_matches(word, T9.data, T9.view.t9_buttons_count)

    @staticmethod
    def _update_t9_words_data(base_path):
        with FileOpener(base_path, 'r', False) as file:
            T9.data.clear()
            for i, k, in enumerate(file.readlines()):
                words = T9._words_regex.findall(k)
                for j in words:
                    T9.data.add(j.lower())
                    T9.data.add(j.title())
        T9._create_t9_base_config(base_path)

    @staticmethod
    def set_t9_words_data_by_default(self):
        cfg_path = T9._get_t9_cfg_path()
        if cfg_path is None or os.path.exists(cfg_path) is None:
            choice = self.view.suggest_choose_t9_data()
            if choice == QMessageBox.No:
                self.view.notify_about_t9()
            else:
                T9.choose_t9_data_base()
        else:
            T9._update_t9_words_data(cfg_path)

    @staticmethod
    def choose_t9_data_base():
        t9_data_base = T9.view.get_open_file_name()
        if t9_data_base is None:
            return
        T9._update_t9_words_data(t9_data_base)

    @staticmethod
    def _get_t9_cfg_path():
        with FileOpener('t9.cfg', 'r', False) as file:
            return file.read()

    @staticmethod
    def _create_t9_base_config(base_path):
        with open('t9.cfg', 'w+') as cfg:
            cfg.write(base_path)


class Find(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.parent = parent
        self.last_start = -1
        self.find_field = QtWidgets.QTextEdit(self)
        self.find_field.resize(250, 50)
        self.init_UI()

    def init_UI(self):
        find_button = QtWidgets.QPushButton("Find", self)
        find_button.clicked.connect(self.find)
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.find_field, 1, 0, 1, 4)
        layout.addWidget(find_button, 2, 1, 1, 2)
        self.setGeometry(300, 300, 360, 250)
        self.setWindowTitle("Find")
        self.setLayout(layout)

    def find(self):
        text = self.parent.text_edit.toPlainText()
        query = self.find_field.toPlainText()
        self.last_start = text.find(query, self.last_start + 1)
        if self.last_start >= 0:
            end = self.last_start + len(query)
            self.move_cursor(self.last_start, end)
        else:
            self.last_start = -1
            cursor = self.parent.text_edit.textCursor()
            cursor.setPosition(0)
            self.parent.text_edit.setTextCursor(cursor)
            QMessageBox.information(self, 'Find', 'Вхождений больше нет',
                                    QMessageBox.Ok)

    def move_cursor(self, start, end):
        cursor = self.parent.text_edit.textCursor()
        cursor.setPosition(start)
        cursor.movePosition(QtGui.QTextCursor.Right,
                            QtGui.QTextCursor.KeepAnchor, end - start)
        self.parent.text_edit.setTextCursor(cursor)


class FileOpener:
    redactor_view = None

    @staticmethod
    def init_redactor_view(view):
        FileOpener.redactor_view = view

    def __init__(self, file_name: str, roots: str, should_show_error=True):
        self.file_name = file_name
        self.roots = roots
        self._char_codec = str()
        self._file = TextIO()
        self._should_show_error = should_show_error

    def __enter__(self) -> TextIO:
        try:
            file = open(self.file_name, 'rb')
            rawdata = file.read()
            file.close()
            self._char_codec = chardet.detect(rawdata)['encoding']

        except FileNotFoundError:
            if self._should_show_error:
                FileOpener.redactor_view.show_error()
            return TextIO()

        try:
            self._file = open(self.file_name, self.roots,
                              encoding=self._char_codec)
            return self._file
        except FileNotFoundError:
            return TextIO()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._file.close()
        return True
