"""
数据库连接测试
"""

import pytest
from backend.db_utils import get_connection


class TestConnection:
    """数据库连接测试类"""

    def test_connection_success(self):
        """测试成功建立连接"""
        conn = get_connection()
        assert conn is not None
        assert conn.open is True
        conn.close()

    def test_connection_database_name(self):
        """测试连接到正确的数据库"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE()")
        db_name = cursor.fetchone()[0]
        assert db_name.lower() == "textbookorder"
        cursor.close()
        conn.close()

    def test_connection_can_execute_query(self):
        """测试连接可以执行查询"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()[0]
        assert result == 1
        cursor.close()
        conn.close()

    def test_multiple_connections(self):
        """测试可以创建多个连接"""
        conn1 = get_connection()
        conn2 = get_connection()
        assert conn1 is not conn2
        assert conn1.open is True
        assert conn2.open is True
        conn1.close()
        conn2.close()
