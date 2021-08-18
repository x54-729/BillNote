from PyQt5.QtWidgets import (
    QAbstractItemView, 
    QHBoxLayout,
    QHeaderView, 
    QPushButton, 
    QTableWidget, 
    QTableWidgetItem, 
    QVBoxLayout, 
    QWidget
)

from bill_database import Database

class DataTable(QTableWidget):

    def __init__(self):

        super(DataTable, self).__init__()
        self.labels = ['日期', '类型', '分类', '支付方式', '描述', '金额']
        self.setColumnCount(len(self.labels))

        self.init()

    def init(self):

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        # may need to add QComboBox
        self.setHorizontalHeaderLabels(self.labels)

    def setItem(self, row, data_tuple):

        for i, data in enumerate(data_tuple):
            super().setItem(row, i, QTableWidgetItem(data))

    def setItems(self, data_list):

        self.setRowCount(len(data_list))
        for i, data_tuple in enumerate(data_list):
            self.setItem(i, data_tuple)

class InsertDataButton(QPushButton):

    def __init__(self, text):

        super(InsertDataButton, self).__init__(text)
        self.clicked.connect(self.pressButton)

    def pressButton(self):
        raise NotImplementedError

class View(QWidget):

    def __init__(self):
        super(View, self).__init__()
        
        self.resize(1200, 675)
        self.setWindowTitle("账本")
        self.mainlayout = QVBoxLayout()
        self.setLayout(self.mainlayout)
        self.db = Database("bills.db")

        self.init()

    def init(self):

        # inert button
        self.mainlayout.addWidget(InsertDataButton("添加记录"))
        self.mainlayout.addWidget(DataTable())
