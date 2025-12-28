import os
import pymysql
import pandas as pd

def get_connection():
    """

    :return:
    """
    return pymysql.connect(host="localhost", port=3306, user="root", passwd="root", db="TextbookOrder")

def get_admin_credentials():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT Username, Password FROM Administrator")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    account_list = [row[0] for row in rows]
    password_list = [row[1] for row in rows]
    return account_list, password_list

def get_student_credentials():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT StudentUsername, StudentPassword FROM Student")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    account_list = [row[0] for row in rows]
    password_list = [row[1] for row in rows]
    return account_list, password_list

def get_textbooks():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT TextbookID, TextbookName, Price, Author, Publisher FROM Textbook")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def get_student_orders(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT StudentName FROM Student WHERE StudentUsername = '{username}'")
    student_name = cur.fetchone()[0]
    cur.execute(f"SELECT OrderID, StudentName, TextbookName, Price FROM Student_Order_View WHERE StudentName = '{student_name}'")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def update_student_password(username, new_password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"UPDATE Student SET StudentPassword = '{new_password}' WHERE StudentUsername = '{username}'")
    conn.commit()
    cur.close()
    conn.close()

def place_order(student_id, book_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"INSERT INTO `Order`(StudentID, TextbookID) VALUES ({student_id}, {book_id})")
    conn.commit()
    cur.close()
    conn.close()

def delete_order(order_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"DELETE FROM `Order` WHERE OrderID = {order_id}")
    conn.commit()
    cur.close()
    conn.close()

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
