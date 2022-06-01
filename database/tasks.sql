drop table "Tasks";

create TABLE "Tasks" (
    id integer unique primary key AUTOINCREMENT,
    name text,
    date text,
    start_time text,
    end_time text,
    user_id integer,
    desc text
)