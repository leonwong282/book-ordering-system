"""
Pytest fixtures for book-ordering-system tests.
"""

import pytest
import pymysql

# 数据库配置
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "passwd": "root",
    "db": "TextbookOrder",
}


@pytest.fixture(scope="function")
def db_connection():
    """函数级数据库连接，每个测试创建一个新连接"""
    conn = pymysql.connect(**DB_CONFIG)
    conn.autocommit(False)  # 禁用自动提交
    yield conn
    conn.rollback()
    conn.close()


@pytest.fixture(scope="function")
def db_cursor(db_connection):
    """函数级游标"""
    cursor = db_connection.cursor()
    yield cursor
    cursor.close()


@pytest.fixture
def sample_student():
    """测试用学生数据 (来自 test-data.sql)"""
    return {
        "id": 1,
        "name": "张伟",
        "username": "stu001",
        "password": "pwd001",
        "major_id": 1,
    }


@pytest.fixture
def sample_admin():
    """测试用管理员数据 (来自 test-data.sql)"""
    return {
        "id": 1,
        "name": "张三",
        "username": "admin001",
        "password": "pass123",
    }


@pytest.fixture
def sample_textbook():
    """测试用教材数据 (来自 test-data.sql)"""
    return {
        "id": 1,
        "name": "数据结构与算法",
        "author": "严蔚敏",
        "publisher": "清华大学出版社",
        "price": 45.0,
        "major_id": 1,
    }


@pytest.fixture
def temp_order_id(db_cursor):
    """创建临时订单，返回订单ID，测试后自动回滚"""
    db_cursor.execute(
        "INSERT INTO `Order`(StudentID, TextbookID) VALUES (1, 1)"
    )
    order_id = db_cursor.lastrowid
    return order_id
