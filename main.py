import connection
from utils import get_history, get_abusers

# Moving Average window size
WSIZE = 5
# Moving Average total days 
TSIZE = 10

db_stats = connection.ssh_postgresdb("DB_STATS")
db_gp = connection.ssh_mysqldb("DB_GP")
db_local = connection.local_db()

get_history(db_stats.cur, db_local.cur, db_local.conn, db_gp.cur)
get_abusers(db_local, WSIZE, TSIZE)

db_stats.conn.close()
db_gp.conn.close()
db_local.conn.close()