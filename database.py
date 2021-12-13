from flask import g
import sqlite3

def connect_db():
    sql = sqlite3.connect('C:/Users/sm21183/Flask/API_Flask/members.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite3'):
        g.sqlite_db = connect_db()
        return g.sqlite_db
