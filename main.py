import connection
from utils import get_positive_rtps, get_nicknames

db_stats = connection.ssh_postgresdb("DB_STATS")
db_gp = connection.ssh_mysqldb("DB_GP")
db_local = connection.local_db()

get_positive_rtps(db_stats.cur, db_local.cur, db_local.conn)
get_nicknames(db_local.cur, db_local.conn, db_gp.cur)

db_stats.conn.close()
db_gp.conn.close()
db_local.conn.close()