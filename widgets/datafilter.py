import sys

from PyQt5.QtWidgets import (
    QComboBox,
    QLabel,
    QWidget
)

sys.path.append("../")

class TimeFilter(QWidget):
    def __init__(self, parent):
        super(TimeFilter, self).__init__(parent)

        self.init()

    def init(self):
        pass

class AmountFilter(QWidget):
    def __init__(self, parent):
        super(TimeFilter, self).__init__(parent)

        self.init()

    def init(self):
        pass

class DataFilter(QWidget):
    def __init__(self, parent):
        super(DataFilter, self).__init__(parent)

        self.types = ["娱乐", "游戏", "生活", "食物"]
        self.methods = ["全部", "支付宝", "微信", "现金"]
        self.init()

    def init(self):

        # 筛选时间
        self.timeFilter

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
        self.inAmountFilter
        self.payAmountFilter