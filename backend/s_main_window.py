from PyQt5.QtWidgets import QMainWindow , QHeaderView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from frontend.SMainWindow import Ui_SMainWindow
from db_utils import get_textbooks, get_student_orders, update_student_password, place_order, delete_order

class SMainWindow(QMainWindow):
    def __init__(self, user_now):
        super().__init__()
        self.user_now = user_now
        self.login = None
        self.ui = Ui_SMainWindow()
        self.ui.setupUi(self)
        # TO DO
        self.show()

    def setup_book_list(self):
        pass

    def setup_order_list(self):
        pass

    def login_out(self):
        pass

    def change_password(self):
        pass

    def order_book(self):
        pass

    def update_order_student(self):
        pass
