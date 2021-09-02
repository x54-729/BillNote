from PyQt5.QtWidgets import (
    QHBoxLayout,
    QPushButton, 
    QVBoxLayout, 
    QWidget
)

from widgets import DataArea, DataFilter

class View(QWidget):

    def __init__(self):
        super(View, self).__init__()
        
        self.resize(750, 400)
        self.setWindowTitle("账本")
        self.mainlayout = QVBoxLayout()
        self.setLayout(self.mainlayout)

        self.init()
        self.update()

    def init(self):

        # filters
        self.filter = DataFilter(self)

        datalayout = QHBoxLayout()
        # payment
        self.payData = DataArea(is_income=False, parent=self)
        datalayout.addWidget(self.payData)
        # income
        self.inData = DataArea(is_income=True, parent=self)
        datalayout.addWidget(self.inData)

        self.mainlayout.addWidget(self.filter)
        self.mainlayout.addLayout(datalayout)

        self.setStyleSheet('''
            QPushButton{
                color:white;
                background:blue;
                padding:3px;
                border-radius:5px;
                font-weight:1000;
                font-family:"STKaiti";
            }
        ''')

    def update(self):

        inDataList, payDataList = self.filter.get_data()
        self.inData.update(inDataList)
        self.payData.update(payDataList)
