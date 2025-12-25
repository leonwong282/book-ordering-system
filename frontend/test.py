import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from LonginUI import Ui_LoginWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_LoginWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())