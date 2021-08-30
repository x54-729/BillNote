import sqlite3
import datetime

from Bill import Bill

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

def delete_database():

    with dbopen(dbname) as cursor:
        cursor.execute("DROP TABLE BILLS")
    

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
        res = cursor.execute("SELECT ID, DATE, TYPE, METHOD, DESCRIPTION, AMOUNT, IS_INCOME\
                                FROM BILLS").fetchall()

    return [ Bill(*data) for data in res ]

def change(id, type_, method, description, amount):

    with dbopen(dbname) as cursor:
        cursor.execute("UPDATE BILLS SET TYPE=?, METHOD=?, \
                        DESCRIPTION=?, AMOUNT=? WHERE ID=?", 
                        (type_, method, description, amount, id))
    

def find_by_id(id):

    with dbopen(dbname) as cursor:
        res = cursor.execute("SELECT ID, DATE, TYPE, METHOD, DESCRIPTION, AMOUNT, IS_INCOME \
                                FROM BILLS WHERE ID=?", (id, )).fetchall()
    
    return [ Bill(*data) for data in res ]

def find_by_is_income(is_income):

    with dbopen(dbname) as cursor:
        res = cursor.execute("SELECT ID, DATE, TYPE, METHOD, DESCRIPTION, AMOUNT, IS_INCOME \
                                FROM BILLS WHERE IS_INCOME=?", (is_income, )).fetchall()

    return [ Bill(*data) for data in res ]

def find_by_type(type_):

    with dbopen(dbname) as cursor:
        res = cursor.execute("SELECT ID, DATE, TYPE, METHOD, DESCRIPTION, AMOUNT, IS_INCOME \
                                 FROM BILLS WHERE TYPE=?", (type_, )).fetchall()
    
    return [ Bill(*data) for data in res ]

def find_by_method(method):

    with dbopen(dbname) as cursor:
        res = cursor.execute("SELECT ID, DATE, TYPE, METHOD, DESCRIPTION, AMOUNT, IS_INCOME \
                                FROM BILLS WHERE METHOD=?", (method, )).fetchall()
    
    return [ Bill(*data) for data in res ]

def find_by_filters(from_date, to_date, type_, method, from_amount, to_amount, is_income):

    search_str = "SELECT ID, DATE, TYPE, METHOD, DESCRIPTION, AMOUNT, IS_INCOME \
                FROM BILLS WHERE ? <= DATE AND DATE <= ? AND ? <= AMOUNT AND AMOUNT <= ？AND IS_INCOME = ?"
    format_tuple = (from_date, to_date, from_amount, to_amount, is_income)

    if type_ != "全部":
        search_str += "AND TYPE = ?"
        format_tuple += (type_)
    
    if method != "全部":
        search_str += "AND METHOD = ?"
        format_tuple += (method)

    with dbopen(dbname) as cursor:
        res = cursor.execute(search_str, format_tuple).fetchall()
    
    return [ Bill(*data) for data in res ]

if __name__ == '__main__':

    bills = getall()
    delete_database()
    create_database()
    for b in bills:
        with dbopen(dbname) as cursor:
            cursor.execute("INSERT INTO BILLS (DATE, TYPE, METHOD, DESCRIPTION, AMOUNT, IS_INCOME) \
                            VALUES(?,?,?,?,?,?)", b[1:] + (b.is_income, ))