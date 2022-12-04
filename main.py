import connection
import mysql.connector
from utils import get_history, get_abusers

# Moving Average window size
WSIZE = 5
# Moving Average total days 
TSIZE = 10

mydb = mysql.connector.connect(
  host="localhost",
  user="admin_cp",
  passwd="qwer1234",
  port="3307"
)

cursor = mydb.cursor()

with open('tables.sql', 'r') as f:
    cursor.execute(f.read(), multi=True)

mydb.commit()

db_stats = connection.ssh_postgresdb("DB_STATS")
db_gp = connection.ssh_mysqldb("DB_GP")
db_local = connection.local_db()

get_history(db_stats.cur, db_local.cur, db_local.conn, db_gp.cur)
get_abusers(db_local, WSIZE, TSIZE)

db_stats.conn.close()
db_gp.conn.close()
db_local.conn.close()