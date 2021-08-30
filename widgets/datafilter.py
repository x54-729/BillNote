import sys

from PyQt5.QtCore import QDate
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import (
    QWidget,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QDateEdit,
    QCalendarWidget
)

import database as db

sys.path.append("../")

class TimeFilter(QWidget):
    def __init__(self, parent):
        super(TimeFilter, self).__init__(parent)

        self.choices = ["本日", "本月", "本年", "自定义（闭区间）"]
        self.current = QDate.currentDate()
        self.init()

    def init(self):

        self.label = QLabel("时间范围：")
        self.dateComboBox = QComboBox()
        self.dateComboBox.addItems(self.choices)
        self.dateComboBox.activated.connect(self.chooseDateRange)
        self.dateComboBox.setCurrentText("本日")

        self.fromCalendar = QDateEdit(self)
        self.fromCalendar.setCalendarPopup(True)
        self.fromCalendar.setDisplayFormat('yyyy-MM-dd')
        self.connectLabel = QLabel("~")
        self.toCalendar = QDateEdit(self)
        self.toCalendar.setCalendarPopup(True)
        self.toCalendar.setDisplayFormat('yyyy-MM-dd')

        firstLayout = QHBoxLayout()
        firstLayout.addWidget(self.label)
        firstLayout.addWidget(self.dateComboBox)

        calendarLayout = QHBoxLayout()
        calendarLayout.addWidget(self.fromCalendar)
        calendarLayout.addWidget(self.connectLabel)
        calendarLayout.addWidget(self.toCalendar)

        self.layout = QVBoxLayout()
        self.layout.addLayout(firstLayout)
        self.layout.addWidget(self.calendarLabel)
        self.layout.addLayout(calendarLayout)

    def setCalendarsVisible(self, flag):

        self.fromCalendar.setVisible(flag)
        self.connectLabel.setVisible(flag)
        self.toCalendar.setVisible(flag)

    def startOfMonth(self):

        return QDate(self.current.year(), self.current.month(), 1)

    def endOfMonth(self):
        
        return QDate(self.current.year(), self.current.month(), self.current.daysInMonth())

    def startOfYear(self):
        
        return QDate(self.current.year(), 1, 1)

    def endOfYear(self):
        
        return QDate(self.current.year(), 12, 31)

    def chooseDateRange(self):

        text = self.dateComboBox.currentText()
        if text == "本日":
            self.fromCalendar.setSelectedDate(self.current)
            self.toCalendar.setSelectedDate(self.current)
            self.setCalendarsVisible(False)
        elif text == "本月":
            self.fromCalendar.setSelectedDate(self.startOfMonth())
            self.toCalendar.setSelectedDate(self.endOfMonth())
            self.setCalendarsVisible(False)
        elif text == "本年":
            self.fromCalendar.setSelectedDate(self.startOfYear())
            self.toCalendar.setSelectedDate(self.endOfYear())
            self.setCalendarsVisible(False)
        elif text == "自定义":
            self.setCalendarsVisible(True)
        else:
            raise NotImplementedError

    def data(self):

        return self.fromCalendar.text(), self.fromCalendar.text()


class AmountFilter(QWidget):
    def __init__(self, parent):
        super(TimeFilter, self).__init__(parent)

        self.init()

    def init(self):
        
        self.label = QLabel("金额：")
        self.connectLabel = QLabel("~")
        self.fromLine = QLineEdit()
        self.fromLine.setValidator(QDoubleValidator())
        self.toLine = QLineEdit()
        self.toLine.setValidator(QDoubleValidator())

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.fromLine)
        self.layout.addWidget(self.connectLabel)
        self.layout.addWidget(self.toLine)

    def data(self):

        return self.fromLine.text(), self.toLine.text()

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
        self.methodFilterLabel = QLabel("支付方式：")
        self.methodFilterComboBox = QComboBox()
        self.methodFilterComboBox.addItems(self.methods)

        # 筛选类别
        self.inTypeFilterLabel = QLabel("分类：")
        self.inTypeFilterComboBox = QComboBox()
        self.inTypeFilterComboBox.addItems(self.types)

        self.payTypeFilterLabel = QLabel("分类：")
        self.payTypeFilterComboBox = QComboBox()
        self.payTypeFilterComboBox.addItems(self.types)

        # 筛选金额
        self.inAmountFilter = AmountFilter(self)
        self.payAmountFilter = AmountFilter(self)

    def get_data(self):

        fromDate, toDate = self.timeFilter.data()
        inFromAmount, inToAmount = self.inAmountFilter.data()
        payFromAmount, payToAmount = self.payAmountFilter.data()
        method = self.methodFilterComboBox.currentText()
        inType = self.inTypeFilterComboBox.currentText()
        payType = self.payTypeFilterComboBox.currentText()

        inDataList = db.find_by_filters(fromDate, toDate, inType, method, inFromAmount, inToAmount, True)
        payDataList = db.find_by_filters(fromDate, toDate, payType, method, payFromAmount, payToAmount, False)

        return inDataList, payDataList

    def pressFilterButton(self):

        inDataList, payDataList = self.get_data()

        self.parent().inData.setItems(inDataList)
        self.parent().payData.setItems(payDataList)