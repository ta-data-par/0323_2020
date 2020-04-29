use new_schema;

select district_id, count(distinct account_id) as ac_freq
from account
group by district_id
order by ac_freq desc
limit 5;

select account_id, group_concat(distinct bank_to), group_concat(distinct amount), count(distinct amount) as diff
from new_schema.order
where k_symbol='SIPO'
group by account_id
having diff>1;

select ml.account_id, district_id, max(amount)
from
(select account_id,amount from new_schema.order where k_symbol='UVER') ml
inner join account on account.account_id=ml.account_id
group by district_id
order by 3 desc
limit 5;

select ml.account_id, district_id, avg(amount)
from
(select account_id,amount from new_schema.order where k_symbol='UVER') ml
inner join account on account.account_id=ml.account_id
group by district_id
order by 3 desc
limit 5;

create table xxx
select l.account_id, district_id, amount
from account a
inner join loan l on l.account_id=a.account_id;


select * from xxx;

select district_id, sum(amount) as total_amount, group_concat(account_id) 
from xxx 
group by district_id 
order by 2 desc;

select x1.district_id, x1.amount, xxx.account_id
from (select district_id, max(amount) as amount, group_concat(account_id) 
from xxx 
group by district_id) as x1
inner join xxx on xxx.district_id=x1.district_id
where xxx.amount=x1.amount;

select *
from xxx as x1, xxx as x2;

select count(*) as one_table from xxx;
# merge every single row with every single row
select *
from xxx as x1, xxx as x2;

select *
from 
(select x1.district_id, x1.amount,count(x2.amount) ranking
from xxx as x1, xxx as x2
where x1.amount<x2.amount and x1.district_id=x2.district_id
group by x1.district_id, x1.amount
order by x1.district_id, x1.amount,
x2.amount) ranked;

select x1.district_id, ceil(count(x1.amount)/2) ranking
from xxx x1
group by district_id;

select district_id, amount, ranking
from 
(select x1.district_id, x1.amount,count(x2.amount) ranking
from xxx as x1, xxx as x2
where x1.amount<x2.amount and x1.district_id=x2.district_id
group by x1.district_id, x1.amount
order by x1.district_id, x1.amount,
x2.amount) ranked
where exists(
select x1.district_id, ceil(count(x1.amount)/2) ranking
from xxx x1
group by district_id
having ranked.district_id=x1.district_id
and ranked.ranking=ranking)