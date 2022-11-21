drop table "Users";

create table "Users"(
    id integer unique,
    nick text,
    reg_date datetime,
    selected_date text,
    selected_command text,
    time_zone integer,
    sharing_id text
)