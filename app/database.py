import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        self.connection = None

    def connect(self):
        if self.connection is None:
            try:
                self.connection = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    passwd="Lhd@t2204",
                    database="QL_TAIKHOANTIETKIEM"
                )
                if self.connection.is_connected():
                    print("Connected to MySQL database")
            except Error as e:
                print(f"Error: {e}")
                self.connection = None
        return self.connection

    def get_cursor(self):
        connection = self.connect();
        connection.reconnect();
        if connection:
            return connection.cursor(buffered=True)
        return None
    
db = Database()
