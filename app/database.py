import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        self.connection = None

    def connect(self):
        if self.connection is None:
            try:
                self.connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    passwd="Npt16012004",
                    database="QL_TAIKHOANTIETKIEM"
                )
                if self.connection.is_connected():
                    print("Connected to MySQL database")
            except Error as e:
                print(f"Error: {e}")
                self.connection = None
        return self.connection
    def get_cursor(self):
        try:
            connection = self.connect()
            if connection:
                return connection.cursor(buffered=True)
            else:
                print("Failed to establish a connection.")
                return None
        except Exception as e:
            print(f"An error occurred while connecting to the database: {e}")
            return None

    
db = Database()
