import re
from difflib import get_close_matches
from PyQt5.QtWidgets import QMessageBox
import os.path
from RedactorUtility import FileOpener


class T9:
    data = set()
    _words_regex = re.compile(r'[A-Za-zА-Яа-я]{2,}')
    view = None

    @staticmethod
    def get_similar_words(word, count):
        return get_close_matches(word, T9.data, count)

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
    def set_t9_words_data_by_default():
        cfg_path = T9._get_t9_cfg_path()
        if cfg_path is None or os.path.exists(cfg_path) is False:
            choice = T9.view.suggest_choose_t9_data()
            if choice == QMessageBox.No:
                T9.view.notify_about_t9()
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
