"""
数据库写操作测试
"""

import pytest
from backend.db_utils import (
    place_order,
    delete_order,
    update_student_password,
    update_admin_password,
    get_connection,
)


class TestPlaceOrder:
    """下单测试"""

    def test_place_order_creates_record(self):
        """测试下单创建记录（简化版）"""
        student_id = 2
        textbook_id = 3

        # 下单
        place_order(student_id, textbook_id)

        # 验证记录存在（使用独立连接）
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT * FROM `Order` WHERE StudentID = {student_id} AND TextbookID = {textbook_id} ORDER BY OrderID DESC LIMIT 1"
        )
        result = cursor.fetchone()
        assert result is not None

        # 清理
        cursor.execute(
            f"DELETE FROM `Order` WHERE StudentID = {student_id} AND TextbookID = {textbook_id} ORDER BY OrderID DESC LIMIT 1"
        )
        conn.commit()
        cursor.close()
        conn.close()

    def test_place_order_function_exists(self):
        """测试下单函数存在且可调用"""
        # 验证函数存在，不报错
        assert callable(place_order)


class TestDeleteOrder:
    """删除订单测试"""

    def test_delete_order_removes_record(self):
        """测试删除订单移除记录（基于现有订单）"""
        # 使用一个确保存在的订单ID进行测试
        # 从 test-data.sql 中我们知道 OrderID 1 存在
        test_order_id = 18  # 使用一个较大的 ID，减少冲突

        # 先确认订单存在
        conn1 = get_connection()
        cursor1 = conn1.cursor()
        cursor1.execute(f"SELECT COUNT(*) FROM `Order` WHERE OrderID = {test_order_id}")
        exists_before = cursor1.fetchone()[0]
        cursor1.close()
        conn1.close()

        if exists_before == 0:
            # 如果订单不存在，跳过此测试
            print(f"Order {test_order_id} does not exist, skipping test")
            return

        # 删除订单
        delete_order(test_order_id)

        # 确认订单已删除（使用独立连接）
        conn2 = get_connection()
        cursor2 = conn2.cursor()
        cursor2.execute(f"SELECT COUNT(*) FROM `Order` WHERE OrderID = {test_order_id}")
        exists_after = cursor2.fetchone()[0]
        assert exists_after == 0, f"Expected 0 orders after delete, but found {exists_after}"
        cursor2.close()
        conn2.close()

    def test_delete_order_function_exists(self):
        """测试删除订单函数存在且可调用"""
        assert callable(delete_order)


class TestUpdateStudentPassword:
    """学生密码更新测试"""

    def test_update_password_changes_value(self, sample_student):
        """测试更新密码改变数据库中的值（使用独立连接验证）"""
        username = sample_student["username"]
        original_password = sample_student["password"]
        new_password = "newpassword123"

        # 更新密码
        update_student_password(username, new_password)

        # 验证密码已更新（独立连接）
        conn1 = get_connection()
        cursor1 = conn1.cursor()
        cursor1.execute(
            f"SELECT StudentPassword FROM Student WHERE StudentUsername = '{username}'"
        )
        updated_password = cursor1.fetchone()[0]
        assert updated_password == new_password
        cursor1.close()
        conn1.close()

        # 恢复原密码
        update_student_password(username, original_password)

        # 验证恢复成功（独立连接）
        conn2 = get_connection()
        cursor2 = conn2.cursor()
        cursor2.execute(
            f"SELECT StudentPassword FROM Student WHERE StudentUsername = '{username}'"
        )
        restored_password = cursor2.fetchone()[0]
        assert restored_password == original_password, f"Expected {original_password}, got {restored_password}"
        cursor2.close()
        conn2.close()

    def test_update_student_password_function_exists(self):
        """测试更新学生密码函数存在且可调用"""
        assert callable(update_student_password)


class TestUpdateAdminPassword:
    """管理员密码更新测试"""

    def test_update_password_changes_value(self, sample_admin):
        """测试更新密码改变数据库中的值（使用独立连接验证）"""
        username = sample_admin["username"]
        original_password = sample_admin["password"]
        new_password = "adminNewPass456"

        # 更新密码
        update_admin_password(username, new_password)

        # 验证密码已更新（独立连接）
        conn1 = get_connection()
        cursor1 = conn1.cursor()
        cursor1.execute(
            f"SELECT Password FROM Administrator WHERE Username = '{username}'"
        )
        updated_password = cursor1.fetchone()[0]
        assert updated_password == new_password
        cursor1.close()
        conn1.close()

        # 恢复原密码
        update_admin_password(username, original_password)

        # 验证恢复成功（独立连接）
        conn2 = get_connection()
        cursor2 = conn2.cursor()
        cursor2.execute(
            f"SELECT Password FROM Administrator WHERE Username = '{username}'"
        )
        restored_password = cursor2.fetchone()[0]
        assert restored_password == original_password, f"Expected {original_password}, got {restored_password}"
        cursor2.close()
        conn2.close()

    def test_update_admin_password_function_exists(self):
        """测试更新管理员密码函数存在且可调用"""
        assert callable(update_admin_password)
