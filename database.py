import pyodbc

# Global variables for connection and cursor
conn = None
cursor = None

def connect_to_database():
    global conn, cursor
    #conn_str = r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=F:\AE Scripts\GetData\myDB.accdb;'
    #conn = pyodbc.connect(conn_str)
    #cursor = conn.cursor()

    try:
        # Connect to the Access database
        conn_str = r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=F:\AE Scripts\GetData\myDB.accdb;'
        conn = pyodbc.connect(conn_str)

        # Create a cursor object
        cursor = conn.cursor()

        print("Database connection successfull.")
        return conn, cursor

    except pyodbc.Error as e:
        print("Error connecting to the database:", e)

    return None, None

def close_database_connection():
    global conn, cursor
    if cursor:
        cursor.close()
        print("Cursor Closed")
    if conn:
        conn.close()
        print("Connection CLosed")
