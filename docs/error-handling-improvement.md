# 错误处理改进方案

## 一、改进目标

为 `book-ordering-system` 项目添加完善的异常处理机制，提高系统稳定性和用户体验。

---

## 二、当前问题分析

### 2.1 已有错误处理

| 文件 | 函数 | 状态 |
|------|------|------|
| `a_main_window.py` | `order_major()` | ✅ 已处理 |
| `a_main_window.py` | `order_book_out()` | ✅ 已处理 |
| `a_main_window.py` | `backup_data()` | ✅ 已处理 |
| `a_main_window.py` | `recover_data()` | ✅ 已处理 |

### 2.2 缺少错误处理的函数

#### db_utils.py (15个函数)

| 函数 | 风险类型 | 优先级 |
|------|----------|--------|
| `get_connection()` | 数据库连接失败 | 🔴 高 |
| `get_admin_credentials()` | 查询失败、资源泄漏 | 🔴 高 |
| `get_student_credentials()` | 查询失败、资源泄漏 | 🔴 高 |
| `get_textbooks()` | 查询失败、资源泄漏 | 🟡 中 |
| `get_student_orders()` | NoneType 错误、SQL注入 | 🔴 高 |
| `update_student_password()` | 更新失败、SQL注入 | 🔴 高 |
| `place_order()` | 插入失败、SQL注入 | 🔴 高 |
| `delete_order()` | 删除失败、SQL注入 | 🟡 中 |
| `get_college_orders()` | 存储过程调用失败 | 🟡 中 |
| `get_major_orders()` | 存储过程调用失败 | 🟡 中 |
| `get_book_orders()` | 存储过程调用失败 | 🟡 中 |
| `get_book_orders_out()` | 文件写入失败 | 🟡 中 |
| `update_admin_password()` | 更新失败、SQL注入 | 🔴 高 |
| `backup_database()` | 命令执行失败 | 🟡 中 |
| `recover_database()` | 命令执行失败 | 🟡 中 |

#### login_window.py (2个函数)

| 函数 | 风险类型 | 优先级 |
|------|----------|--------|
| `login_in_a_window()` | 数据库异常导致登录崩溃 | 🔴 高 |
| `login_in_s_window()` | 数据库异常导致登录崩溃 | 🔴 高 |

#### s_main_window.py (5个函数)

| 函数 | 风险类型 | 优先级 |
|------|----------|--------|
| `setup_book_list()` | 初始化失败导致窗口崩溃 | 🔴 高 |
| `setup_order_list()` | 初始化失败导致窗口崩溃 | 🔴 高 |
| `change_password()` | 密码更新失败无反馈 | 🟡 中 |
| `order_book()` | 下单失败无反馈 | 🔴 高 |
| `delete_order_student()` | 删除失败无反馈 | 🟡 中 |

#### a_main_window.py (2个函数)

| 函数 | 风险类型 | 优先级 |
|------|----------|--------|
| `setup_order_book_list()` | 初始化失败导致窗口崩溃 | 🔴 高 |
| `order_college()` | 查询失败无反馈 | 🟡 中 |
| `change_password_a()` | 密码更新失败无反馈 | 🟡 中 |

---

## 三、改进方案

### 3.1 创建自定义异常类

在 `backend/` 目录新建 `exceptions.py`:

```python
class DatabaseError(Exception):
    """数据库操作异常"""
    pass

class ConnectionError(DatabaseError):
    """数据库连接异常"""
    pass

class QueryError(DatabaseError):
    """查询异常"""
    pass

class FileOperationError(Exception):
    """文件操作异常"""
    pass
```

### 3.2 db_utils.py 改进

#### 3.2.1 使用上下文管理器确保资源释放

```python
from contextlib import contextmanager

@contextmanager
def get_db_connection():
    """数据库连接上下文管理器"""
    conn = None
    try:
        conn = pymysql.connect(
            host="localhost", port=3306,
            user="root", passwd="root",
            db="TextbookOrder"
        )
        yield conn
    except pymysql.Error as e:
        raise ConnectionError(f"数据库连接失败: {e}")
    finally:
        if conn:
            conn.close()
```

#### 3.2.2 查询函数模板

```python
def get_admin_credentials():
    """获取管理员凭证"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT Username, Password FROM Administrator")
                rows = cur.fetchall()
                account_list = [row[0] for row in rows]
                password_list = [row[1] for row in rows]
                return account_list, password_list
    except ConnectionError:
        raise
    except Exception as e:
        raise QueryError(f"获取管理员凭证失败: {e}")
```

#### 3.2.3 写操作函数模板（带事务）

```python
def place_order(student_id, book_id):
    """下单"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO `Order`(StudentID, TextbookID) VALUES (%s, %s)",
                    (student_id, book_id)
                )
                conn.commit()
                return True
    except ConnectionError:
        raise
    except Exception as e:
        raise QueryError(f"下单失败: {e}")
```

#### 3.2.4 文件操作函数模板

```python
def get_book_orders_out():
    """导出订单到CSV"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.callproc("pOderBook")
                data = cur.fetchall()
                column_names = [desc[0] for desc in cur.description]
                df = pd.DataFrame(data, columns=column_names)
                filename = "/Users/liang/Downloads/data_Order_Book.csv"
                df.to_csv(filename, index=False, encoding="utf-8-sig")
                return True
    except ConnectionError:
        raise
    except IOError as e:
        raise FileOperationError(f"文件写入失败: {e}")
    except Exception as e:
        raise QueryError(f"导出失败: {e}")
```

#### 3.2.5 系统命令函数模板

```python
def backup_database(backup_path):
    """备份数据库"""
    import subprocess

    user = "root"
    password = "root"
    database = "TextbookOrder"
    backup_filename = os.path.join(backup_path, f"{database}.sql")

    try:
        result = subprocess.run(
            ["mysqldump", f"-u{user}", f"-p{password}", database],
            capture_output=True,
            text=True,
            check=True
        )
        with open(backup_filename, "w") as f:
            f.write(result.stdout)
        return backup_filename
    except subprocess.CalledProcessError as e:
        raise FileOperationError(f"备份失败: {e.stderr}")
    except IOError as e:
        raise FileOperationError(f"写入备份文件失败: {e}")
```

### 3.3 UI 层改进

#### 3.3.1 login_window.py

```python
def login_in_a_window(self):
    try:
        account = self.ui.lineEdit_A_account.text()
        password = self.ui.lineEdit_A_password.text()

        if not account or not password:
            self.ui.stackedWidget.setCurrentIndex(1)
            return

        account_list, password_list = get_admin_credentials()

        for i in range(len(account_list)):
            if account == account_list[i] and password == password_list[i]:
                self.window = AMainWindow(account)
                self.close()
                return

        self.ui.stackedWidget.setCurrentIndex(2)

    except Exception as e:
        QMessageBox.critical(self, "错误", f"登录失败: {str(e)}")
```

#### 3.3.2 s_main_window.py

```python
def order_book(self):
    try:
        book = self.ui.lineEdit_S_M_bookID.text()
        student = self.ui.lineEdit_S_M_studentID.text()

        if not book or not student:
            QMessageBox.warning(self, "提示", "请输入学号和书号")
            return

        place_order(student, book)
        self.setup_order_list()  # 刷新订单列表
        self.ui.lineEdit_S_M_studentID.clear()
        self.ui.lineEdit_S_M_bookID.clear()
        QMessageBox.information(self, "成功", "下单成功")

    except Exception as e:
        QMessageBox.critical(self, "错误", f"下单失败: {str(e)}")
```

---

## 四、实施步骤

### 阶段一：底层改进 (db_utils.py)

1. 创建 `backend/exceptions.py` 自定义异常类
2. 添加 `get_db_connection()` 上下文管理器
3. 为所有查询函数添加 try-except-finally
4. 使用参数化查询替换字符串格式化（防SQL注入）
5. 为写操作添加事务控制

### 阶段二：UI 层改进

6. 改进 `login_window.py` 的两个登录函数
7. 改进 `s_main_window.py` 的5个函数
8. 改进 `a_main_window.py` 的3个未处理函数

### 阶段三：测试验证

9. 测试数据库连接失败场景
10. 测试网络中断场景
11. 测试无效输入场景
12. 测试文件权限受限场景

---

## 五、改进前后对比

### 改进前
```python
def get_textbooks():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT ... FROM Textbook")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data
```

**问题**:
- 连接失败时程序崩溃
- 查询异常时连接不会关闭（资源泄漏）

### 改进后
```python
def get_textbooks():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT ... FROM Textbook")
                return cur.fetchall()
    except ConnectionError:
        raise
    except Exception as e:
        raise QueryError(f"获取教材列表失败: {e}")
```

**优点**:
- 连接自动管理，确保关闭
- 异常分类明确，便于上层处理
- 错误信息清晰

---

## 六、注意事项

1. **不要吞掉异常**: 底层函数应抛出异常，由 UI 层决定如何展示
2. **日志记录**: 考虑添加 logging 记录异常详情（用于排查问题）
3. **用户友好**: UI 层的错误提示应简洁明了，避免暴露技术细节
4. **保持一致**: 所有函数遵循相同的异常处理模式
