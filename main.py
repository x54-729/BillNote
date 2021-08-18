import sys

from PyQt5.QtWidgets import QApplication, QWidget

from view import View

if __name__ == '__main__':

    app = QApplication(sys.argv)
    v = View()
    v.show()

    sys.exit(app.exec_())