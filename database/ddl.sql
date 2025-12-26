
create table TextbookOrder.Administrator
(
    AdminID     tinyint auto_increment comment '管理员ID'
        primary key,
    Name        mediumtext  not null comment '管理员姓名',
    ContactInfo int         not null comment '管理员的联系方式',
    Username    varchar(50) not null comment '管理员登录账号',
    Password    varchar(50) null comment '管理员登录密码'
)
    comment '管理员表' charset = utf8;

create table TextbookOrder.College
(
    CollegeID   tinyint auto_increment comment '学院ID'
        primary key,
    CollegeName varchar(50) not null comment '学院的名称'
)
    comment '学院表' charset = utf8;

create table TextbookOrder.Major
(
    MajorID   tinyint auto_increment comment '专业ID'
        primary key,
    MajorName varchar(50) not null comment '专业的名称',
    CollegeID tinyint     not null comment '关联到所属学院的ID',
    constraint Major_College_CollegeID_fk
        foreign key (CollegeID) references textbookorder.College (CollegeID)
)
    comment '专业表' charset = utf8;

create table TextbookOrder.`Order`
(
    OrderID    tinyint auto_increment comment '订单号'
        primary key,
    StudentID  tinyint                             not null comment '关联到学生的学号',
    TextbookID tinyint                             not null comment '关联到教材的编号',
    Time       timestamp default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP comment '订单生成时间',
    constraint Order_Student_StudentID_fk
        foreign key (StudentID) references textbookorder.Student (StudentID),
    constraint Order_Textbook_TextbookID_fk
        foreign key (TextbookID) references textbookorder.Textbook (TextbookID)
)
    comment '订单表';

create table TextbookOrder.order_log
(
    log_id        int auto_increment
        primary key,
    log_message   varchar(255)                        null,
    log_timestamp timestamp default CURRENT_TIMESTAMP not null
);

create table TextbookOrder.Student
(
    StudentID          tinyint     not null comment '学号'
        primary key,
    StudentName        varchar(50) not null comment '姓名',
    MajorID            tinyint     not null comment '关联到所属专业的ID',
    StudentContactInfo tinyint     not null comment '学生的联系方式',
    StudentUsername    varchar(50) not null comment '学生登录的账号',
    StudentPassword    varchar(50) null comment '学生账号的密码',
    constraint Student_Major_MajorID_fk
        foreign key (MajorID) references textbookorder.Major (MajorID)
)
    comment '学生表' charset = utf8;

create index Student_StudentName_index
    on TextbookOrder.Student (StudentName);

create table TextbookOrder.Textbook
(
    TextbookID   tinyint auto_increment comment '教材编号'
        primary key,
    TextbookName varchar(100) not null comment '教材的名称',
    Author       varchar(50)  not null comment '教材的作者',
    Publisher    varchar(100) not null comment '教材的出版社',
    Price        double       not null comment '教材的价格',
    MajorID      tinyint      not null comment '关联专业'
)
    comment '教材表' charset = utf8;

create index Textbook_TextbookName_index
    on TextbookOrder.Textbook (TextbookName);


