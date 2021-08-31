import sys

from PyQt5.QtGui import QCursor
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMenu,
    QMessageBox,  
    QTableWidget, 
    QTableWidgetItem,
    QToolTip,
    QVBoxLayout,
    QWidget, 
    QPushButton
)

sys.path.append("../")
import database.bill_database as db
from .datadialog import ModifyDataDialog, InsertDataDialog

class DataTable(QTableWidget):

    def __init__(self, is_income, parent):

        super(DataTable, self).__init__(parent)
        self.sum = 0
        self.is_income = is_income
        self.datalist = []
        self.labels = ['id', '日期', '分类', '支付方式', '备注', '金额']
        self.setColumnCount(len(self.labels))
        self.hideColumn(0)

        self.init()

    def init(self):

        # 右键点击
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

        # 不可编辑
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 选中整行
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 自适应
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setHorizontalHeaderLabels(self.labels)
        # 悬停显示
        self.cellEntered.connect(self.showCellText)
        self.setMouseTracking(True)

        self.menu = DataTableContextMenu(self)

    def showCellText(self, row, col):
        text = self.item(row, col).text()
        QToolTip.showText(QCursor.pos(), text)

    def setItem(self, row, data_tuple):

        self.sum += data_tuple[-1]
        for i, data in enumerate(data_tuple):
            if isinstance(data, float):
                data = "{:.2f}".format(data)
            super().setItem(row, i, QTableWidgetItem(data))

    def setItems(self, data_list):

        self.sum = 0
        self.datalist = data_list
        self.setRowCount(len(data_list))
        for i, data_tuple in enumerate(data_list):
            self.setItem(i, data_tuple)

    def showContextMenu(self):

        self.menu.exec(QCursor.pos())


class DataTableContextMenu(QMenu):
    def __init__(self, parent):
        super(DataTableContextMenu, self).__init__(parent=parent)
        self.setFixedSize(130, 75)
        self.init()

    def init(self):

        self.mod = self.addAction("编辑")
        self.mod.triggered.connect(self.triggerModifyAction)
        self.dele = self.addAction("删除")
        self.dele.triggered.connect(self.triggerDelAction)

    def triggerModifyAction(self):

        idx = self.parent().currentRow()
        data = self.parent().datalist[idx]
        self.modDialog = ModifyDataDialog(
            is_income=self.parent().is_income, 
            parent=self.parent(),
            type_=data.type, method=data.method, 
            desc=data.description, amount=data.amount,
            id = data.id
            )
        self.modDialog.show()

    def triggerDelAction(self):

        reply = QMessageBox.question(self.parent(), '删除数据', '确认要删除这条数据吗？', QMessageBox.Yes|QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return
        idx = self.parent().currentRow()
        data = self.parent().datalist[idx]
        db.delete(data.id)
        self.parent().parent().update()

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

class DataArea(QWidget):
    def __init__(self, is_income, parent):
        super(DataArea, self).__init__(parent)

        self.is_income = is_income

        self.init()

    def init(self):

        self.table = DataTable(self.is_income, self.parent())
        self.button = InsertDataButton(self.is_income, self.parent())
        self.label = QLabel()

        topLayout = QHBoxLayout()
        topLayout.addWidget(self.button, alignment=QtCore.Qt.AlignLeft)
        topLayout.addWidget(self.label, alignment=QtCore.Qt.AlignRight)

        self.layout = QVBoxLayout()
        self.layout.addLayout(topLayout)
        self.layout.addWidget(self.table)

        self.setLayout(self.layout)

    def update(self, datalist):
        
        self.table.setItems(datalist)
        sum_ = self.table.sum
        if self.is_income:
            text = "共收入{:.2f}元"
        else:
            text = "共支出{:.2f}元"
        self.label.setText(text.format(sum_))
