create table lib (
	id bigserial PRIMARY KEY,
	book_name varchar(200),
	author varchar(200),
	years smallint,
	pages integer,
	copies bigint);
	
create table in_hand (
	person_mame varchar(500),
	book_id integer not null references lib(id),
	date_give date,
	date_back date);
	
insert into lib (book_name, author, years, pages, copies) values 
	('The Hitchhikers Guide to the Galaxy', 
 	'Douglas Adams',
	1979,
	180,
	10000);
	
insert into lib (book_name, author, years, pages, copies) values 
	('Dandelion Wine', 
 	'Ray Bradbury',
	1957,
	281,
	10000);
	
delete from lib where book_name = 'Dandelion Wine';

update lib set copies = 15000 where author = 'Douglas Adams';

select count(*) from in_hand where date_back is null;

select book_name from lib 
right join (select book_id, count(book_id) as cnt from in_hand group by book_id order by cnt desc limit 3) as ih 
on lib.id = ih.book_id;
