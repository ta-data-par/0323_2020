### challenge1
-- step1
select t.title_id as titleID, t.price, t.advance, t. royalty, ta.royaltyper, s.qty, a.au_id as authorID, a.au_lname, a.au_fname, (t.price*t.royalty*ta.royaltyper*s.qty/10000) as ROYALTIES
from titles t
inner join sales s on s.title_id = t.title_id
inner join titleauthor ta on ta.title_id = s.title_id
inner join authors a on a.au_id = ta.au_id
order by ROYALTIES desc;

-- step2
select titleID, authorID, sum(ROYALTIES) aggregated_royalties
from (
select t.title_id as titleID, t.price, t.advance, t. royalty, ta.royaltyper, s.qty, a.au_id as authorID, a.au_lname, a.au_fname, (t.price*t.royalty*ta.royaltyper*s.qty/10000) as ROYALTIES
from titles t
inner join sales s on s.title_id = t.title_id
inner join titleauthor ta on ta.title_id = s.title_id
inner join authors a on a.au_id = ta.au_id
order by ROYALTIES desc) as temp
group by titleID, authorID;

-- step3
select authorID, aggregated_royalties
from (
select titleID, authorID, sum(ROYALTIES) aggregated_royalties
from (
select t.title_id as titleID, t.price, t.advance, t. royalty, ta.royaltyper, s.qty, a.au_id as authorID, a.au_lname, a.au_fname, (t.price*t.royalty*ta.royaltyper*s.qty/10000) as ROYALTIES
from titles t
inner join sales s on s.title_id = t.title_id
inner join titleauthor ta on ta.title_id = s.title_id
inner join authors a on a.au_id = ta.au_id
order by ROYALTIES desc) as temp1
group by titleID, authorID) as temp2
order by aggregated_royalties desc
limit 3;

###challege 2 alernative solution
-- step1
CREATE TEMPORARY TABLE temp1
select t.title_id as titleID, t.price, t.advance, t. royalty, ta.royaltyper, s.qty, a.au_id as authorID, a.au_lname, a.au_fname, (t.price*t.royalty*ta.royaltyper*s.qty/10000) as ROYALTIES
from titles t
inner join sales s on s.title_id = t.title_id
inner join titleauthor ta on ta.title_id = s.title_id
inner join authors a on a.au_id = ta.au_id
order by ROYALTIES desc;

-- step2
CREATE TEMPORARY TABLE temp2 
select titleID, authorID, sum(ROYALTIES) aggregated_royalties
from temp1 
group by titleID, authorID;

-- step3
select authorID, aggregated_royalties
from temp2
order by aggregated_royalties desc
limit 3;

###challenge3

-- step4
create table most_profiting_authors
select authorID, aggregated_royalties as profits
from temp3
order by profits desc
limit 3;