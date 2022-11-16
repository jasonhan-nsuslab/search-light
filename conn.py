import psycopg2
import mysql.connector
import configparser
from db import Database
from sshtunnel import SSHTunnelForwarder

vars = configparser.ConfigParser()
vars.read("vars.cfg")

def get_db_stats():
    tunnel = SSHTunnelForwarder(
        (vars["DB_STATS"]["ssh_host"], int(vars["DB_STATS"]["ssh_port"])),
        ssh_username=vars["DB_STATS"]["ssh_uname"],
        ssh_pkey=vars["DB_STATS"]["mypkey"],
        remote_bind_address=(vars["DB_STATS"]["sql_hostname"], int(vars["DB_STATS"]["sql_port"]))
    )
    tunnel.start()
    conn = psycopg2.connect(
        host="127.0.0.1", 
        user=vars["DB_STATS"]["sql_uname"],
        password=vars["DB_STATS"]["sql_passwd"], 
        database=vars["DB_STATS"]["sql_db"],
        port=tunnel.local_bind_port
    )
    return Database(conn.cursor(), conn)

def get_db_local():
    conn = mysql.connector.connect(
        host=vars["DB_LOCAL"]["sql_hostname"],
        user=vars["DB_LOCAL"]["sql_uname"],
        passwd=vars["DB_LOCAL"]["sql_passwd"],
        database=vars["DB_LOCAL"]["sql_db"]
    )
    return Database(conn.cursor(), conn)