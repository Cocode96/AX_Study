truncate table MEMBERS;

select * from MEMBERS;

drop table CLUB_MEMBERS;

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

insert into club_members(user_seq , club_name)
values (3, '통기타');

select * from club_members cm ;