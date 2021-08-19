import sqlite3
import datetime
import os

dbname = "bills.db"

class dbopen(object):
    """
    Simple CM for sqlite3 databases. Commits everything at exit.
    Refernce to https://gist.github.com/miku/6522074
    """
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.conn = sqlite3.connect(self.path)
        cursor = self.conn.cursor()
        return cursor

    def __exit__(self, exc_class, exc, traceback):
        self.conn.commit()
        self.conn.close()

def create_database():

    with dbopen(dbname) as cursor:
        cursor.execute("CREATE TABLE BILLS \
                        (ID INTEGER PRIMARY KEY,\
                        DATE DATE NOT NULL,\
                        TYPE CHARACTER(10) NOT NULL,\
                        METHOD CHARACTER(10) NOT NULL,\
                        DESCRIPTION VARCHAR(50),\
                        AMOUNT DOUBLE NOT NULL,\
                        IS_INCOME TINYINT)")
if not os.path.exists(dbname):
    create_database()
    

def insert(type_, method, description, amount, is_income):
    date = datetime.date.today()

    with dbopen(dbname) as cursor:
        cursor.execute("INSERT INTO BILLS (DATE, TYPE, METHOD, DESCRIPTION, AMOUNT, IS_INCOME) \
                        VALUES(?,?,?,?,?,?)", (date, type_, method, description, amount, is_income))
    

def delete(id):

    with dbopen(dbname) as cursor:
        cursor.execute("DELETE FROM BILLS WHERE ID = ?", (id,))
    

def getall():

    with dbopen(dbname) as cursor:
        res = cursor.execute("SELECT ID, DATE, TYPE, METHOD, DESCRIPTION, AMOUNT\
                                FROM BILLS").fetchall()

    return res

def change(id, type_, method, description, amount):

    with dbopen(dbname) as cursor:
        cursor.execute("UPDATE BILLS SET TYPE=?, METHOD=?\
                        DESCRIPTION=?, AMOUNT=? WHERE ID=?", 
                        (type_, method, description, amount, id))
    

def find_by_id(id):

    with dbopen(dbname) as cursor:
        res = cursor.execute("SELECT ID, DATE, TYPE, METHOD, DESCRIPTION, AMOUNT \
                                FROM BILLS WHERE ID=?", (id, )).fetchall()
    
    return res

def find_by_is_income(is_income):

    with dbopen(dbname) as cursor:
        res = cursor.execute("SELECT ID, DATE, TYPE, METHOD, DESCRIPTION, AMOUNT \
                                FROM BILLS WHERE IS_INCOME=?", (is_income, )).fetchall()

    return res

def find_by_type(type_):

    with dbopen(dbname) as cursor:
        res = cursor.execute("SELECT ID, DATE, TYPE, METHOD, DESCRIPTION, AMOUNT \
                                 FROM BILLS WHERE TYPE=?", (type_, )).fetchall()
    
    return res

def find_by_method(method):

    with dbopen(dbname) as cursor:
        res = cursor.execute("SELECT ID, DATE, TYPE, METHOD, DESCRIPTION, AMOUNT \
                                FROM BILLS WHERE METHOD=?", (method, )).fetchall()
    
    return res