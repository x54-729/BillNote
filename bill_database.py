import sqlite3
import datetime

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

class Database:

    def __init__(self, name):
        
        self.name = name

    def create_database(self):

        with dbopen(self.name) as cursor:
            cursor.execute("CREATE TABLE BILLS \
                            (ID INT PRIMARY KEY NOT NULL,\
                            DATE DATE NOT NULL,\
                            AMOUNT DOUBLE NOT NULL,\
                            DESCRIPTION VARCHAR(50),\
                            METHOD CHARACTER(10) NOT NULL,\
                            TYPE CHARACTER(10) NOT NULL,\
                            IS_INCOME TINYINT")
        

    def insert(self, amount, description, method, type_, is_income):
        date = datetime.date.today()

        with dbopen(self.name) as cursor:
            cursor.execute("INSERT INTO BILLS (DATE, AMOUNT, DESCRIPTION, METHOD, TYPE, IS_INCOME) \
                            VALUES(?,?,?,?,?,?)", (date, amount, description, method, type_, is_income))
        

    def delete(self, id):

        with dbopen(self.name) as cursor:
            cursor.execute("DELETE FROM BILLS WHERE ID = ?", (id,))
        

    def getall(self):

        with dbopen(self.name) as cursor:
            res = cursor.fetchall()
            
        return res

    def change(self, id, amount, description, method, type_, is_income):

        with dbopen(self.name) as cursor:
            cursor.execute("UPDATE BILLS SET AMOUNT=?, DESCRIPTION=?, METHOD=?\
                            TYPE=?, IS_INCOME=? WHERE ID=?", 
                            (amount, description, method, type_, is_income, id))
        

    def find_by_id(self, id):

        with dbopen(self.name) as cursor:
            res = cursor.execute("SELECT * FROM BILLS WHERE ID=?", (id, ))
        
        return res

    def find_by_is_income(self, is_income):

        with dbopen(self.name) as cursor:
            res = cursor.execute("SELECT * FROM BILLS WHERE IS_INCOME=?", (is_income, ))
        
        return res

    def find_by_type(self, type_):

        with dbopen(self.name) as cursor:
            res = cursor.execute("SELECT * FROM BILLS WHERE TYPE=?", (type_, ))
        
        return res

    def find_by_method(self, method):

        with dbopen(self.name) as cursor:
            res = cursor.execute("SELECT * FROM BILLS WHERE METHOD=?", (method, ))
        
        return res