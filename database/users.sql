drop table "Users";


create table "Users"(
    id integer unique not null ,
    nick text,
    reg_date datetime
)