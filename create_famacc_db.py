import sqlite3.dbapi2
import threading
from _docdulieu_account import DocDuLieuAccCount
import sqlite3



def CREATE():
    contl = sqlite3.connect("DataText/Farm_Info.db")


    cursor = contl.cursor()

    command = """CREATE TABLE Farm_Info( Email TEXT, Password TEXT, SoDao INTEGER, LoaiMo INTEGER, NangCapAH INTEGER, XayNha INTEGER, MainAcc FLOAT)"""

    cursor.execute(command)




#CREATE()



class SQLite():
    '''Doc File Database'''
    def __init__(self, file='sqlite.db'):
        self.file=file
    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        self.conn.row_factory = sqlite3.Row
        return self.conn.cursor()
    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()



def Creat_Databasemoi():
    with SQLite(file ='DataText/Farm_Info.db') as cur:  
        command = """CREATE TABLE Farm_Info( Email TEXT, Password TEXT, SoDao INTEGER, LoaiMo INTEGER, NangCapAH INTEGER, XayNha INTEGER, MainAcc FLOAT)"""

        cur.execute(command)



def Creat_Database():
    print("Loading Database...")

    with SQLite('DataText/Farm_Info.db') as cur:  
        cur.execute("""DELETE FROM Farm_Info""")         

        cur.execute("""INSERT INTO Farm_Info 
                ( Email , Password , SoDao , LoaiMo , NangCapAH , XayNha , MainAcc ) 
                    VALUES 
                    (?, ? ,?, ?, ?, ? ,?)""",("chanhbui@gmail.com","Ngacuong1",5,5,2,6,True))




Creat_Database()
