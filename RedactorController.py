from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from RedactorView import RedactorView
from RedactorModel import RedactorModel
from T9 import T9


def suggest_saving_file(func):
    def wrapper(self):
        if self.model.is_saved is False:
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
        self.view.init_UI()
        self.view.show()
        T9.view = self.view
        T9.set_t9_words_data_by_default()

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

    def on_cursor_changed(self):
        self.model.update_t9_buttons()

    def t9_button_clicked(self, button):
        text = button.text()
        if len(text) != 0:
            self.model.change_word_under_cursor(text)

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

    def redactor_exit(self):
        self.view.close()

    def on_close_event(self, event):
        choice = self.view.suggest_saving_file_message()
        if choice == QMessageBox.Cancel:
            event.ignore()
            return
        if choice == QMessageBox.Yes:
            self.model.save_current_file()
        event.accept()
