---
layout: post
title: LeetCode - Database problems summary
tags:
- LeetCode
- Mysql
categories:
- SQL
description: Here is a summary of LeetCode Database section.
---


# Description
Here is a summary of LeetCode Database section.

[Source link](https://leetcode.com/problemset/database/)


# 删除重复数据
Write a SQL query to delete all duplicate email entries in a table named Person, keeping only unique emails based on its smallest Id.

```
+----+------------------+
| Id | Email            |
+----+------------------+
| 1  | john@example.com |
| 2  | bob@example.com  |
| 3  | john@example.com |
+----+------------------+
Id is the primary key column for this table.
```
For example, after running your query, the above Person table should have the following rows:
```
+----+------------------+
| Id | Email            |
+----+------------------+
| 1  | john@example.com |
| 2  | bob@example.com  |
+----+------------------+
```

>删除重复数据是非常普遍和基础的操作。首先我们可以用连接自身以及where条件过滤来完成。

```
delete p1
from Person p1,Person p2
where p1.Email=p2.Email
and p1.id>p2.id
```

>用子查询和min选出每个同名组中最小的id号，删除除了这些id以外的行。

```
delete  from Person
where id not in (select b.id from (select min(id) as id from Person group by Email) b)
```

# 排序问题
Write a SQL query to rank scores. If there is a tie between two scores, both should have the same ranking. Note that after a tie, the next ranking number should be the next consecutive integer value. In other words, there should be no "holes" between ranks.
```
+----+-------+
| Id | Score |
+----+-------+
| 1  | 3.50  |
| 2  | 3.65  |
| 3  | 4.00  |
| 4  | 3.85  |
| 5  | 4.00  |
| 6  | 3.65  |
+----+-------+
```
For example, given the above Scores table, your query should generate the following report (order by highest score):
```
+-------+------+
| Score | Rank |
+-------+------+
| 4.00  | 1    |
| 4.00  | 1    |
| 3.85  | 2    |
| 3.65  | 3    |
| 3.65  | 3    |
| 3.50  | 4    |
+-------+------+
```

>这里用结果集中大于等于当前score的distinct行数来表示某分数在整个结果集中的序列。

```
select s.Score, (select count(*) from (select distinct Score from Scores) s2 where s2.Score>=s.Score) Rank
from Scores s
order by Rank asc
```

# 分组比较问题
The Trips table holds all taxi trips. Each trip has a unique Id, while Client_Id and Driver_Id are both foreign keys to the Users_Id at the Users table. Status is an ENUM type of (‘completed’, ‘cancelled_by_driver’, ‘cancelled_by_client’).
```
+----+-----------+-----------+---------+--------------------+----------+
| Id | Client_Id | Driver_Id | City_Id |        Status      |Request_at|
+----+-----------+-----------+---------+--------------------+----------+
| 1  |     1     |    10     |    1    |     completed      |2013-10-01|
| 2  |     2     |    11     |    1    | cancelled_by_driver|2013-10-01|
| 3  |     3     |    12     |    6    |     completed      |2013-10-01|
| 4  |     4     |    13     |    6    | cancelled_by_client|2013-10-01|
| 5  |     1     |    10     |    1    |     completed      |2013-10-02|
| 6  |     2     |    11     |    6    |     completed      |2013-10-02|
| 7  |     3     |    12     |    6    |     completed      |2013-10-02|
| 8  |     2     |    12     |    12   |     completed      |2013-10-03|
| 9  |     3     |    10     |    12   |     completed      |2013-10-03|
| 10 |     4     |    13     |    12   | cancelled_by_driver|2013-10-03|
+----+-----------+-----------+---------+--------------------+----------+
```
The Users table holds all users. Each user has an unique Users_Id, and Role is an ENUM type of (‘client’, ‘driver’, ‘partner’).
```
+----------+--------+--------+
| Users_Id | Banned |  Role  |
+----------+--------+--------+
|    1     |   No   | client |
|    2     |   Yes  | client |
|    3     |   No   | client |
|    4     |   No   | client |
|    10    |   No   | driver |
|    11    |   No   | driver |
|    12    |   No   | driver |
|    13    |   No   | driver |
+----------+--------+--------+
```
Write a SQL query to find the cancellation rate of requests made by unbanned clients between Oct 1, 2013 and Oct 3, 2013. For the above tables, your SQL query should return the following rows with the cancellation rate being rounded to two decimal places.
```
+------------+-------------------+
|     Day    | Cancellation Rate |
+------------+-------------------+
| 2013-10-01 |       0.33        |
| 2013-10-02 |       0.00        |
| 2013-10-03 |       0.50        |
+------------+-------------------+
```

>将数据集以时间分组，利用case when 来判断是否计入取消订单数。也可以用if语句。

```
select t.Request_at as Day,
round((sum(case when t.Status in ("cancelled_by_driver","cancelled_by_client") then 1 else 0 end)/count(*)),2) as "Cancellation Rate"
from Trips t inner join Users u on t.Client_Id =u.Users_Id
where u.Banned <> "Yes"
and t.Request_at between "2013-10-01" and "2013-10-03"
group by t.Request_at
```

The Employee table holds all employees. Every employee has an Id, and there is also a column for the department Id.
```
+----+-------+--------+--------------+
| Id | Name  | Salary | DepartmentId |
+----+-------+--------+--------------+
| 1  | Joe   | 70000  | 1            |
| 2  | Henry | 80000  | 2            |
| 3  | Sam   | 60000  | 2            |
| 4  | Max   | 90000  | 1            |
| 5  | Janet | 69000  | 1            |
| 6  | Randy | 85000  | 1            |
+----+-------+--------+--------------+
```
The Department table holds all departments of the company.
```
+----+----------+
| Id | Name     |
+----+----------+
| 1  | IT       |
| 2  | Sales    |
+----+----------+
```
Write a SQL query to find employees who earn the top three salaries in each of the department. For the above tables, your SQL query should return the following rows.
```
+------------+----------+--------+
| Department | Employee | Salary |
+------------+----------+--------+
| IT         | Max      | 90000  |
| IT         | Randy    | 85000  |
| IT         | Joe      | 70000  |
| Sales      | Henry    | 80000  |
| Sales      | Sam      | 60000  |
+------------+----------+--------+
```

>取top3的分组数据和取最大分组salary有所不同。后者可以用where salary in （select max(salary) ..group by ）子查询语句来实现。
这里运用了排序问题中的思想。将当前salary与同一group中（表现为departmentid相等），大于等于当前distinct的salary的数量作为该salary的rank。其他限制条件就迎刃而解了。

```
select d.Name Department, e1.Name Employee, e1.Salary
from Employee e1
join Department d
on e1.DepartmentId = d.Id
where 3 > (select count(distinct(e2.Salary))
                  from Employee e2
                  where e2.Salary > e1.Salary
                  and e1.DepartmentId = e2.DepartmentId
                  );
```
