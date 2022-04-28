select * from disk where runid = (select max(runid) from disk)

