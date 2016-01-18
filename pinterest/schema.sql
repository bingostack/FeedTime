drop table if exists pins;
create table pins (
    id integer primary key autoincrement,
    sourceboard text not null,
    targetboard text not null,
    note text,
    image_url text not null,
    link text,
    datetime text not null,
    is_posted integer not null default 0,
    pin_user text not null,
    pin_id text not null
);
