from PyQt5.QtGui import QFont, QTextCursor, QTextCharFormat
from difflib import get_close_matches
from RedactorUtility import T9


class RedactorModel:
    def __init__(self):
        self.text = None
        self.font = None
        self.font_size = 14
        self.current_char_format = QTextCharFormat()
        self.view = None
        self.file_name = "Безымянный.red"
        self.file_path = ""
        self.is_saved = True

    def open_file(self, new_file_path):
        try:
            with open(new_file_path, 'r') as file:
                self.view.text_edit.clear()
                self.view.text_edit.setText(file.read())
                self.is_saved = True
        except FileNotFoundError:
            self.view.show_error()
            return

        self.file_name = new_file_path.split('/')[-1]
        self.file_path = new_file_path

        if not new_file_path.endswith(".red"):
            self.is_saved = False
            self.file_path = ''
            self.file_name += '.red'

    def save_current_file(self):
        try:
            with open(self.file_path, 'w') as file:
                file.write(self.view.text_edit.toHtml())
                self.is_saved = True
        except FileNotFoundError:
            self.save_as_current_file()

    def save_as_current_file(self):
        new_file_path = self.view.get_save_file_name()
        if new_file_path:
            self.file_path = new_file_path
            self.file_name = new_file_path.split('/')[-1]
            try:
                with open(self.file_path, 'w') as file:
                    file.write(self.view.text_edit.toHtml())
                    self.is_saved = True
            except FileNotFoundError:
                self.view.show_error()

    def set_text_changed(self):
        self.is_saved = False
        self.text = self.view.text_edit.toPlainText()
        if len(self.text) == 0:
            self._change_default_font()

    def change_font(self, new_font):
        self.font = new_font
        self.view.text_edit.setCurrentFont(self.font)
        self.view.text_edit.setFontPointSize(self.font_size)

    def change_font_size(self, size):
        self.font_size = int(size)
        self.view.text_edit.setFontPointSize(self.font_size)

    def _change_default_font(self):
        if self.font is None:
            self.font = self.view.text_edit.font()
        self.view.text_edit.setStyleSheet("font: {0}pt \"{1}\";"
                                          .format(self.font_size,
                                                  self.font.family()))

    def change_font_color(self, color):
        self.view.text_edit.setTextColor(color)

    def set_font_italic(self):
        self.view.text_edit.setFontItalic(not self.view.text_edit.fontItalic())

    def set_font_underline(self):
        self.view.text_edit.setFontUnderline(
            not self.view.text_edit.fontUnderline())

    def set_font_bold(self):
        self.view.text_edit.setFontWeight(
            QFont.Normal
            if self.view.text_edit.fontWeight() == QFont.Bold
            else QFont.Bold)

    def set_font_strike(self):
        tmp = self.view.text_edit.currentCharFormat()
        tmp.setFontStrikeOut(not tmp.fontStrikeOut())
        self.view.text_edit.setCurrentCharFormat(tmp)

    def update_t9_buttons(self):
        cursor = self.view.text_edit.textCursor()
        cursor.select(QTextCursor.WordUnderCursor)
        word = cursor.selectedText()
        matches = get_close_matches(word, T9.data,
                                    self.view.t9_buttons_count)
        while len(matches) < self.view.t9_buttons_count:
            matches.append('')
        self.view.main_form.update_buttons(matches)

    def change_word_under_cursor(self, word):
        cursor = self.view.text_edit.textCursor()
        self.current_char_format = cursor.charFormat()
        cursor.select(QTextCursor.WordUnderCursor)
        cursor.removeSelectedText()
        cursor.insertText(word, self.current_char_format)
        self.view.text_edit.setFocus()

    def cut(self):
        self.view.text_edit.cut()

    def copy(self):
        self.view.text_edit.copy()

    def paste(self):
        self.view.text_edit.paste()

    def undo(self):
        self.view.text_edit.undo()

    def redo(self):
        self.view.text_edit.redo()

    def add_observer(self, observer):
        self.view = observer
        self._change_default_font()

    def notify_observers(self):
        for x in self.view:
            x.modelIsChanged()
