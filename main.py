import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QRect, QMimeData
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFontDialog,
    QTextEdit, QAction, QFileDialog, QMessageBox
)
from PyQt5.QtGui import QIcon, QFileOpenEvent
from PyQt5 import QtPrintSupport


class Redactor(QMainWindow):
    _WINDOW_WIDTH = 1000
    _WINDOW_HEIGHT = 800

    qaction_name_to_qaction = dict()
    qwidget_name_to_qwidget = dict()

    class Bar:
        def __init__(self, name: str, bar, UI_elements: str):
            self.bar_name = name
            self.UI_elements = UI_elements
            self.parent_bar = bar

        def add_qactions(self):
            for UI_element in self.UI_elements.split(', '):
                if UI_element == 'Sep':
                    self.parent_bar.addSeparator()
                elif UI_element in Redactor.qwidget_name_to_qwidget:
                    self.parent_bar.addWidget(
                        Redactor.qwidget_name_to_qwidget[UI_element])
                elif UI_element in Redactor.qaction_name_to_qaction:
                    self.parent_bar.addAction(
                        Redactor.qaction_name_to_qaction[UI_element])
                else:
                    continue

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.text_edit = QTextEdit(self)
        self.mime_data = QMimeData()
        self.clipboard = QApplication.clipboard()
        self.file_name = "Безымянный.red"
        self.file_path = ""
        self.is_saved = True

        self.setCentralWidget(self.text_edit)
        self.qactions_init()
        self.qwidgets_init()
        self.text_edit.textChanged.connect(self.set_text_changed)

        self.bars = {
            'File': Redactor.Bar('File', self.menuBar().addMenu('Файл'),
                                 'New, Open, Save, SaveAs, Sep, Close'),
            'Edit': Redactor.Bar('Edit', self.menuBar().addMenu('Правка'),
                                 'Cut, Copy, Paste, Sep, Undo, Redo'),
            'Format': Redactor.Bar('Format', self.addToolBar('Формат'),
                                   'Font, FontSize, FontColor')
        }

        for bar in self.bars.values():
            bar.add_qactions()
        self.initUI()

    def set_text_changed(self):
        self.is_saved = False

    def qwidgets_init(self):
        font = QtWidgets.QFontComboBox(self)
        font.currentFontChanged.connect(
            lambda f: self.text_edit.setCurrentFont(f))
        font_size = QtWidgets.QSpinBox(self)
        font_size.valueChanged.connect(
            lambda size: self.text_edit.setFontPointSize(size))
        font_size.setValue(14)
        Redactor.qwidget_name_to_qwidget = {
            'Font': font,
            'FontSize': font_size
        }

    def qactions_init(self):
        Redactor.qaction_name_to_qaction = {
            'New': self.get_qaction('icons/new.png', 'Создать',
                                    self.new_file,
                                    'Создать новый файл', 'CTRL+N'),
            'Open': self.get_qaction('icons/open.png', 'Открыть..',
                                     self.open_file,
                                     'Открыть файл', 'CTRL+O'),
            'Save': self.get_qaction('icons/save.png', 'Сохранить',
                                     self.save_current_file,
                                     'Сохранить файл', 'CTRL+S'),
            'SaveAs': self.get_qaction('icons/save.png', 'Сохранить как..',
                                       self.save_as_current_file,
                                       'Сохранить файл как', 'CTRL+SHIFT+S'),
            'Close': self.get_qaction('', 'Выход',
                                      self.redactor_exit,
                                      '', ''),
            'Cut': self.get_qaction('icons/cut.png', 'Вырезать',
                                    self.text_edit.cut,
                                    'Копировать в буфер обмена и удалить',
                                    'CTRL+X'),
            'Copy': self.get_qaction('icons/copy.png', 'Копировать',
                                     self.text_edit.copy,
                                     'Копировать в буфер обмена',
                                     'CTRL+C'),
            'Paste': self.get_qaction('icons/paste.png', 'Вставить',
                                      self.text_edit.paste,
                                      'Вставить из буфера обмена',
                                      'CTRL+V'),
            'Undo': self.get_qaction('icons/undo.png', 'Отменить',
                                     self.text_edit.undo,
                                     'Возвращает предыдущее состояние',
                                     'CTRL+Z'),
            'Redo': self.get_qaction('icons/redo.png', 'Вернуть',
                                     self.text_edit.redo,
                                     'Возвращает состояние до отмены',
                                     'CTRL+SHIFT+Z'),
            'FontColor': self.get_qaction('icons/font-color.png',
                                          'Изменить цвет шрифта',
                                          self.change_font_color)
        }

    def get_qaction(self, icon_path: str, name: str, action,
                    status_tip=None, short_cut=None):
        qaction = QAction(QIcon(icon_path), name, self)
        if status_tip:
            qaction.setStatusTip(status_tip)
        if short_cut:
            qaction.setShortcut(short_cut)
        qaction.triggered.connect(action)
        return qaction

    def initUI(self):
        self.setWindowTitle("Текстовый редактор")
        self.setGeometry(Redactor.get_qrect_for_window())

    @staticmethod
    def get_qrect_for_window():
        desktop = QApplication.desktop()
        return QRect(desktop.width() // 2 - Redactor._WINDOW_WIDTH // 2,
                     desktop.height() // 2 - Redactor._WINDOW_HEIGHT // 2,
                     Redactor._WINDOW_WIDTH,
                     Redactor._WINDOW_HEIGHT)

    def new_file(self):
        if not self._suggest_saving_file():
            return
        self.text_edit.clear()
        spawn = Redactor()
        spawn.show()

    def open_file(self):
        if not self._suggest_saving_file():
            return

        new_file_path = QFileDialog.getOpenFileName(
            self, 'Выбор файла', filter='(*.html *.txt *.log *.red)')[0]

        if new_file_path:
            self.text_edit.clear()
            with open(new_file_path, 'r') as file:
                self.text_edit.setText(file.read())
                self.is_saved = True

            self.file_name = new_file_path.split('/')[-1]
            self.file_path = new_file_path

            if not new_file_path.endswith(".red"):
                self.is_saved = False
                self.file_path = ''
                new_file_path += '.red'

    def _suggest_saving_file(self):
        if not self.is_saved:
            choice = QMessageBox.question(
                self, '',
                'Вы хотите сохранить изменения в "' + self.file_name + '"?',
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if choice == QMessageBox.Yes:
                return self.save_current_file()
            elif choice == QMessageBox.Cancel:
                return False
        return True

    def save_current_file(self):
        try:
            with open(self.file_path, 'w') as file:
                file.write(self.text_edit.toHtml())
                self.is_saved = True
                return True
        except FileNotFoundError:
            return self.save_as_current_file()

    def save_as_current_file(self):
        new_file_path = QFileDialog.getSaveFileName(self, 'Сохранение файла',
                                                    filter='*.red')[0]
        if new_file_path:
            self.file_path = new_file_path
            self.file_name = new_file_path.split('/')[-1]
            with open(self.file_path, 'w') as file:
                file.write(self.text_edit.toHtml())
                self.is_saved = True
                return True
        else:
            return False

    def change_font_color(self):
        color = QtWidgets.QColorDialog.getColor()
        self.text_edit.setTextColor(color)

    def redactor_exit(self):
        if self._suggest_saving_file():
            self.close()

    def closeEvent(self, event):
        if self._suggest_saving_file():
            event.accept()
        else:
            event.ignore()


def initialise_window():
    app = QApplication(sys.argv)
    redactor = Redactor()
    redactor.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    initialise_window()
