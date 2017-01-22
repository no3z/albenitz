import os
import sqlite3
import time

dbname = "/home/no3z/albenitz/sensors.db"

def log_data(data):
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    string = "CREATE TABLE IF NOT EXISTS sensors (timestamp DATETIME"
    for k,v in data.iteritems():
        string += ",{0} NUMERIC".format(k)
    string += ")"
        
    curs.execute(string)
    string = "INSERT INTO sensors VALUES(datetime('now')"
    for k,v in data.iteritems():
        string += ", {0}".format(v)
    string += ")"
        
    curs.execute(string)
    conn.commit()
    conn.close()

def get_data(dbname, interval):
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    
    if interval == None:
        curs.execute("SELECT * from sensors")
    else:
        curs.execute("SELECT * from sensors WHERE timestamp>datetime('now','-%s')" % interval)
        rows = curs.fetchall()
        
    conn.close()
    return rows

def create_table(rows):
    chart_table = {}

    for row in rows:
        chart_table[row[0]] = row[1]
        
    return chart_table

def create_yaxis(rows, name, index):
    axis = [name]
    
    for row in rows:
        axis.append(float(row[index]))

    return axis

def create_xaxis(rows):
    axis = ['x']

    for row in rows:
        axis.append(str(row[0]))

    return axis
