
create
    definer = root@localhost procedure TextbookOrder.p1(IN id int)
begin
SELECT
    TextbookName,
    COUNT(TextbookID) AS '订购数量'
FROM Student_Order_View
WHERE CollegeID = id
GROUP BY TextbookName;
end;


create
    definer = root@localhost procedure TextbookOrder.pCollege(IN id int)
begin
SELECT
    TextbookName,
    COUNT(TextbookID) AS '订购数量'
FROM Student_Order_View
WHERE CollegeID = id
GROUP BY TextbookName;
end;

create
    definer = root@localhost procedure TextbookOrder.pMajor(IN id int)
begin
SELECT
    TextbookName,
    COUNT(TextbookID) AS '订购数量'
FROM Student_Order_View
WHERE MajorID = id
GROUP BY TextbookName;
end;

create
    definer = root@localhost procedure TextbookOrder.pOderBook()
begin
SELECT
    TextbookName,
    COUNT(TextbookID) AS '订购数量'
FROM Student_Order_View
GROUP BY TextbookName;
end;


create
    definer = root@localhost procedure TextbookOrder.log_order_changes(IN action varchar(50), IN order_id int)
BEGIN
    DECLARE log_message VARCHAR(255);
    SET log_message = CONCAT(action, ' order with ID ', order_id);
    INSERT INTO order_log (log_message) VALUES (log_message);
END;

