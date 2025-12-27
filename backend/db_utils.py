import os
import pymysql

def get_connection():
    """

    :return:
    """
    return pymysql.connect(host="localhost", port=3306, user="root", passwd="root", db="TextbookOrder")

def get_admin_credentials():
    pass

def get_student_credentials():
    pass

