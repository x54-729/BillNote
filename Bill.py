import sqlite3

class Bill:

    def __init__(self, num, type_, description, method='alipay', is_income=False):

        self.num = num
        self.type = type_
        self.description = description
        self.method = method
        self.is_income = is_income

