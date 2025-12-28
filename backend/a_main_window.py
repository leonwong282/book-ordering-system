from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QHeaderView, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from frontend.AMainWindow import Ui_AMainWindow
from db_utils import get_college_orders, get_major_orders, get_book_orders, update_admin_password, backup_database, \
    recover_database, get_book_orders_out

class AMainWindow(QMainWindow):
    def __init__(self, user_now):
        super().__init__()
        self.user_now = user_now
        self.login = None
        self.ui = Ui_AMainWindow()
        self.ui.setupUi(self)
        # TO DO
        self.show()

    def login_out_a(self):
        pass

    def change_password_a(self):
        pass

    def order_college(self):
        pass

    def order_major(self):
        pass

    def change_major(self):
        pass

    def setup_order_book_list(self):
        pass

    def change_order_book(self):
        pass

    def order_book_out(self):
        pass

    def backup_data(self):
        pass

    def recover_data(self):
        pass