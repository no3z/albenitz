import os
import sqlite3
import time

dbname = "/home/no3z/albenitz/sensors.db"

def purge_old_data():
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    string = "DELETE FROM sensors WHERE timestamp <= datetime('now', '-8 days');"

    curs.execute(string)
                                                            
    conn.commit()
    conn.close()
