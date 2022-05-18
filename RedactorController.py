import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QRect, QMimeData
from PyQt5.QtWidgets import (
    QApplication, QMainWindow,
    QTextEdit, QAction, QFileDialog, QMessageBox
)
from PyQt5.QtGui import QIcon, QFileOpenEvent, QFont
from PyQt5 import QtPrintSupport
from RedactorView import RedactorView
from RedactorModel import RedactorModel


def suggest_saving_file(func):
    def wrapper(self):
        choice = self.view.suggest_saving_file_message()
        if choice == QMessageBox.Cancel:
            return
        if choice == QMessageBox.Yes:
            self.model.save_current_file()
        func(self)

    return wrapper


class RedactorController:
    def __init__(self, model):
        self.model = model
        self.view = None
        self.init_view()

    def init_view(self):
        self.view = RedactorView(self.model, self)
        self.view.initUI()
        self.view.show()

    @suggest_saving_file
    def new_file(self):
        self.model.destroy()
        self.model = RedactorModel()
        self.init_view()

    @suggest_saving_file
    def open_file(self):
        new_file_path = self.view.get_open_file_name()
        if new_file_path is None:
            return
        self.model.open_file(new_file_path)

    def save_current_file(self):
        self.model.save_current_file()

    def save_as_current_file(self):
        self.model.save_as_current_file()

    def set_text_changed(self):
        self.model.set_text_changed()

    def change_font(self, new_font):
        self.model.change_font(new_font)

    def change_font_size(self, size):
        self.model.change_font_size(size)

    def change_font_color(self):
        color = QtWidgets.QColorDialog.getColor()
        self.model.change_font_color(color)

    def set_font_italic(self):
        self.model.set_font_italic()

    def set_font_underline(self):
        self.model.set_font_underline()

    def set_font_bold(self):
        self.model.set_font_bold()

    def set_font_strike(self):
        self.model.set_font_strike()

    def cut(self):
        self.model.cut()

    def copy(self):
        self.model.copy()

    def paste(self):
        self.model.paste()

    def undo(self):
        self.model.undo()

    def redo(self):
        self.model.redo()

    @suggest_saving_file
    def redactor_exit(self):
        self.view.destroy()