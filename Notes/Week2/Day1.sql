select job_id
from jobs;

select job_id, job_desc
from jobs;

select * 
from jobs;

select * from jobs;

select 

*

from 

jobs;


select * from authors;

select distinct au_lname, au_fname from authors; # syntax error 

select * from authors
where state='CA'
;

select * from authors
where state='CA' and contract!=1
;

select * from authors
where (state='CA' and contract!=1) or state='KS'
;

select * from authors
where state='KS';

select * from authors
where state='IN' or state='CA';

select * from authors
where state in ('IN','CA','Paris');

select * from authors
where not contract=1 and state not in ('IN','KS');

select * from authors
where not contract=1;

select * from authors 
where au_fname like '%star';


select * from authors 
where au_fname like '%r';


select * from authors 
where address like '%6%';

select *
from discounts;

select * from discounts
order by discount;

select * from discounts
order by discount desc;

select * from discounts
order by discount desc
limit 1;

select * from discounts
where stor_id is null;

select * from authors;

select * from titles;

select * from titleauthor
order by title_id;


select * from publishers;

select * from titles
inner join publishers on titles.pub_id=publishers.pub_id;

select publishers.pub_id, count(title) as titles from titles
right join publishers on titles.pub_id=publishers.pub_id
group by publishers.pub_id
;


select stor_name, ucase(city)
from stores;

select stor_name, lcase(city)
from stores;

select count(stor_name), lcase(city)
from stores
group by city;

select count(title) as number_of_books, type, group_concat(title)
from titles
group by type;

select *
from titles;

select *
from sales;

select t.title_id, sum(qty), count( distinct t.price), max(t.price), t.title, t.type
from sales s
inner join titles t
on s.title_id=t.title_id
group by title_id;

select t.title_id, sum(qty), count( distinct t.price), max(t.price), t.title, t.type
from sales s
inner join titles t
on s.title_id=t.title_id
group by title_id,t.title, t.type;

select t.title_id, sum(qty)*max(t.price) as revenue, t.title, t.type
from sales s
inner join titles t
on s.title_id=t.title_id
group by title_id,t.title, t.type;

select length(title)
from titles;
