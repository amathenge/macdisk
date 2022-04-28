drop table if exists disk;

create table disk (id integer primary key autoincrement,
  runid timestamp,
  filesystem varchar(16),
  blocks integer,
  blocks_used integer,
  blocks_available integer,
  used_percent varchar(8),
  mountpoint varchar(32)
);

