select first_name, last_name, email from customers;
select product_id, list_price, discount from order_items;
select * from products;

select distinct store_id from orders;

-- store_id + staff_id를 조합한 중복 제거
select distinct store_id, staff_id from orders;
select distinct state from customers;
select distinct brand_id from products;

select distinct store_id from orders where store_id > 1;

select * from orders where shipped_date = '';
select * from orders where shipped_date is null;
select * from staffs where store_id = 1;

select * from products where list_price >= 500 and list_price <= 1000;

select order_id, product_id, list_price,
	case when list_price < 100 then '적다'
		 when list_price < 500 then '중가'
	else '고가'
	end as price_grade
from order_items;

select order_id, product_id, list_price as price,
	case when list_price < 100 then '적다'
		 when list_price < 500 then '중가'
	else '고가'
	end as price_grade
from order_items;

select  * from products where product_name like 'Trek';

select * from products where product_name like 'Trek%' -- 상품명이 Trek으로 시작하는 패턴


select * from orders where order_date >= '2016-01-01' and order_date <= '2016-01-31';

select * from customers where state = 'NY' or state = 'CA';

select * from customers
where state in ('NY', 'CA');

select * from customers
where state not in ('NY', 'CA');

select * from products order by list_price desc;
select * from products order by list_price asc;

select * from orders order by store_id asc;

select count(*) "총 주문건수" from orders;

select avg(list_price) 평균, max(list_price) 최대값, min(list_price) 최소값
from products group by brand_id order by brand_id;

select brand_id, product_name, count(*) "상품 갯수" from products
group by brand_id, product_name order by brand_id asc;

select brand_id, product_name, count(*) "상품 갯수" from products
-- where count(*) >= 100
group by brand_id, product_name  having count(*) >= 1 order by brand_id asc;

select product_name from products;

select category_id, avg(list_price) 평균
from products
group by category_id
having avg(list_price) >= 500;

-- 1월 17일 이전 = 46개
select order_id, order_date from orders
where order_date <= '2016-01-17' order by order_date;

-- 1월 15일 이후 =
select order_id, order_date from orders
where order_date >= '2016-01-15' order by order_date;

-- 공통 레코드 조회(교집합 - intersect)
select order_id, order_date from orders
where order_date <= '2016-01-17'
intersect
select order_id, order_date from orders
where order_date >= '2016-01-15'
order by order_date;

select order_id, order_date from orders
where order_date <= '2016-01-17'
union
select order_id, order_date from orders
where order_date >= '2016-01-15'
order by order_date;

select order_id, order_date from orders
where order_date <= '2016-01-17'
except
select order_id, order_date from orders
where order_date >= '2016-01-15'
order by order_date;

-- 가능한 조합을 다 만든다. 카페시안 곱
select * from orders, stores;
select * from orders, stores where orders.store_id = stores.store_id; -- 주문이 발생한 매장 정보

select * from orders o --동등 조인
inner join stores s on o.store_id = s.store_id;

select * from orders o --동등 조인
join stores s on o.store_id = s.store_id;

insert into stores (store_id, store_name)
values (4, 'sparta market');

-- stores 기준에서 orders 테이블의 정보를 결합
select * from orders o --동등 조인
inner join stores s on o.store_id = s.store_id;

select * from orders o
left join stores s on o.store_id = s.store_id;

insert into orders (order_id, customer_id, order_date)
values(1700, 1, current_timestamp);

select * from orders o
full outer join stores s on o.store_id = s.store_id;

select * from orders o
right join stores s on o.store_id = s.store_id
order by s.store_id, o.order_id;

select o.order_id, o.order_date , s.store_name , f.first_name staff_first_name, c.first_name, c.last_name
from orders o
left join customers c  on o.customer_id = c.customer_id
left join stores s on s.store_id = o.store_id
left join staffs f on o.staff_id = s.store_id;
