import sys

from PyQt5.QtGui import QCursor
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QMenu,
    QMessageBox,  
    QTableWidget, 
    QTableWidgetItem, 
)

sys.path.append("../")
import database.bill_database as db
from .datadialog import ModifyDataDialog

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

        # right click
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setHorizontalHeaderLabels(self.labels)

        self.menu = DataTableContextMenu(self)

    def setItem(self, row, data_tuple):

        self.sum += data_tuple[-1]
        for i, data in enumerate(data_tuple):
            if isinstance(data, float):
                data = "{:.2f}".format(data)
            super().setItem(row, i, QTableWidgetItem(data))

    def setItems(self, data_list):

        self.sun = 0
        self.datalist = data_list
        self.setRowCount(len(data_list))
        for i, data_tuple in enumerate(data_list):
            self.setItem(i, data_tuple)

    def showContextMenu(self):

        self.menu.exec(QCursor.pos())

    def update(self):

        self.parent().update()


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
        self.parent().update()