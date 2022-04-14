drop table "tasks";

create TABLE "tasks" (
    id integer unique primary key AUTOINCREMENT,
    name text,
    start_time datetime,
    end_time datetime,
    user_id integer unique,
    desc text
)