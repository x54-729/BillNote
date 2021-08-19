from PyQt5.QtGui import QDoubleValidator
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QDialog,
    QGridLayout, 
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit, 
    QPushButton, 
    QTableWidget, 
    QTableWidgetItem, 
    QVBoxLayout, 
    QWidget
)

import bill_database as db

class DataTable(QTableWidget):

    def __init__(self):

        super(DataTable, self).__init__()
        self.sum = 0
        self.labels = ['id', '日期', '分类', '支付方式', '备注', '金额']
        self.setColumnCount(len(self.labels))
        self.hideColumn(0)

        self.init()
        self.update()

    def init(self):

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setHorizontalHeaderLabels(self.labels)

    def setItem(self, row, data_tuple):

        self.sum += data_tuple[-1]
        for i, data in enumerate(data_tuple):
            super().setItem(row, i, QTableWidgetItem(str(data)))

    def setItems(self, data_list):

        self.setRowCount(len(data_list))
        for i, data_tuple in enumerate(data_list):
            self.setItem(i, data_tuple)

    def update(self):

        raise NotImplementedError

class InDataTable(DataTable):

    def __init__(self):
        super(InDataTable, self).__init__()

    def update(self):

        self.sum = 0
        data = db.find_by_is_income(is_income=True)
        self.setItems(data)

class PayDataTable(DataTable):

    def __init__(self):
        super(PayDataTable, self).__init__()

    def update(self):

        self.sum = 0
        data = db.find_by_is_income(is_income=False)
        self.setItems(data)

class InsertBox(QDialog):
    def __init__(self, is_income, parent):
        super(InsertBox, self).__init__(parent=parent)

        self.setFixedSize(600, 170)
        self.setWindowTitle("输入数据")
        self.types = ["娱乐", "游戏", "生活", "食物"]
        self.methods = ["支付宝", "微信", "现金"]
        self.is_income = is_income

        self.init()

    def init(self):

        self.typeLabel = QLabel("分类：")
        self.typeComboBox = QComboBox()
        self.typeComboBox.addItems(self.types)

        self.methodLabel = QLabel("支付方式：")
        self.methodComboBox = QComboBox()
        self.methodComboBox.addItems(self.methods)

        self.descLabel = QLabel("备注：")
        self.descLine = QLineEdit()
        self.descLine.setMaxLength(10)

        self.amountLabel = QLabel("金额：")
        self.amountLine = QLineEdit()
        self.amountLine.setValidator(QDoubleValidator())

        self.confirmButton = QPushButton("确认")
        self.confirmButton.clicked.connect(self.pressConfirmButton)

        toplayout = QHBoxLayout()
        toplayout.addWidget(self.typeLabel)
        toplayout.addWidget(self.typeComboBox)
        toplayout.addWidget(self.methodLabel)
        toplayout.addWidget(self.methodComboBox)
        toplayout.addWidget(self.amountLabel)
        toplayout.addWidget(self.amountLine)
        self.layout = QVBoxLayout()
        self.layout.addLayout(toplayout)
        self.layout.addWidget(self.descLabel, alignment=QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.descLine)
        self.layout.addWidget(self.confirmButton, alignment=QtCore.Qt.AlignCenter)

        self.setLayout(self.layout)

    def pressConfirmButton(self):

        db.insert(
            self.typeComboBox.currentText(),
            self.methodComboBox.currentText(),
            self.descLine.text(),
            self.amountLine.text(),
            self.is_income
            )

        if self.is_income:
            self.parent().inData.update()
        else:
            self.parent().payData.update()


class InsertDataButton(QPushButton):

    def __init__(self, is_income, parent):

        text = "添加收入" if is_income else "添加支出"
        super(InsertDataButton, self).__init__(text, parent)
        self.is_income = is_income
        self.clicked.connect(self.pressButton)

    def pressButton(self):

        self.insertBox = InsertBox(self.is_income, self.parent())
        self.insertBox.exec()

        self.insertBox.destroy()

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
        self.payData = PayDataTable()
        datalayout.addWidget(self.payData)
        # income
        self.inData = InDataTable()
        datalayout.addWidget(self.inData)

        self.mainlayout.addLayout(insertlayout)
        self.mainlayout.addLayout(datalayout)
