from PyQt5.QtWidgets import QMainWindow , QHeaderView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from frontend.SMainWindow import Ui_SMainWindow
from backend.db_utils import get_textbooks, get_student_orders, update_student_password, place_order, delete_order

class SMainWindow(QMainWindow):
    def __init__(self, user_now):
        super().__init__()
        self.user_now = user_now
        self.login = None
        self.ui = Ui_SMainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_login_out.clicked.connect(self.login_out)
        self.ui.pushButton_S_shopping.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.pushButton_S_order.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.pushButton_S_update_pw.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.pushButton_S_M_sure.clicked.connect(self.change_password)
        self.ui.pushButton_S_M_order_sure.clicked.connect(self.order_book)
        self.ui.pushButton_S_M_order_sure_update.clicked.connect(self.delete_order_student)
        self.setup_book_list()
        self.setup_order_list()
        self.show()

    def setup_book_list(self):
        """
        init book list
        :return:
        """
        self.model = QStandardItemModel(5, 4)
        self.model.setHorizontalHeaderLabels(['书号', '书名', '价格', '作者', '出版社'])
        data = get_textbooks()
        for row in range(len(data)):
            for col in range(len(data[row])):
                item = QStandardItem(str(data[row][col]))
                self.model.setItem(row, col, item)
        self.ui.tableView_S_M_bookList.setModel(self.model)
        self.ui.tableView_S_M_bookList.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableView_S_M_bookList.verticalHeader().setVisible(False)

    def setup_order_list(self):
        """
        init order list
        :return:
        """
        self.model2 = QStandardItemModel(4, 4)
        self.model2.setHorizontalHeaderLabels(['订单号', '姓名', '书名', '价格'])
        data = get_student_orders(self.user_now)
        for row in range(len(data)):
            for col in range(len(data[row])):
                item = QStandardItem(str(data[row][col]))
                self.model2.setItem(row, col, item)
        self.ui.tableView_2.setModel(self.model2)
        self.ui.tableView_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableView_2.verticalHeader().setVisible(False)

    def login_out(self):
        """
        student login out
        :return:
        """
        from backend.login_window import LoginWindow
        self.close()
        self.login = LoginWindow(self.user_now)

    def change_password(self):
        password_old = self.ui.lineEdit_S_M_password.text()
        password_new = self.ui.lineEdit_S_M_new_password.text()
        if len(password_old) == 0 or len(password_new) == 0 or len(self.ui.lineEdit_S_M_new_password_sure.text()) == 0:
            self.ui.stackedWidget_2.setCurrentIndex(1)
        elif self.ui.lineEdit_S_M_new_password_sure.text() == password_new:
            self.ui.stackedWidget_2.setCurrentIndex(3)
            update_student_password(self.user_now, password_new)
        else:
            self.ui.stackedWidget_2.setCurrentIndex(2)

    def order_book(self):
        book = self.ui.lineEdit_S_M_bookID.text()
        student = self.ui.lineEdit_S_M_studentID.text()
        place_order(student, book)
        self.ui.lineEdit_S_M_studentID.clear()
        self.ui.lineEdit_S_M_bookID.clear()

    def delete_order_student(self):
        order_id = self.ui.lineEdit_S_M_order_update.text()
        delete_order(order_id)
        self.setup_order_list()
        self.ui.lineEdit_S_M_order_update.clear()
