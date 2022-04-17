drop table "Users";

create table "Users"(
    id integer unique,
    nick text,
    reg_date datetime,
    selected_date text,
    selected_command text
)