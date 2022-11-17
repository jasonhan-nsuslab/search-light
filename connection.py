import psycopg2
import mysql.connector
import configparser
from db import Database
from sshtunnel import SSHTunnelForwarder

vars = configparser.ConfigParser()
vars.read("vars.cfg")

def ssh_postgresdb(db):
    tunnel = SSHTunnelForwarder(
        (vars[db]["ssh_host"], int(vars[db]["ssh_port"])),
        ssh_username=vars[db]["ssh_uname"],
        ssh_pkey=vars[db]["mypkey"],
        remote_bind_address=(vars[db]["sql_hostname"], int(vars[db]["sql_port"]))
    )
    tunnel.start()
    conn = psycopg2.connect(
        host="127.0.0.1", 
        user=vars[db]["sql_uname"],
        password=vars[db]["sql_passwd"],
        database=vars[db]["sql_db"],
        port=tunnel.local_bind_port
    )
    return Database(conn.cursor(), conn)

def ssh_mysqldb(db):
    tunnel = SSHTunnelForwarder(
        (vars[db]["ssh_host"], int(vars[db]["ssh_port"])),
        ssh_username=vars[db]["ssh_uname"],
        ssh_pkey=vars[db]["mypkey"],
        remote_bind_address=(vars[db]["sql_hostname"], int(vars[db]["sql_port"]))
    )
    tunnel.start()
    conn = mysql.connector.connect(
        host="127.0.0.1", 
        user=vars[db]["sql_uname"],
        password=vars[db]["sql_passwd"],
        database=vars[db]["sql_db"],
        port=tunnel.local_bind_port
    )
    return Database(conn.cursor(), conn)

def local_db():
    conn = mysql.connector.connect(
        host=vars["DB_LOCAL"]["sql_hostname"],
        port=vars["DB_LOCAL"]["sql_port"],
        user=vars["DB_LOCAL"]["sql_uname"],
        passwd=vars["DB_LOCAL"]["sql_passwd"],
        database=vars["DB_LOCAL"]["sql_db"]
    )
    return Database(conn.cursor(), conn)