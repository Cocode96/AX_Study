create table MEMBERS(
	--seq INT generated always as identity primary key, -- 자동 증감 기본키
	seq SERIAL primary key, -- 자동 증감 기본키
	user_id VARCHAR(50) unique not null, -- 유일값 null 허용 x
	password VARCHAR(65) not null, -- null 허용 x
	user_name VARCHAR(45) not null,
	cellphone VARCHAR(15),
	email VARCHAR(70),
	address VARCHAR(100),
	zipcode VARCHAR(10),
	created_at TIMESTAMP
);

-- MEMBERS 테이블을 삭제한다
drop  table MEMBERS;

-- INSERT
insert into MEMBERS(user_id, password, user_name)
values ('user02', '1234', '사용자01');

-- SELECT 조회
select * from members

-- 복합키
create table CLUB_MEMBERS(
	user_seq INT,
	club_name VARCHAR(50),
	user_name VARCHAR(45),
	age INT CHECK(age <= 25),
	created_at TIMESTAMPTZ default current_timestamp,
	primary key(user_seq, club_name)
);

-- 삭제
drop table CLUB_MEMBERS;

-- INSERT
insert into CLUB_MEMBERS (user_seq , club_name, user_name, age)
values(3, '통기타', '김철수', 23);

select * from club_members;
