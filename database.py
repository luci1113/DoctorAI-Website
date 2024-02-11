import sqlite3
from flask import g

def connect_to_database():
    sql= sqlite3.connect("D:/Project App/Sem 7/Project based/New Start/final model/final_website_doctorAI/employee.db")
    sql.row_factory=sqlite3.Row
    return sql

def get_database():
    if not hasattr(g,"employee_db"):
        g.employee_db=connect_to_database()
        return g.employee_db