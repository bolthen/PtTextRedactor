import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QRect, QMimeData
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFontDialog,
    QTextEdit, QAction, QFileDialog
)
from PyQt5.QtGui import QIcon
from PyQt5 import QtPrintSupport


class Redactor(QMainWindow):
    _WINDOW_WIDTH = 1000
    _WINDOW_HEIGHT = 800

    qaction_name_to_qaction = dict()

    '''class FileMenuActions:
        def __init__(self, parent):
            self.parent = parent
            self.menu = self.parent.file_menu
            self.new_file = QAction('Создать', self.parent)
            self.open_file = QAction('Открыть...', self.parent)
            self.save_file = QAction('Сохранить', self.parent)
            self.save_file_as = QAction('Сохранить как...', self.parent)
            self.close_file = QAction('Выход', self.parent)
            self._add_to_parent()

        def _add_to_parent(self):
            self.menu.addAction(self.new_file)
            self.menu.addAction(self.open_file)
            self.menu.addAction(self.save_file)
            self.menu.addAction(self.save_file_as)
            self.menu.addSeparator()
            self.menu.addAction(self.close_file)

    class EditMenuActions:
        def __init__(self, parent):
            self.parent = parent
            self.menu = self.parent.edit_menu
            self.undo = QAction('Отменить', self.parent)
            self.cut = QAction('Вырезать', self.parent)
            self.copy = QAction('Скопировать', self.parent)
            self.paste = QAction('Вставить', self.parent)
            self.font = QAction('Шрифт', self.parent)
            self.color = QAction('Цвет', self.parent)
            self._add_to_parent()

        def _add_to_parent(self):
            self.menu.addAction(self.undo)
            self.menu.addSeparator()
            self.menu.addAction(self.cut)
            self.menu.addAction(self.copy)
            self.menu.addAction(self.paste)
            self.menu.addSeparator()
            self.menu.addAction(self.font)
            self.menu.addAction(self.color)'''

    class Bar:
        def __init__(self, name: str, bar, qactions: str):
            self.bar_name = name
            self.qactions = qactions
            self.parent_bar = bar

        def add_qactions(self):
            for action in self.qactions.split(', '):
                if action == 'Sep':
                    self.parent_bar.addSeparator()
                else:
                    if action not in Redactor.qaction_name_to_qaction:
                        continue
                    self.parent_bar.addAction(
                        Redactor.qaction_name_to_qaction[action])

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.file_name = None
        '''self.file_menu = self.menuBar().addMenu('Файл')
        self.edit_menu = self.menuBar().addMenu('Правка')
        self.file_toolbar = self.addToolBar('Файл')
        self.edit_toolbar = self.addToolBar('Правка')'''

        # self.status_bar = self.statusBar()

        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)

        self.mime_data = QMimeData()
        self.clipboard = QApplication.clipboard()

        # self.file_menu_actions = Redactor.FileMenuActions(self)
        # self.edit_menu_actions = Redactor.EditMenuActions(self)

        self.qations_init()
        self.bars = {
            'File': Redactor.Bar('File', self.menuBar().addMenu('Файл'),
                                 'New, Open, Save, SaveAs'),
            'Edit': Redactor.Bar('Edit', self.menuBar().addMenu('Правка'),
                                 'Cut, Copy, Paste, Sep, Undo, Redo')
        }

        for bar in self.bars.values():
            bar.add_qactions()

        '''self.new_file = QAction('Создать', self)
        self.open_file = QAction('Открыть...', self)
        self.save_file = QAction('Сохранить', self)
        self.save_file_as = QAction('Сохранить как...', self)
        self.close_file = QAction('Выход', self)

        self.cut_action = QAction('Cut', self)
        self.copy_action = QAction('Copy', self)
        self.paste_action = QAction('Paste', self)
        self.font_action = QAction('Font', self)
        self.color_action = QAction('Color', self)
        self.about_action = QAction('Qt', self)'''

        self.initUI()

    def qations_init(self):
        Redactor.qaction_name_to_qaction = {
            'New': self.get_qaction('icons/new.png', 'Создать', self.new_file,
                                    'Создать новый файл', 'CTRL+N'),
            'Open': self.get_qaction('icons/open.png', 'Открыть..',
                                     self.open_file,
                                     'Открыть файл', 'CTRL+O'),
            'Save': self.get_qaction('icons/save.png', 'Сохранить',
                                     self.save_file,
                                     'Сохранить файл', 'CTRL+S'),
            'SaveAs': self.get_qaction('icons/save.png', 'Сохранить как',
                                       self.save_as_file,
                                       'Сохранить файл в новом экземпляре',
                                       'CTRL+SHIFT+S'),
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
                                     'CTRL+SHIFT+Z')
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

    def menu_init(self):
        pass
        '''self.file_menu.addAction(self.new_file)
        self.file_menu.addAction(self.open_file)
        self.file_menu.addAction(self.save_file)
        self.file_menu.addAction(self.save_file_as)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.close_file)

        self.edit_menu.addAction(self.cut_action)
        self.edit_menu.addAction(self.copy_action)
        self.edit_menu.addAction(self.paste_action)
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(self.font_action)
        self.edit_menu.addAction(self.color_action)'''

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
        redactor = Redactor(self)
        redactor.show()

    def open_file(self):
        self.file_name = QFileDialog.getOpenFileName(self, 'Выбор файла',
                                                     filter="(*.writer)")[0]

        if self.file_name:
            with open(self.file_name, "r") as file:
                data = file.read()
                self.text_edit.setText(data)

    def save_file(self):
        if not self.file_name:
            self.file_name = QFileDialog.getSaveFileName(self,
                                                         'Сохранение файла')[0]
        self.write_to_fail()

    def save_as_file(self):
        self.file_name = QFileDialog.getSaveFileName(self,
                                                     'Сохранение файла')[0]
        self.write_to_fail()

    def write_to_fail(self):
        if self.file_name:
            if not self.file_name.endswith(".writer"):
                self.file_name += ".writer"

            with open(self.file_name, "w") as file:
                file.write(self.text_edit.toHtml())


def initialise_window():
    app = QApplication(sys.argv)
    redactor = Redactor()
    redactor.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    initialise_window()
