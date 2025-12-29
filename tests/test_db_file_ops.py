"""
文件与系统操作测试
"""

import os
import pytest
from backend.db_utils import get_book_orders_out, backup_database, recover_database


class TestExportCSV:
    """CSV 导出测试"""

    @pytest.fixture
    def export_path(self):
        """导出文件路径"""
        return "/Users/liang/Downloads/data_Order_Book.csv"

    def test_export_creates_file(self, export_path):
        """测试导出创建 CSV 文件"""
        # 删除已存在的文件
        if os.path.exists(export_path):
            os.remove(export_path)

        # 执行导出
        get_book_orders_out()

        # 验证文件存在
        assert os.path.exists(export_path)

    def test_export_file_not_empty(self, export_path):
        """测试导出的 CSV 文件非空"""
        get_book_orders_out()
        assert os.path.getsize(export_path) > 0

    def test_export_file_has_header(self, export_path):
        """测试导出的 CSV 文件有表头"""
        get_book_orders_out()
        with open(export_path, "r", encoding="utf-8-sig") as f:
            header = f.readline().strip()
            # 表头应包含字段名
            assert len(header) > 0

    def test_export_file_has_data_rows(self, export_path):
        """测试导出的 CSV 文件有数据行"""
        get_book_orders_out()
        with open(export_path, "r", encoding="utf-8-sig") as f:
            lines = f.readlines()
            # 至少有表头 + 1行数据
            assert len(lines) >= 2


class TestBackupDatabase:
    """数据库备份测试"""

    @pytest.fixture
    def backup_path(self):
        """备份目录"""
        return "/Users/liang/Downloads"

    @pytest.fixture
    def backup_file(self, backup_path):
        """备份文件路径"""
        return os.path.join(backup_path, "TextbookOrder.sql")

    def test_backup_creates_file(self, backup_path, backup_file):
        """测试备份创建 SQL 文件"""
        # 删除已存在的文件
        if os.path.exists(backup_file):
            os.remove(backup_file)

        # 执行备份
        backup_database(backup_path)

        # 验证文件存在
        assert os.path.exists(backup_file)

    def test_backup_file_not_empty(self, backup_path, backup_file):
        """测试备份的 SQL 文件非空"""
        backup_database(backup_path)
        assert os.path.getsize(backup_file) > 0

    def test_backup_file_contains_sql(self, backup_path, backup_file):
        """测试备份文件包含 SQL 语句"""
        backup_database(backup_path)
        with open(backup_file, "r", encoding="utf-8") as f:
            content = f.read()
            # 应包含 CREATE TABLE 或 INSERT 语句
            assert "CREATE" in content or "INSERT" in content or "DROP" in content


class TestRecoverDatabase:
    """数据库恢复测试"""

    @pytest.fixture
    def sql_file_path(self):
        """恢复用 SQL 文件路径"""
        return "/Users/liang/Downloads/TextbookOrder.sql"

    def test_recover_with_existing_file(self, sql_file_path):
        """测试使用存在的文件恢复"""
        # 确保备份文件存在
        backup_path = "/Users/liang/Downloads"
        backup_database(backup_path)

        # 执行恢复（不应抛出异常）
        recover_database(sql_file_path)
        # 如果没有异常，测试通过

    def test_recover_preserves_data(self, sql_file_path):
        """测试恢复后数据完整"""
        from backend.db_utils import get_connection

        # 先备份
        backup_path = "/Users/liang/Downloads"
        backup_database(backup_path)

        # 获取恢复前的数据量
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Student")
        count_before = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        # 执行恢复
        recover_database(sql_file_path)

        # 获取恢复后的数据量
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Student")
        count_after = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        # 数据量应该相同
        assert count_after == count_before
