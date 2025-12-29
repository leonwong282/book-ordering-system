# pytest 单元测试方案

## 一、概述

为 `book-ordering-system` 项目编写 pytest 单元测试，确保核心功能的正确性和稳定性。

---

## 二、当前状态

- **测试文件**: 无
- **测试框架**: pytest（已在 requirements.txt 中）
- **README 状态**: `pytest 单元测试` 标记为待完成

---

## 三、测试范围

### 3.1 模块优先级

| 优先级 | 模块 | 文件 | 原因 |
|--------|------|------|------|
| 🔴 P0 | 数据库工具 | `db_utils.py` | 核心业务逻辑，无 UI 依赖 |
| 🟡 P1 | 登录逻辑 | `login_window.py` | 认证逻辑可提取测试 |
| 🟢 P2 | 管理员窗口 | `a_main_window.py` | UI 依赖重，可选 |
| 🟢 P2 | 学生窗口 | `s_main_window.py` | UI 依赖重，可选 |

### 3.2 db_utils.py 函数清单 (15个)

#### 连接管理
| 函数 | 功能 | 测试类型 |
|------|------|---------|
| `get_connection()` | 获取数据库连接 | 集成测试 |

#### 查询操作 (读)
| 函数 | 功能 | 测试类型 |
|------|------|---------|
| `get_admin_credentials()` | 获取管理员账号密码列表 | 单元测试 |
| `get_student_credentials()` | 获取学生账号密码列表 | 单元测试 |
| `get_textbooks()` | 获取教材列表 | 单元测试 |
| `get_student_orders(username)` | 获取学生订单 | 单元测试 |
| `get_college_orders(college_id)` | 按学院查询订单统计 | 单元测试 |
| `get_major_orders(major_id)` | 按专业查询订单统计 | 单元测试 |
| `get_book_orders()` | 获取所有图书订单统计 | 单元测试 |

#### 写操作 (增删改)
| 函数 | 功能 | 测试类型 |
|------|------|---------|
| `place_order(student_id, book_id)` | 创建订单 | 单元测试 |
| `delete_order(order_id)` | 删除订单 | 单元测试 |
| `update_student_password(username, new_password)` | 更新学生密码 | 单元测试 |
| `update_admin_password(username, new_password)` | 更新管理员密码 | 单元测试 |

#### 文件与系统操作
| 函数 | 功能 | 测试类型 |
|------|------|---------|
| `get_book_orders_out()` | 导出订单到 CSV | 集成测试 |
| `backup_database(backup_path)` | 备份数据库 | 集成测试 |
| `recover_database(sql_file_path)` | 恢复数据库 | 集成测试 |

---

## 四、测试目录结构

```
book-ordering-system/
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # 共享 fixtures
│   ├── test_db_connection.py    # 数据库连接测试
│   ├── test_db_query.py         # 查询操作测试
│   ├── test_db_write.py         # 写操作测试
│   └── test_db_file_ops.py      # 文件/系统操作测试
```

---

## 五、Fixtures 设计

### 5.1 conftest.py

```python
import pytest
import pymysql

# 数据库配置
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "passwd": "root",
    "db": "TextbookOrder"
}


@pytest.fixture(scope="session")
def db_connection():
    """会话级数据库连接"""
    conn = pymysql.connect(**DB_CONFIG)
    yield conn
    conn.close()


@pytest.fixture(scope="function")
def db_cursor(db_connection):
    """函数级游标，自动回滚"""
    cursor = db_connection.cursor()
    yield cursor
    db_connection.rollback()  # 测试后回滚
    cursor.close()


@pytest.fixture
def sample_student_username():
    """测试用学生用户名"""
    return "teststudent"


@pytest.fixture
def sample_admin_username():
    """测试用管理员用户名"""
    return "testadmin"


@pytest.fixture
def temp_order(db_cursor):
    """创建临时订单，测试后自动清理"""
    # 插入测试订单
    db_cursor.execute(
        "INSERT INTO `Order`(StudentID, TextbookID) VALUES (1, 1)"
    )
    order_id = db_cursor.lastrowid
    yield order_id
    # 清理（由 rollback 处理）
```

---

## 六、测试用例设计

### 6.1 test_db_connection.py

```python
"""数据库连接测试"""
import pytest
from backend.db_utils import get_connection


class TestConnection:
    """连接测试类"""

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
        assert db_name == "TextbookOrder"
        cursor.close()
        conn.close()
```

### 6.2 test_db_query.py

```python
"""查询操作测试"""
import pytest
from backend.db_utils import (
    get_admin_credentials,
    get_student_credentials,
    get_textbooks,
    get_student_orders,
    get_college_orders,
    get_major_orders,
    get_book_orders,
)


class TestCredentials:
    """凭证查询测试"""

    def test_get_admin_credentials_returns_tuple(self):
        """测试返回两个列表"""
        accounts, passwords = get_admin_credentials()
        assert isinstance(accounts, list)
        assert isinstance(passwords, list)
        assert len(accounts) == len(passwords)

    def test_get_admin_credentials_not_empty(self):
        """测试管理员列表非空"""
        accounts, passwords = get_admin_credentials()
        assert len(accounts) > 0

    def test_get_student_credentials_returns_tuple(self):
        """测试返回两个列表"""
        accounts, passwords = get_student_credentials()
        assert isinstance(accounts, list)
        assert isinstance(passwords, list)
        assert len(accounts) == len(passwords)

    def test_get_student_credentials_not_empty(self):
        """测试学生列表非空"""
        accounts, passwords = get_student_credentials()
        assert len(accounts) > 0


class TestTextbooks:
    """教材查询测试"""

    def test_get_textbooks_returns_tuple_list(self):
        """测试返回元组列表"""
        data = get_textbooks()
        assert isinstance(data, tuple)

    def test_get_textbooks_row_has_five_columns(self):
        """测试每行有5列: ID, Name, Price, Author, Publisher"""
        data = get_textbooks()
        if len(data) > 0:
            assert len(data[0]) == 5

    def test_get_textbooks_not_empty(self):
        """测试教材列表非空"""
        data = get_textbooks()
        assert len(data) > 0


class TestStudentOrders:
    """学生订单查询测试"""

    def test_get_student_orders_returns_tuple(self):
        """测试返回元组"""
        # 使用已知存在的学生用户名
        data = get_student_orders("student1")
        assert isinstance(data, tuple)

    def test_get_student_orders_row_has_four_columns(self):
        """测试每行有4列: OrderID, StudentName, TextbookName, Price"""
        data = get_student_orders("student1")
        if len(data) > 0:
            assert len(data[0]) == 4


class TestStatistics:
    """统计查询测试"""

    def test_get_college_orders_returns_tuple(self):
        """测试按学院统计"""
        data = get_college_orders(1)
        assert isinstance(data, tuple)

    def test_get_major_orders_returns_tuple(self):
        """测试按专业统计"""
        data = get_major_orders(1)
        assert isinstance(data, tuple)

    def test_get_book_orders_returns_tuple(self):
        """测试所有图书统计"""
        data = get_book_orders()
        assert isinstance(data, tuple)

    def test_get_book_orders_row_has_two_columns(self):
        """测试每行有2列: TextbookID, Count"""
        data = get_book_orders()
        if len(data) > 0:
            assert len(data[0]) == 2
```

### 6.3 test_db_write.py

```python
"""写操作测试"""
import pytest
from backend.db_utils import (
    place_order,
    delete_order,
    update_student_password,
    update_admin_password,
)


class TestOrderOperations:
    """订单操作测试"""

    def test_place_order_success(self, db_cursor):
        """测试下单成功"""
        # 获取初始订单数
        db_cursor.execute("SELECT COUNT(*) FROM `Order`")
        initial_count = db_cursor.fetchone()[0]

        # 下单
        place_order(1, 1)

        # 验证订单数增加
        db_cursor.execute("SELECT COUNT(*) FROM `Order`")
        new_count = db_cursor.fetchone()[0]
        assert new_count == initial_count + 1

    def test_delete_order_success(self, db_cursor, temp_order):
        """测试删除订单成功"""
        # 确认订单存在
        db_cursor.execute(
            f"SELECT COUNT(*) FROM `Order` WHERE OrderID = {temp_order}"
        )
        assert db_cursor.fetchone()[0] == 1

        # 删除订单
        delete_order(temp_order)

        # 确认订单已删除
        db_cursor.execute(
            f"SELECT COUNT(*) FROM `Order` WHERE OrderID = {temp_order}"
        )
        assert db_cursor.fetchone()[0] == 0


class TestPasswordUpdate:
    """密码更新测试"""

    def test_update_student_password(self, db_cursor):
        """测试更新学生密码"""
        username = "student1"
        new_password = "newpass123"

        # 获取原密码
        db_cursor.execute(
            f"SELECT StudentPassword FROM Student WHERE StudentUsername = '{username}'"
        )
        original_password = db_cursor.fetchone()[0]

        # 更新密码
        update_student_password(username, new_password)

        # 验证密码已更新
        db_cursor.execute(
            f"SELECT StudentPassword FROM Student WHERE StudentUsername = '{username}'"
        )
        updated_password = db_cursor.fetchone()[0]
        assert updated_password == new_password

        # 恢复原密码
        update_student_password(username, original_password)

    def test_update_admin_password(self, db_cursor):
        """测试更新管理员密码"""
        username = "admin1"
        new_password = "adminpass123"

        # 获取原密码
        db_cursor.execute(
            f"SELECT Password FROM Administrator WHERE Username = '{username}'"
        )
        original_password = db_cursor.fetchone()[0]

        # 更新密码
        update_admin_password(username, new_password)

        # 验证密码已更新
        db_cursor.execute(
            f"SELECT Password FROM Administrator WHERE Username = '{username}'"
        )
        updated_password = db_cursor.fetchone()[0]
        assert updated_password == new_password

        # 恢复原密码
        update_admin_password(username, original_password)
```

### 6.4 test_db_file_ops.py

```python
"""文件与系统操作测试"""
import os
import pytest
from backend.db_utils import get_book_orders_out, backup_database


class TestExport:
    """导出测试"""

    def test_export_creates_csv_file(self):
        """测试导出创建 CSV 文件"""
        expected_path = "/Users/liang/Downloads/data_Order_Book.csv"

        # 删除已存在的文件
        if os.path.exists(expected_path):
            os.remove(expected_path)

        # 执行导出
        get_book_orders_out()

        # 验证文件存在
        assert os.path.exists(expected_path)

    def test_export_csv_not_empty(self):
        """测试导出的 CSV 文件非空"""
        expected_path = "/Users/liang/Downloads/data_Order_Book.csv"
        get_book_orders_out()

        assert os.path.getsize(expected_path) > 0


class TestBackup:
    """备份测试"""

    def test_backup_creates_sql_file(self):
        """测试备份创建 SQL 文件"""
        backup_path = "/Users/liang/Downloads"
        expected_file = os.path.join(backup_path, "TextbookOrder.sql")

        # 删除已存在的文件
        if os.path.exists(expected_file):
            os.remove(expected_file)

        # 执行备份
        backup_database(backup_path)

        # 验证文件存在
        assert os.path.exists(expected_file)

    def test_backup_sql_not_empty(self):
        """测试备份的 SQL 文件非空"""
        backup_path = "/Users/liang/Downloads"
        expected_file = os.path.join(backup_path, "TextbookOrder.sql")

        backup_database(backup_path)

        assert os.path.getsize(expected_file) > 0
```

---

## 七、运行测试

### 7.1 基本命令

```bash
# 运行所有测试
pytest

# 详细输出
pytest -v

# 运行特定文件
pytest tests/test_db_query.py

# 运行特定类
pytest tests/test_db_query.py::TestCredentials

# 运行特定方法
pytest tests/test_db_query.py::TestCredentials::test_get_admin_credentials_returns_tuple

# 显示 print 输出
pytest -s

# 覆盖率报告
pytest --cov=backend --cov-report=html
```

### 7.2 pytest.ini 配置

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

---

## 八、测试数据准备

### 8.1 前置条件

确保数据库中存在以下测试数据：

```sql
-- 管理员账号
INSERT INTO Administrator (AdminID, Username, Password)
VALUES (1, 'admin1', 'admin123');

-- 学生账号
INSERT INTO Student (StudentID, StudentUsername, StudentPassword, MajorID)
VALUES (1, 'student1', 'student123', 1);

-- 教材
INSERT INTO Textbook (TextbookID, TextbookName, Author, Publisher, Price, MajorID)
VALUES (1, '数据库系统概论', '王珊', '高等教育出版社', 49.00, 1);

-- 学院
INSERT INTO College (CollegeID, CollegeName)
VALUES (1, '计算机学院');

-- 专业
INSERT INTO Major (MajorID, MajorName, CollegeID)
VALUES (1, '软件工程', 1);
```

### 8.2 使用 test-data.sql

项目已有 `database/test-data.sql`，运行测试前执行：

```bash
mysql -uroot -proot TextbookOrder < database/test-data.sql
```

---

## 九、覆盖率目标

| 模块 | 目标覆盖率 | 说明 |
|------|-----------|------|
| `db_utils.py` | ≥ 80% | 核心模块 |
| 查询函数 | 100% | 必须全覆盖 |
| 写操作函数 | ≥ 90% | 关键业务 |
| 文件操作函数 | ≥ 70% | 依赖外部环境 |

---

## 十、注意事项

1. **数据隔离**: 写操作测试使用事务回滚，避免污染数据
2. **测试顺序**: 使用 `pytest-order` 插件控制测试顺序（如需要）
3. **环境依赖**: 需要本地 MySQL 服务运行
4. **路径硬编码**: `get_book_orders_out()` 和 `backup_database()` 使用硬编码路径
5. **存储过程**: 确保 `pCollege`、`pMajor`、`pOderBook` 已创建

---

## 十一、后续扩展

1. **Mock 测试**: 使用 `unittest.mock` 模拟数据库连接
2. **CI 集成**: GitHub Actions 自动运行测试
3. **UI 测试**: 使用 `pytest-qt` 测试 PyQt5 组件
4. **性能测试**: 使用 `pytest-benchmark` 测试查询性能
