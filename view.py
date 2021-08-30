from PyQt5.QtWidgets import (
    QHBoxLayout,
    QPushButton, 
    QVBoxLayout, 
    QWidget
)

from widgets import DataTable, InsertDataDialog, DataFilter

import database as db

class InsertDataButton(QPushButton):

    def __init__(self, is_income, parent):

        text = "添加收入" if is_income else "添加支出"
        super(InsertDataButton, self).__init__(text, parent)
        self.is_income = is_income
        self.clicked.connect(self.pressButton)

    def pressButton(self):

        self.insertDialog = InsertDataDialog(self.is_income, self.parent())
        self.insertDialog.exec()

        self.insertDialog.destroy()


class View(QWidget):

    def __init__(self):
        super(View, self).__init__()
        
        self.resize(1200, 675)
        self.setWindowTitle("账本")
        self.mainlayout = QVBoxLayout()
        self.setLayout(self.mainlayout)

        self.init()

    def init(self):

        # inert buttons
        insertlayout = QHBoxLayout()
        insertlayout.addWidget(InsertDataButton(is_income=False, parent=self))
        insertlayout.addWidget(InsertDataButton(is_income=True, parent=self))

        datalayout = QHBoxLayout()
        # payment
        self.payData = DataTable(is_income=False)
        datalayout.addWidget(self.payData)
        # income
        self.inData = DataTable(is_income=True)
        datalayout.addWidget(self.inData)

        self.mainlayout.addLayout(insertlayout)
        self.mainlayout.addLayout(datalayout)
