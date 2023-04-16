drop table if exists disk;

create table disk (id integer primary key autoincrement,
  runid timestamp,
  filesystem varchar(16),
  blocks integer,
  blocks_used integer,
  blocks_available integer,
  used_percent varchar(8),
  mount_point varchar(32)
);


drop table if exists log;

create table log (
    id integer primary key autoincrement,
    logtime datetime,
    message text
);
