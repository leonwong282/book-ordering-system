from PyQt5.QtWidgets import QMainWindow
from frontend.LonginUI import Ui_LoginWindow
from backend.a_main_window import AMainWindow
from backend.s_main_window import SMainWindow
from backend.db_utils import get_admin_credentials, get_student_credentials


class LoginWindow(QMainWindow):
    """
    login
    """

    def __init__(self):
        super().__init__()
        self.window = None
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        # Show student login UI in Login Window
        self.ui.pushButton_A_login.clicked.connect(
            lambda: self.ui.stackedWidget_2.setCurrentIndex(1)
        )
        # Show admin  login UI in Login Window
        self.ui.pushButton_S_login.clicked.connect(
            lambda: self.ui.stackedWidget_2.setCurrentIndex(0)
        )
        # If account and password is ture, opening Student Main Window
        self.ui.pushButton_A_sure.clicked.connect(self.login_in_a_window)
        # If account and password is ture, opening Admin Main Window
        self.ui.pushButton_S_sure.clicked.connect(self.login_in_s_window)
        self.show()

    def login_in_a_window(self):
        """
        :return:
        """
        account = self.ui.lineEdit_A_account.text()
        password = self.ui.lineEdit_A_password.text()
        account_list, password_list = get_admin_credentials()
        for i in range(len(account_list)):
            if len(account) == 0 or len(password) == 0:
                self.ui.stackedWidget.setCurrentIndex(1)
            elif account == account_list[i] and password == password_list[i]:
                self.window = AMainWindow(account)
                self.close()  # close Login window
            else:
                self.ui.stackedWidget.setCurrentIndex(2)

    def login_in_s_window(self):
        """

        :return:
        """
        account = self.ui.lineEdit_S_account.text()
        password = self.ui.lineEdit_S_password.text()
        account_list, password_list = get_student_credentials()
        for i in range(len(account_list)):
            if len(account) == 0 or len(password) == 0:
                self.ui.stackedWidget.setCurrentIndex(1)
            elif account == account_list[i] and password == password_list[i]:
                self.window = SMainWindow(account)
                self.close()
            else:
                self.ui.stackedWidget.setCurrentIndex(2)
