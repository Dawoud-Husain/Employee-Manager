from flask import g 

import sqlite3 

#Connect to the database 
def connect_to_database():
    sql = sqlite3.connect('/employeeapplication.db')
    sql.row_factory = sqlite3.Row
    return sql  

#Get the database 
def get_database():
    if hasattr(g, 'employee_db'):
        g.employee_db = connect_to_database()

    return g.employeeapplication_db


 