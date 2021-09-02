import sys

from PyQt5.QtGui import QDoubleValidator
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
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
from .common import LabelComboBox


class DataDialog(QDialog):
    def __init__(self, is_income, parent, type_=None, method=None, desc=None, amount=None):
        super(DataDialog, self).__init__(parent=parent)

        self.setFixedSize(380, 130)
        self.types = ["娱乐", "游戏", "生活", "食物"]
        self.type_icons = [
            "icons/entertainment.svg",
            "icons/game.svg",
            "icons/living.svg",
            "icons/food.svg"
        ]
        self.methods = ["支付宝", "微信", "现金"]
        self.method_icons = [
            "icons/alipay.svg",
            "icons/wechat.svg",
            "icons/cash.svg"
        ]
        self.is_income = is_income

        self.type = type_
        self.method = method
        self.desc = desc
        self.amount = amount

        self.init()

    def init(self):

        self.typeEdit = LabelComboBox(self, "分类：", self.types, self.type_icons, self.type)

        self.methodEdit = LabelComboBox(self, "支付方式：", self.methods, self.method_icons, self.method)

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
        toplayout.addWidget(self.typeEdit)
        toplayout.addWidget(self.methodEdit)
        toplayout.addWidget(self.amountLabel)
        toplayout.addWidget(self.amountLine)
        self.layout = QVBoxLayout()
        self.layout.addLayout(toplayout)
        self.layout.addWidget(self.descLabel, alignment=QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.descLine)
        self.layout.addWidget(self.confirmButton, alignment=QtCore.Qt.AlignCenter)

        self.setLayout(self.layout)

    def get_text(self):
        
        return self.typeEdit.text(), self.methodEdit.text(),\
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
            self.typeEdit.text(),
            self.methodEdit.text(),
            self.descLine.text(),
            self.amountLine.text(),
            self.is_income
            )

        self.parent().parent().update()
            
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
            self.typeEdit.text(),
            self.methodEdit.text(),
            self.descLine.text(),
            self.amountLine.text(),
            )

        self.parent().update()
            
        self.close()