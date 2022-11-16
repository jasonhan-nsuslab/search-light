import conn
from utils import get_positive_rtps

stats = conn.get_db_stats()
print(get_positive_rtps(stats.cur, stats.conn))