### challenge1
select a.au_id, a.au_lname, a.au_fname, t.title, p.pub_name
from authors a
inner join titleauthor ta on a.au_id = ta.au_id
inner join titles t on t.title_id = ta.title_id
inner join publishers p on p.pub_id = t.pub_id
order by a.au_id;