
create definer = root@localhost view TextbookOrder.student_order_view as
select `o1`.`OrderID`     AS `OrderID`,
       `s`.`StudentName`  AS `StudentName`,
       `t`.`TextbookName` AS `TextbookName`,
       `t`.`Price`        AS `Price`,
       `t`.`TextbookID`   AS `TextbookID`,
       `t`.`MajorID`      AS `MajorID`,
       `m`.`MajorName`    AS `MajorName`,
       `c`.`CollegeName`  AS `CollegeName`,
       `c`.`CollegeID`    AS `CollegeID`
from ((((`textbookorder`.`student` `s` join `textbookorder`.`order` `o1`
         on ((`s`.`StudentID` = `o1`.`StudentID`))) join `textbookorder`.`textbook` `t`
        on ((`t`.`TextbookID` = `o1`.`TextbookID`))) join `textbookorder`.`major` `m`
       on ((`t`.`MajorID` = `m`.`MajorID`))) join `textbookorder`.`college` `c`
      on ((`m`.`CollegeID` = `c`.`CollegeID`)));

-- comment on column TextbookOrder.student_order_view.OrderID not supported: 订单号

-- comment on column TextbookOrder.student_order_view.StudentName not supported: 姓名

-- comment on column TextbookOrder.student_order_view.TextbookName not supported: 教材的名称

-- comment on column TextbookOrder.student_order_view.Price not supported: 教材的价格

-- comment on column TextbookOrder.student_order_view.TextbookID not supported: 教材编号

-- comment on column TextbookOrder.student_order_view.MajorID not supported: 关联专业

-- comment on column TextbookOrder.student_order_view.MajorName not supported: 专业的名称

-- comment on column TextbookOrder.student_order_view.CollegeName not supported: 学院的名称

-- comment on column TextbookOrder.student_order_view.CollegeID not supported: 学院ID

grant select on table TextbookOrder.student_order_view to student;

