from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QWidget,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
)

class LabelComboBox(QWidget):
    def __init__(self, parent, text, items, default_item = None, horizontal = True):
        super(LabelComboBox, self).__init__(parent=parent)
        assert default_item is None or default_item in items
        self.label = QLabel(text)
        self.comboBox = QComboBox()
        self.items = items
        self.default = default_item

        self.layout = QHBoxLayout() if horizontal else QVBoxLayout()

        self.init()

    def init(self):

        self.comboBox.addItems(self.items)
        if self.default is not None:
            self.comboBox.setCurrentText(self.default)

        self.layout.addWidget(self.label, alignment=QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.comboBox, alignment=QtCore.Qt.AlignLeft)
        self.setLayout(self.layout)

    def text(self):

        return self.comboBox.currentText()

        