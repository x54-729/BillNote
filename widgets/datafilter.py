import sys

from PyQt5.QtCore import QDate
from PyQt5 import QtCore
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import (
    QGridLayout,
    QPushButton,
    QWidget,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QDateEdit,
)

import database as db

sys.path.append("../")
from .common import LabelComboBox

class TimeFilter(QWidget):
    def __init__(self, parent):
        super(TimeFilter, self).__init__(parent)

        self.choices = ["本日", "本月", "本年", "自定义（闭区间）"]
        self.init()

    def init(self):

        self.dateEdit = LabelComboBox(self, "时间范围：", self.choices)
        self.dateEdit.comboBox.activated.connect(self.chooseDateRange)

        self.fromCalendar = QDateEdit(self.today(), self)
        self.fromCalendar.setCalendarPopup(True)
        self.fromCalendar.setDisplayFormat('yyyy-MM-dd')
        self.connectLabel = QLabel("~")
        self.toCalendar = QDateEdit(self.today(), self)
        self.toCalendar.setCalendarPopup(True)
        self.toCalendar.setDisplayFormat('yyyy-MM-dd')

        calendarLayout = QHBoxLayout()
        calendarLayout.addWidget(self.fromCalendar, alignment=QtCore.Qt.AlignLeft)
        calendarLayout.addWidget(self.connectLabel, alignment=QtCore.Qt.AlignLeft)
        calendarLayout.addWidget(self.toCalendar, alignment=QtCore.Qt.AlignLeft)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.dateEdit)
        self.layout.addLayout(calendarLayout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.setCalendarsVisible(False)

    def setCalendarsVisible(self, flag):

        self.fromCalendar.setVisible(flag)
        self.connectLabel.setVisible(flag)
        self.toCalendar.setVisible(flag)

    def today(self):

        return QDate.currentDate()

    def startOfMonth(self):

        return QDate(self.today().year(), self.today().month(), 1)

    def endOfMonth(self):
        
        return QDate(self.today().year(), self.today().month(), self.today().daysInMonth())

    def startOfYear(self):
        
        return QDate(self.today().year(), 1, 1)

    def endOfYear(self):
        
        return QDate(self.today().year(), 12, 31)

    def chooseDateRange(self):

        text = self.dateEdit.text()
        if text == "本日":
            self.fromCalendar.setDate(self.today())
            self.toCalendar.setDate(self.today())
            self.setCalendarsVisible(False)
        elif text == "本月":
            self.fromCalendar.setDate(self.startOfMonth())
            self.toCalendar.setDate(self.endOfMonth())
            self.setCalendarsVisible(False)
        elif text == "本年":
            self.fromCalendar.setDate(self.startOfYear())
            self.toCalendar.setDate(self.endOfYear())
            self.setCalendarsVisible(False)
        elif text == "自定义（闭区间）":
            self.setCalendarsVisible(True)
        else:
            raise NotImplementedError

    def text(self):

        return self.fromCalendar.text(), self.toCalendar.text()


class AmountFilter(QWidget):
    def __init__(self, parent):
        super(AmountFilter, self).__init__(parent)

        self.init()

    def init(self):
        
        self.label = QLabel("金额：")
        self.connectLabel = QLabel("~")
        self.fromLine = QLineEdit()
        self.fromLine.setValidator(QDoubleValidator())
        self.fromLine.setText("0")
        self.toLine = QLineEdit()
        self.toLine.setValidator(QDoubleValidator())
        self.toLine.setText("10000")

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.fromLine)
        self.layout.addWidget(self.connectLabel)
        self.layout.addWidget(self.toLine)

        self.setLayout(self.layout)

    def text(self):

        return float(self.fromLine.text()), float(self.toLine.text())

class DataFilter(QWidget):
    def __init__(self, parent):
        super(DataFilter, self).__init__(parent)

        self.types = ["全部", "娱乐", "游戏", "生活", "食物"]
        self.methods = ["全部", "支付宝", "微信", "现金"]
        self.init()

    def init(self):

        # 筛选时间
        self.timeFilter = TimeFilter(self)

        # 筛选支付方式
        self.methodFilter = LabelComboBox(self, "支付方式：", self.methods, "全部")

        # 筛选类别
        self.inTypeFilter = LabelComboBox(self, "分类：", self.types, "全部")
        self.payTypeFilter = LabelComboBox(self, "分类：", self.types, "全部")

        # 筛选金额
        self.inAmountFilter = AmountFilter(self)
        self.payAmountFilter = AmountFilter(self)

        self.filterButton = QPushButton(text="应用筛选", parent=self)
        self.filterButton.clicked.connect(self.pressFilterButton)

        firstRowLayout = QHBoxLayout()
        firstRowLayout.addWidget(self.timeFilter, alignment=QtCore.Qt.AlignLeft)
        firstRowLayout.addWidget(self.methodFilter, alignment=QtCore.Qt.AlignLeft)
        firstRowLayout.setContentsMargins(0, 0, 0, 0)

        secondRowLayout = QHBoxLayout()
        secondRowLayout.addWidget(self.payTypeFilter)
        secondRowLayout.addWidget(self.payAmountFilter)
        secondRowLayout.addWidget(self.inTypeFilter)
        secondRowLayout.addWidget(self.inAmountFilter)
        secondRowLayout.setContentsMargins(0, 0, 0, 0)

        layout = QVBoxLayout()
        layout.addLayout(firstRowLayout)
        layout.addLayout(secondRowLayout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.filterButton, alignment=QtCore.Qt.AlignCenter)

        self.layout = layout
        self.setLayout(self.layout)

    def get_data(self):

        fromDate, toDate = self.timeFilter.text()
        inFromAmount, inToAmount = self.inAmountFilter.text()
        payFromAmount, payToAmount = self.payAmountFilter.text()
        method = self.methodFilter.text()
        inType = self.inTypeFilter.text()
        payType = self.payTypeFilter.text()

        inDataList = db.find_by_filters(fromDate, toDate, inType, method, inFromAmount, inToAmount, True)
        payDataList = db.find_by_filters(fromDate, toDate, payType, method, payFromAmount, payToAmount, False)

        return inDataList, payDataList

    def pressFilterButton(self):

        self.parent().update()