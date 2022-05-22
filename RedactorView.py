from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QRect, QMimeData
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLayout, QGridLayout, QHBoxLayout, QVBoxLayout,
    QTextEdit, QAction, QFileDialog, QMessageBox, QLabel, QPushButton, QStyle,
    QStatusBar
)
from PyQt5.QtGui import QIcon, QTextCursor, QFont, QPalette, QColor

import RedactorUtility
from RedactorUtility import Bar, T9
from difflib import get_close_matches


class RedactorView(QMainWindow):
    _WINDOW_WIDTH = 1000
    _WINDOW_HEIGHT = 800

    def __init__(self, model, controller, parent=None):
        QMainWindow.__init__(self, parent)
        self.main_form = None
        self.t9_buttons_count = 3
        self.model = model
        self.controller = controller
        self.text_edit = QTextEdit(self)
        self.text_edit.textChanged.connect(self.controller.set_text_changed)
        p = self.text_edit.palette()
        p.setColor(QPalette.Highlight, QColor("blue"))
        self.text_edit.setPalette(p)
        self.text_edit.cursorPositionChanged.connect(
            self.controller.on_cursor_changed)
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
                          'Underline, Bold, Strike, Find')
        }
        self.qwidgets_connect()
        self.qactions_init()
        self.model.add_observer(self)

    def init_UI(self):
        self.main_form = RedactorWindowWidget(self)

        self.setCentralWidget(self.main_form)
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
        qwidget_font_size.setValue(14)
        self.text_edit.setFontPointSize(14)
        self.qwidget_name_to_qwidget['Font'].currentFontChanged.connect(
            self.controller.change_font)
        self.qwidget_name_to_qwidget['FontSize'].textChanged.connect(
            self.controller.change_font_size)

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
                                       self.controller.set_font_strike),
            'Find': self.get_qaction('icons/find.png', 'Поиск',
                                     RedactorUtility.Find(self).show,
                                     'Ищет совпадения', 'CTRL+F')
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
            self, self.model.file_name,
            'Вы хотите сохранить изменения в "' + self.model.file_name
            + '"?',
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

    def closeEvent(self, event):
        self.controller.on_close_event(event)


class RedactorWindowWidget(QtWidgets.QWidget):
    def __init__(self, view):
        super(RedactorWindowWidget, self).__init__(view)
        self.form = QVBoxLayout(self)
        self.form.addWidget(view.text_edit)
        self.helps = QHBoxLayout(self)
        self.buttons = []

        for i in range(view.t9_buttons_count):
            button = RedactorWindowWidget.get_new_t9_button()
            button.clicked.connect(
                lambda _: view.controller.t9_button_clicked(self.sender()))
            self.buttons.append(button)
            self.helps.addWidget(button)

        self.form.addLayout(self.helps)
        self.setLayout(self.form)

    def update_buttons(self, words):
        for word, button in zip(words, self.buttons):
            button.setText(word)

    @staticmethod
    def get_new_t9_button():
        button = QPushButton('')
        button.setStyleSheet('QPushButton {'
                             'border: 2px solid #8f8f91;'
                             'border-radius: 15px'
                             '}'
                             'QPushButton:pressed {'
                             'background-color: #c7c7c7;'
                             '}')

        button.setFixedHeight(40)
        button.setFont(QFont('Arial', 16))
        return button
