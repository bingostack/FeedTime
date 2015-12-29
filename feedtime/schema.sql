drop table if exists pins
create table pins (
    id integer primary key autoincrement,
    board_owner text not null,
    board_name text not null,
    note text,
    image_url text not null,
    link text,
    post_datetime text not null
);
