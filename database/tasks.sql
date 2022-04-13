drop table "tasks";

create TABLE "tasks" (
    id integer unique primary key AUTOINCREMENT,
    name text,
    start_time text,
    end_time text,
    user_id integer unique,
    desc text
)