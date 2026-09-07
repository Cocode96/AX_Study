CREATE TABLE MEMBERS (
	seq SERIAL PRIMARY KEY,
	user_id VARCHAR(50) NOT NULL UNIQUE,
	password VARCHAR(65) NOT NULL,
	cellphone VARCHAR(15),
	age VARCHAR(2),
	created_at TIMESTAMPTZ
);

select * from members m;

ALTER TABLE MEMBERS ADD COLUMN user_name VARCHAR(45) NOT NULL;
ALTER TABLE MEMBERS ADD COLUMN mobile VARCHAR(15);

alter table members drop column cellphone;

ALTER TABLE MEMBERS RENAME COLUMN mobile TO cellphone;

-- age VARCHAR -> INT
ALTER TABLE MEMBERS ALTER COLUMN age TYPE INT USING(age::INT);

-- cellphone + NOT NULL
ALTER TABLE MEMBERS ALTER COLUMN cellphone SET NOT NULL;

-- created_at + 기본값 CURRENT_TIMESTAMP
ALTER TABLE MEMBERS
ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP;



-- CLUB_MEMBERS
CREATE TABLE CLUB_MEMBERS (
	seq SERIAL,
	club_name VARCHAR(40)
);

-- seq 기본키 설정
ALTER TABLE CLUB_MEMBERS
ADD CONSTRAINT pk_club_members PRIMARY KEY(seq);



-- user_seq 필드 추가, 외래키 부여
ALTER TABLE CLUB_MEMBERS ADD COLUMN user_seq INT;

ALTER TABLE CLUB_MEMBERS ADD CONSTRAINT fk_club_members
	FOREIGN KEY (user_seq) REFERENCES MEMBERS(seq);

insert into members (user_id, user_name, password, cellphone, age)
values ('user01', '철수', '1234', '01010001000', 20);

select * from members;

update members
set age = 30, cellphone='01011111111'
where user_id = 'user01';

delete from members where user_id='user01';

select * from members;
