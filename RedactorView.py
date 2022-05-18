import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QRect, QMimeData
from PyQt5.QtWidgets import (
    QApplication, QMainWindow,
    QTextEdit, QAction, QFileDialog, QMessageBox
)
from PyQt5.QtGui import QIcon, QFileOpenEvent, QFont
from PyQt5 import QtPrintSupport
from RedactorUtility import Bar


class RedactorView(QMainWindow):
    _WINDOW_WIDTH = 1000
    _WINDOW_HEIGHT = 800

    def __init__(self, model, controller, parent=None):
        QMainWindow.__init__(self, parent)
        self.text_edit = QTextEdit(self)
        self.controller = controller
        self.text_edit.textChanged.connect(self.controller.set_text_changed)
        self.model = model
        self.model.add_observer(self)
        self.mime_data = QMimeData()
        self.clipboard = QApplication.clipboard()
        self.qaction_name_to_qaction = dict()
        self.qwidget_name_to_qwidget = dict()
        self.bars = {
            'File': Bar('File', self.menuBar().addMenu('Файл'),
                        'New, Open, Save, SaveAs, Sep, Close'),
            'Edit': Bar('Edit', self.menuBar().addMenu('Правка'),
                        'Cut, Copy, Paste, Sep, Undo, Redo'),
            'Format': Bar('Format', self.addToolBar('Формат'),
                          'Font, FontSize, FontColor, Sep, Italic, '
                          'Underline, Bold, Strike')
        }
        self.qwidgets_connect()
        self.qactions_init()

    def initUI(self):
        self.setCentralWidget(self.text_edit)
        self.setWindowTitle("Текстовый редактор")
        self.setGeometry(RedactorView.get_qrect_for_window())
        for bar in self.bars.values():
            bar.add_UI_elements(self)

    def qwidgets_connect(self):
        qwidget_font = QtWidgets.QFontComboBox(self)
        qwidget_font_size = QtWidgets.QSpinBox(self)
        self.qwidget_name_to_qwidget = {
            'Font': qwidget_font,
            'FontSize': qwidget_font_size
        }
        self.qwidget_name_to_qwidget['Font'].currentFontChanged.connect(
            self.controller.change_font)
        self.qwidget_name_to_qwidget['FontSize'].valueChanged.connect(
            self.controller.change_font_size)
        self.qwidget_name_to_qwidget['FontSize'].setValue(14)



    def qactions_init(self):
        self.qaction_name_to_qaction = {
            'New': self.get_qaction('icons/new.png', 'Создать',
                                    self.controller.new_file,
                                    'Создать новый файл', 'CTRL+N'),
            'Open': self.get_qaction('icons/open.png', 'Открыть..',
                                     self.controller.open_file,
                                     'Открыть файл', 'CTRL+O'),
            'Save': self.get_qaction('icons/save.png', 'Сохранить',
                                     self.controller.save_current_file,
                                     'Сохранить файл', 'CTRL+S'),
            'SaveAs': self.get_qaction('icons/save.png', 'Сохранить как..',
                                       self.controller.save_as_current_file,
                                       'Сохранить файл как', 'CTRL+SHIFT+S'),
            'Close': self.get_qaction('', 'Выход',
                                      self.controller.redactor_exit,
                                      '', ''),
            'Cut': self.get_qaction('icons/cut.png', 'Вырезать',
                                    self.controller.cut,
                                    'Копировать в буфер обмена и удалить',
                                    'CTRL+X'),
            'Copy': self.get_qaction('icons/copy.png', 'Копировать',
                                     self.controller.copy,
                                     'Копировать в буфер обмена',
                                     'CTRL+C'),
            'Paste': self.get_qaction('icons/paste.png', 'Вставить',
                                      self.controller.paste,
                                      'Вставить из буфера обмена',
                                      'CTRL+V'),
            'Undo': self.get_qaction('icons/undo.png', 'Отменить',
                                     self.controller.undo,
                                     'Возвращает предыдущее состояние',
                                     'CTRL+Z'),
            'Redo': self.get_qaction('icons/redo.png', 'Вернуть',
                                     self.controller.redo,
                                     'Возвращает состояние до отмены',
                                     'CTRL+SHIFT+Z'),
            'FontColor': self.get_qaction('icons/font-color.png',
                                          'Изменить цвет шрифта',
                                          self.controller.change_font_color),
            'Italic': self.get_qaction('icons/italic.png', 'Курсив',
                                       self.controller.set_font_italic),
            'Underline': self.get_qaction('icons/underline.png',
                                          'Подчёркнутый',
                                          self.controller.set_font_underline),
            'Bold': self.get_qaction('icons/bold.png', 'Жирный',
                                     self.controller.set_font_bold),
            'Strike': self.get_qaction('icons/strike.png', 'Зачёркнутый',
                                       self.controller.set_font_strike)
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

    @staticmethod
    def get_qrect_for_window():
        desktop = QApplication.desktop()
        return QRect(desktop.width() // 2 - RedactorView._WINDOW_WIDTH // 2,
                     desktop.height() // 2 - RedactorView._WINDOW_HEIGHT // 2,
                     RedactorView._WINDOW_WIDTH,
                     RedactorView._WINDOW_HEIGHT)

    @staticmethod
    def show_error():
        errorbox = QtWidgets.QMessageBox()
        errorbox.setWindowTitle("Ошибка")
        errorbox.setText("Что-то пошло не так, "
                         "невозможно продолжить действие")
        errorbox.exec_()

    def get_open_file_name(self):
        return QFileDialog.getOpenFileName(
            self, 'Выбор файла', filter='(*.html *.txt *.log *.red)')[0]

    def get_save_file_name(self):
        return QFileDialog.getSaveFileName(self, 'Сохранение файла',
                                           filter='*.red')[0]

    def suggest_saving_file_message(self):
        return QMessageBox.question(
            self, '',
            'Вы хотите сохранить изменения в "' + self.model.file_name
            + '"?',
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

    def closeEvent(self, event):
        if self.controller.suggest_saving_file():
            event.accept()
        else:
            event.ignore()
