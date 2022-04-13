drop table "Users";

create table "Users"(
    id integer unique,
    nick text,
    reg_date datetime
)