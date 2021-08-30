import sys

from PyQt5.QtGui import QDoubleValidator
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QComboBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox, 
    QPushButton, 
    QVBoxLayout, 
)

sys.path.append("../")
import database as db


class DataDialog(QDialog):
    def __init__(self, is_income, parent, type_=None, method=None, desc=None, amount=None):
        super(DataDialog, self).__init__(parent=parent)

        self.setFixedSize(600, 170)
        self.types = ["娱乐", "游戏", "生活", "食物"]
        self.methods = ["支付宝", "微信", "现金"]
        self.is_income = is_income

        self.type = type_
        self.method = method
        self.desc = desc
        self.amount = amount

        self.init()

    def init(self):

        self.typeLabel = QLabel("分类：")
        self.typeComboBox = QComboBox()
        self.typeComboBox.addItems(self.types)
        self.typeComboBox.setCurrentText(self.type)

        self.methodLabel = QLabel("支付方式：")
        self.methodComboBox = QComboBox()
        self.methodComboBox.addItems(self.methods)
        self.methodComboBox.setCurrentText(self.method)

        self.descLabel = QLabel("备注：")
        self.descLine = QLineEdit()
        self.descLine.setMaxLength(10)
        if self.desc is not None:
            self.descLine.setText(self.desc)

        self.amountLabel = QLabel("金额：")
        self.amountLine = QLineEdit()
        self.amountLine.setValidator(QDoubleValidator())
        if self.amount is not None:
            self.amountLine.setText("{:.2f}".format(self.amount))

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

    def get_data(self):
        
        return self.typeComboBox.currentText(), self.methodComboBox.currentText(),\
                self.descLine.text(), self.amountLine.text()

    def pressConfirmButton(self):

        raise NotImplementedError

class InsertDataDialog(DataDialog):
    def __init__(self, is_income, parent):
        super(InsertDataDialog, self).__init__(is_income, parent)
        self.setWindowTitle("输入数据")

    def pressConfirmButton(self):

        if self.amountLine.text() == "":
            QMessageBox.warning(self.parent(), '输入数据', '金额不能为空！', QMessageBox.Yes, QMessageBox.Yes)
            return

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
            
        self.close()

class ModifyDataDialog(DataDialog):
    def __init__(self, is_income, parent, type_, method, desc, amount, id):
        super(ModifyDataDialog, self).__init__(is_income, parent, type_, method, desc, amount)
        self.setWindowTitle("修改数据")
        self.id = id

    def pressConfirmButton(self):

        if self.amountLine.text() == "":
            QMessageBox.warning(self.parent(), '修改数据', '金额不能为空！', QMessageBox.Yes, QMessageBox.Yes)
            return

        reply = QMessageBox.question(self.parent(), '修改数据', '确认要修改这条数据吗？', QMessageBox.Yes|QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return

        db.change(
            self.id,
            self.typeComboBox.currentText(),
            self.methodComboBox.currentText(),
            self.descLine.text(),
            self.amountLine.text(),
            )

        self.parent().update()
            
        self.close()