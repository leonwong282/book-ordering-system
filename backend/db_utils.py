import os
import pymysql
import pandas as pd

def get_connection():
    """

    :return:
    """
    return pymysql.connect(host="localhost", port=3306, user="root", passwd="root", db="TextbookOrder")

def get_admin_credentials():
    pass

def get_student_credentials():
    pass

def get_textbooks():
    pass

def get_student_orders(username):
    pass

def update_student_password(username, new_password):
    pass

def place_order(student_id, book_id):
    pass

def delete_order(order_id):
    pass

def get_college_orders(college_id):
    pass

def get_major_orders(major_id):
    pass

def get_book_orders():
    pass

def get_book_orders_out():
    pass

def update_admin_password(username, new_password):
    pass

def backup_database():
    pass

def recover_database():
    pass
