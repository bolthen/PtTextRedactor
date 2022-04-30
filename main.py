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

        self.text_edit = QTextEdit(self)
        self.mime_data = QMimeData()
        self.clipboard = QApplication.clipboard()
        self.file_name = "Безымянный.txt"
        self.file_path = ""
        self.is_saved = True

        self.setCentralWidget(self.text_edit)
        self.qations_init()
        self.text_edit.textChanged.connect(self.set_text_changed)

        self.bars = {
            'File': Redactor.Bar('File', self.menuBar().addMenu('Файл'),
                                 'New, Open, Save, SaveAs, Sep, Close'),
            'Edit': Redactor.Bar('Edit', self.menuBar().addMenu('Правка'),
                                 'Cut, Copy, Paste, Sep, Undo, Redo')
        }

        for bar in self.bars.values():
            bar.add_qactions()

        self.initUI()

    def set_text_changed(self):
        if self.text_edit.toPlainText():
            self.is_saved = False
        else:
            self.is_saved = True

    def qations_init(self):
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
        spawn = Redactor()
        spawn.show()

    def open_file(self):
        new_file_path, _ = QFileDialog.getOpenFileName(self, 'Open File',
                                                       './', 'Files (*.txt)')

        if not self._suggest_saving_file():
            return

        if new_file_path:
            self.text_edit.clear()
            self.file_path = new_file_path
            self.file_name = new_file_path.split('/')[-1]
            with open(self.file_path, 'r') as file:
                self.text_edit.setText(file.read())

    def _suggest_saving_file(self):
        if not self.is_saved:
            choice = QMessageBox.question(
                self, '',
                'Вы хотите сохранить изменения в "' + self.file_name + '"?',
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if choice == QMessageBox.Yes:
                self.save_current_file()
            elif choice == QMessageBox.No:
                self.text_edit.clear()
            else:
                return False
        return True

    def save_current_file(self):
        try:
            with open(self.file_path, 'w') as file:
                file.write(self.text_edit.toPlainText())
        except FileNotFoundError:
            self.save_as_current_file()

    def save_as_current_file(self):
        self.file_path, _ = QFileDialog.getSaveFileName(self, 'Save File',
                                                        './', 'Files (*.txt)')
        if self.file_path:
            with open(self.file_path, 'w') as f:
                f.write(self.text_edit.toPlainText())
                self.is_saved = True

    def redactor_exit(self):
        if self._suggest_saving_file():
            self.close()


def initialise_window():
    app = QApplication(sys.argv)
    redactor = Redactor()
    redactor.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    initialise_window()
