from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
)

class LabelComboBox(QWidget):
    def __init__(self, parent, text, items, icons=None, default_item = None, horizontal = True):
        super(LabelComboBox, self).__init__(parent=parent)
        assert default_item is None or default_item in items
        if icons is not None:
            assert len(icons) == len(items)

        self.label = QLabel(text)
        self.comboBox = QComboBox()
        self.items = items
        self.icons = icons
        self.default = default_item

        self.layout = QHBoxLayout() if horizontal else QVBoxLayout()

        self.init()

    def init(self):

        if self.icons is None:
            self.comboBox.addItems(self.items)
        else:
            for icon, text in zip(self.icons, self.items):
                self.comboBox.addItem(QIcon(icon), text)
        if self.default is not None:
            self.comboBox.setCurrentText(self.default)

        self.layout.setContentsMargins(0, 2, 0, 2)
        self.layout.addWidget(self.label, alignment=QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.comboBox, alignment=QtCore.Qt.AlignLeft)
        self.setLayout(self.layout)

        self.setStyleSheet('''
            QComboBox{
                padding-top: 2px;
                padding-bottom: 2px;
                padding-left: 5px;
                padding-right: 5px;
                border-radius: 5px;
                border: 1px solid black;
                font-weight:1000;
                font-family:"STKaiti";
            }
            QComboBox::drop-down{
                padding: 0px;
                border-radius: 5px;
                width: 20px;
            }
            QComboBox::down-arrow{
                image: url('./icons/drop-combobox');
                height: 15px;
                width: 15px;
            }
        ''')

    def text(self):

        return self.comboBox.currentText()

        