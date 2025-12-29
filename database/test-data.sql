-- 先关闭外键检查（因为 TRUNCATE 不允许有外键引用）
SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE TextbookOrder.`Order`;
TRUNCATE TABLE TextbookOrder.order_log;
TRUNCATE TABLE TextbookOrder.Student;
TRUNCATE TABLE TextbookOrder.Textbook;
TRUNCATE TABLE TextbookOrder.Major;
TRUNCATE TABLE TextbookOrder.College;
TRUNCATE TABLE TextbookOrder.Administrator;

SET FOREIGN_KEY_CHECKS = 1;

-- 插入学院数据
INSERT INTO TextbookOrder.College (CollegeID, CollegeName)
VALUES (1, '计算机科学与技术学院');
INSERT INTO TextbookOrder.College (CollegeID, CollegeName)
VALUES (2, '软件学院');
INSERT INTO TextbookOrder.College (CollegeID, CollegeName)
VALUES (3, '经济管理学院');
INSERT INTO TextbookOrder.College (CollegeID, CollegeName)
VALUES (4, '外国语学院');
INSERT INTO TextbookOrder.College (CollegeID, CollegeName)
VALUES (5, '数学与统计学院');

-- 插入专业数据
INSERT INTO TextbookOrder.Major (MajorID, MajorName, CollegeID)
VALUES (1, '计算机科学与技术', 1);
INSERT INTO TextbookOrder.Major (MajorID, MajorName, CollegeID)
VALUES (2, '软件工程', 2);
INSERT INTO TextbookOrder.Major (MajorID, MajorName, CollegeID)
VALUES (3, '数据科学与大数据技术', 1);
INSERT INTO TextbookOrder.Major (MajorID, MajorName, CollegeID)
VALUES (4, '人工智能', 1);
INSERT INTO TextbookOrder.Major (MajorID, MajorName, CollegeID)
VALUES (5, '工商管理', 3);
INSERT INTO TextbookOrder.Major (MajorID, MajorName, CollegeID)
VALUES (6, '会计学', 3);
INSERT INTO TextbookOrder.Major (MajorID, MajorName, CollegeID)
VALUES (7, '英语', 4);
INSERT INTO TextbookOrder.Major (MajorID, MajorName, CollegeID)
VALUES (8, '日语', 4);
INSERT INTO TextbookOrder.Major (MajorID, MajorName, CollegeID)
VALUES (9, '数学与应用数学', 5);
INSERT INTO TextbookOrder.Major (MajorID, MajorName, CollegeID)
VALUES (10, '统计学', 5);

-- 插入管理员数据
INSERT INTO TextbookOrder.Administrator (AdminID, Name, ContactInfo, Username, Password)
VALUES (1, '张三', 138001380, 'admin001', 'pass123');
INSERT INTO TextbookOrder.Administrator (AdminID, Name, ContactInfo, Username, Password)
VALUES (2, '李四', 139001390, 'admin002', 'pass456');
INSERT INTO TextbookOrder.Administrator (AdminID, Name, ContactInfo, Username, Password)
VALUES (3, '王五', 137001370, 'admin003', 'pass789');

-- 插入学生数据
-- 插入学生数据（修正后的联系方式字段，适配tinyint类型）
INSERT INTO TextbookOrder.Student (StudentID, StudentName, MajorID, StudentContactInfo, StudentUsername,
                                   StudentPassword)
VALUES (1, '张伟', 1, 1, 'stu001', 'pwd001');
INSERT INTO TextbookOrder.Student (StudentID, StudentName, MajorID, StudentContactInfo, StudentUsername,
                                   StudentPassword)
VALUES (2, '李娜', 2, 2, 'stu002', 'pwd002');
INSERT INTO TextbookOrder.Student (StudentID, StudentName, MajorID, StudentContactInfo, StudentUsername,
                                   StudentPassword)
VALUES (3, '王芳', 3, 3, 'stu003', 'pwd003');
INSERT INTO TextbookOrder.Student (StudentID, StudentName, MajorID, StudentContactInfo, StudentUsername,
                                   StudentPassword)
VALUES (4, '刘洋', 1, 4, 'stu004', 'pwd004');
INSERT INTO TextbookOrder.Student (StudentID, StudentName, MajorID, StudentContactInfo, StudentUsername,
                                   StudentPassword)
VALUES (5, '陈静', 5, 5, 'stu005', 'pwd005');
INSERT INTO TextbookOrder.Student (StudentID, StudentName, MajorID, StudentContactInfo, StudentUsername,
                                   StudentPassword)
VALUES (6, '杨强', 4, 6, 'stu006', 'pwd006');
INSERT INTO TextbookOrder.Student (StudentID, StudentName, MajorID, StudentContactInfo, StudentUsername,
                                   StudentPassword)
VALUES (7, '赵敏', 6, 7, 'stu007', 'pwd007');
INSERT INTO TextbookOrder.Student (StudentID, StudentName, MajorID, StudentContactInfo, StudentUsername,
                                   StudentPassword)
VALUES (8, '周杰', 7, 8, 'stu008', 'pwd008');
INSERT INTO TextbookOrder.Student (StudentID, StudentName, MajorID, StudentContactInfo, StudentUsername,
                                   StudentPassword)
VALUES (9, '吴磊', 2, 9, 'stu009', 'pwd009');
INSERT INTO TextbookOrder.Student (StudentID, StudentName, MajorID, StudentContactInfo, StudentUsername,
                                   StudentPassword)
VALUES (10, '郑梅', 8, 10, 'stu010', 'pwd010');

-- 插入教材数据
INSERT INTO TextbookOrder.Textbook (TextbookID, TextbookName, Author, Publisher, Price, MajorID)
VALUES (1, '数据结构与算法', '严蔚敏', '清华大学出版社', 45.0, 1);
INSERT INTO TextbookOrder.Textbook (TextbookID, TextbookName, Author, Publisher, Price, MajorID)
VALUES (2, '操作系统概念', 'Abraham Silberschatz', '高等教育出版社', 89.0, 1);
INSERT INTO TextbookOrder.Textbook (TextbookID, TextbookName, Author, Publisher, Price, MajorID)
VALUES (3, '数据库系统概论', '王珊', '高等教育出版社', 56.0, 1);
INSERT INTO TextbookOrder.Textbook (TextbookID, TextbookName, Author, Publisher, Price, MajorID)
VALUES (4, '软件工程导论', '张海藩', '清华大学出版社', 42.0, 2);
INSERT INTO TextbookOrder.Textbook (TextbookID, TextbookName, Author, Publisher, Price, MajorID)
VALUES (5, 'Java编程思想', 'Bruce Eckel', '机械工业出版社', 108.0, 2);
INSERT INTO TextbookOrder.Textbook (TextbookID, TextbookName, Author, Publisher, Price, MajorID)
VALUES (6, 'Python数据分析', 'Wes McKinney', '机械工业出版社', 119.0, 3);
INSERT INTO TextbookOrder.Textbook (TextbookID, TextbookName, Author, Publisher, Price, MajorID)
VALUES (7, '机器学习', '周志华', '清华大学出版社', 88.0, 4);
INSERT INTO TextbookOrder.Textbook (TextbookID, TextbookName, Author, Publisher, Price, MajorID)
VALUES (8, '深度学习', 'Ian Goodfellow', '人民邮电出版社', 168.0, 4);
INSERT INTO TextbookOrder.Textbook (TextbookID, TextbookName, Author, Publisher, Price, MajorID)
VALUES (9, '管理学原理', '周三多', '高等教育出版社', 58.0, 5);
INSERT INTO TextbookOrder.Textbook (TextbookID, TextbookName, Author, Publisher, Price, MajorID)
VALUES (10, '市场营销学', '菲利普·科特勒', '中国人民大学出版社', 65.0, 5);
INSERT INTO TextbookOrder.Textbook (TextbookID, TextbookName, Author, Publisher, Price, MajorID)
VALUES (11, '会计学基础', '陈信元', '上海财经大学出版社', 48.0, 6);
INSERT INTO TextbookOrder.Textbook (TextbookID, TextbookName, Author, Publisher, Price, MajorID)
VALUES (12, '财务管理', '荆新', '中国人民大学出版社', 52.0, 6);
INSERT INTO TextbookOrder.Textbook (TextbookID, TextbookName, Author, Publisher, Price, MajorID)
VALUES (13, '综合英语教程', '何兆熊', '上海外语教育出版社', 38.0, 7);
INSERT INTO TextbookOrder.Textbook (TextbookID, TextbookName, Author, Publisher, Price, MajorID)
VALUES (14, '英语写作基础', '丁往道', '高等教育出版社', 32.0, 7);
INSERT INTO TextbookOrder.Textbook (TextbookID, TextbookName, Author, Publisher, Price, MajorID)
VALUES (15, '标准日本语', '人民教育出版社', '人民教育出版社', 45.0, 8);
INSERT INTO TextbookOrder.Textbook (TextbookID, TextbookName, Author, Publisher, Price, MajorID)
VALUES (16, '数学分析', '华东师范大学', '高等教育出版社', 78.0, 9);
INSERT INTO TextbookOrder.Textbook (TextbookID, TextbookName, Author, Publisher, Price, MajorID)
VALUES (17, '线性代数', '同济大学', '高等教育出版社', 42.0, 9);
INSERT INTO TextbookOrder.Textbook (TextbookID, TextbookName, Author, Publisher, Price, MajorID)
VALUES (18, '概率论与数理统计', '盛骤', '高等教育出版社', 46.0, 10);
INSERT INTO TextbookOrder.Textbook (TextbookID, TextbookName, Author, Publisher, Price, MajorID)
VALUES (19, '应用统计学', '贾俊平', '中国人民大学出版社', 54.0, 10);
INSERT INTO TextbookOrder.Textbook (TextbookID, TextbookName, Author, Publisher, Price, MajorID)
VALUES (20, '计算机网络', '谢希仁', '电子工业出版社', 49.0, 1);

-- 插入订单数据
INSERT INTO TextbookOrder.`Order` (OrderID, StudentID, TextbookID, Time)
VALUES (1, 1, 1, '2025-12-01 09:30:00');
INSERT INTO TextbookOrder.`Order` (OrderID, StudentID, TextbookID, Time)
VALUES (2, 1, 3, '2025-12-01 10:15:00');
INSERT INTO TextbookOrder.`Order` (OrderID, StudentID, TextbookID, Time)
VALUES (3, 2, 4, '2025-12-02 14:20:00');
INSERT INTO TextbookOrder.`Order` (OrderID, StudentID, TextbookID, Time)
VALUES (4, 2, 5, '2025-12-02 14:25:00');
INSERT INTO TextbookOrder.`Order` (OrderID, StudentID, TextbookID, Time)
VALUES (5, 3, 6, '2025-12-03 11:00:00');
INSERT INTO TextbookOrder.`Order` (OrderID, StudentID, TextbookID, Time)
VALUES (6, 4, 1, '2025-12-03 16:45:00');
INSERT INTO TextbookOrder.`Order` (OrderID, StudentID, TextbookID, Time)
VALUES (7, 4, 20, '2025-12-03 16:50:00');
INSERT INTO TextbookOrder.`Order` (OrderID, StudentID, TextbookID, Time)
VALUES (8, 5, 9, '2025-12-04 08:30:00');
INSERT INTO TextbookOrder.`Order` (OrderID, StudentID, TextbookID, Time)
VALUES (9, 6, 7, '2025-12-05 13:20:00');
INSERT INTO TextbookOrder.`Order` (OrderID, StudentID, TextbookID, Time)
VALUES (10, 7, 11, '2025-12-05 15:10:00');
INSERT INTO TextbookOrder.`Order` (OrderID, StudentID, TextbookID, Time)
VALUES (11, 7, 12, '2025-12-05 15:15:00');
INSERT INTO TextbookOrder.`Order` (OrderID, StudentID, TextbookID, Time)
VALUES (12, 8, 13, '2025-12-06 10:00:00');
INSERT INTO TextbookOrder.`Order` (OrderID, StudentID, TextbookID, Time)
VALUES (13, 9, 4, '2025-12-07 09:45:00');
INSERT INTO TextbookOrder.`Order` (OrderID, StudentID, TextbookID, Time)
VALUES (14, 10, 15, '2025-12-08 14:30:00');
INSERT INTO TextbookOrder.`Order` (OrderID, StudentID, TextbookID, Time)
VALUES (15, 11, 16, '2025-12-09 11:20:00');
INSERT INTO TextbookOrder.`Order` (OrderID, StudentID, TextbookID, Time)
VALUES (16, 12, 18, '2025-12-10 16:00:00');
INSERT INTO TextbookOrder.`Order` (OrderID, StudentID, TextbookID, Time)
VALUES (17, 13, 2, '2025-12-11 08:50:00');
INSERT INTO TextbookOrder.`Order` (OrderID, StudentID, TextbookID, Time)
VALUES (18, 14, 6, '2025-12-12 13:40:00');
INSERT INTO TextbookOrder.`Order` (OrderID, StudentID, TextbookID, Time)
VALUES (19, 15, 10, '2025-12-13 10:30:00');
INSERT INTO TextbookOrder.`Order` (OrderID, StudentID, TextbookID, Time)
VALUES (20, 1, 20, '2025-12-14 15:20:00');