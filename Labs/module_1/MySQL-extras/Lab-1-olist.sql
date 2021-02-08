use olist;

###1. From the order_items table, find the price of the highest priced order and lowest price order.
select min(price), max(price)
from order_items;

###2. From the order_items table, what is range of the shipping_limit_date of the orders?
select min(shipping_limit_date), max(shipping_limit_date)
from order_items;

###3. From the customers table, find the states with the greatest number of customers.
SELECT  customer_state, count(customer_id)
from customers
group by customer_state
order by 2 desc
limit 3;

###4. From the customers table, within the state with the greatest number of customers, find the cities with the greatest number of customers.
SELECT customer_city, customer_state, count(customer_id)
from customers
where customer_state = 'SP'
group by customer_city
order by 3 desc
limit 3;

###5. From the closed_deals table, how many distinct business segments are there (not including null)?
select count(distinct business_segment)
from closed_deals;

###6. From the closed_deals table, sum the declared_monthly_revenue for duplicate row values in business_segment and find the 3 business segments with the highest declared monthly revenue (of those that declared revenue).
select business_segment, sum(declared_monthly_revenue)
from closed_deals
group by business_segment
order by 2 desc
limit 3;

###7. From the order_reviews table, find the total number of distinct review score values.
select count(distinct review_score)
from order_reviews;

###8. In the order_reviews table, create a new column with a description that corresponds to each number category for each review score from 1 - 5, then find the review score and category occurring most frequently in the table.

select distinct review_score, count(review_score) as review_occuracy
from order_reviews
group by review_score
order by review_score desc;

###9. From the order_reviews table, find the review value occurring most frequently and how many times it occurs.
select distinct review_score as review_score_level, count(review_score) as review_occuracy
from order_reviews
group by review_score
order by review_occuracy desc
limit 1;
