import sys

from AMainWindow import Ui_AMainWindow
from LonginUI import Ui_LoginWindow
from PyQt5.QtWidgets import QApplication, QMainWindow
from SMainWindow import Ui_SMainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    # ui = Ui_LoginWindow()
    # ui = Ui_AMainWindow()
    ui = Ui_SMainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())