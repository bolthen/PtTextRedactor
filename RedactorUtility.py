import re


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
    words_regex = re.compile(r'[A-Za-zА-Яа-я]{2,}')

    @staticmethod
    def init_T9(words_source):
        with open(words_source, 'r', encoding='UTF-8') as f:
            for i, k, in enumerate(f.readlines()):
                words = T9.words_regex.findall(k)
                for j in words:
                    T9.data.add(j.lower())
