-- character_id | character_name | quest_id | quest_name | cleared | shop_id | shop_name

truncate table MEMBERS;

select * from MEMBERS;

drop table CLUB_MEMBERS;
drop table members;

insert into members (user_id, user_name, password)
values ('user01', '김철수', '1234');

delete from members where seq=3;

-- 외래키
create table CLUB_MEMBERS(
	seq SERIAL primary key,
	user_seq INT references MEMBERS(seq) on delete cascade,
	club_name VARCHAR(40),
	created_at TIMESTAMPTZ default CURRENT_TIMESTAMP
); -- 한명의 유저가 여러개의 클럽에 들어갈 수 있기 때문에 이렇게 한다.

CREATE TABLE members (
    member_id  INT  primary key,
    name       VARCHAR(50)  not null,
    email      VARCHAR(100)  unique not null,
    joined_at  DATE not null default current_date
);

select * from members;

insert into members (member_id, name, email)
values (1, '김철수', 'cjftn@example.com'),
(2, '이영희', 'dudgml@example.com'),
(3, '노숙희', 'tnrgml@example.com');

insert into members (member_id, name, email)
values (4, '이미영', 'aldud@example.com');

insert into members (member_id, name, email)
values (5, '구자철', 'asdf@example.com');

delete from members where member_id = 5;

SELECT
    version(),
    inet_server_addr(),
    inet_server_port(),
    current_database(),
    current_user;

CREATE TABLE items (
    item_id INT PRIMARY KEY,
    item_name VARCHAR(20) NOT NULL,
    price INT NOT NULL,
    item_type VARCHAR(20),
    description VARCHAR(50)
);

select * from items;

INSERT INTO items (item_id, item_name, price, item_type, description)
VALUES
    (1, '철검', 1000, 'WEAPON', '초보자용 검'),
    (2, '가죽 갑옷', 1500, 'ARMOR', '초보자용 갑옷'),
    (3, '체력 물약', 500, 'CONSUMABLE', '체력을 회복한다');

ALTER table items
add column rarity varchar(50);

alter table items
alter column item_name type varchar(50);

alter table items
add constraint uq_item_name unique (item_name);

alter table items
drop column description;
