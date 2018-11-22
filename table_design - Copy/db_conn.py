import pyodbc


def conn_db():
    """creating method to connect db"""
    con = pyodbc.connect("Driver={ODBC Driver 11 for SQL Server};SERVER=cesdevsvr01\mssqldev; \
                         DATABASE=HBK_Test;UID=kokila;PWD=Prajju@24")
    cursor = con.cursor()
    return cursor


CURSOR = conn_db()
