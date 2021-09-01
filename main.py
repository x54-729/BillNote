from sqlite3.dbapi2 import paramstyle
from database.bill_database import delete
import sys
import argparse

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication, Qt

from view import View
from database import reconstruct_database

if __name__ == '__main__':

    parse = argparse.ArgumentParser()
    parse.add_argument("--reconstruct", "-r", action="store_true", help="重构数据库")
    args = parse.parse_args()

    if args.reconstruct:
        reconstruct_database()

    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    v = View()
    v.show()

    sys.exit(app.exec_())