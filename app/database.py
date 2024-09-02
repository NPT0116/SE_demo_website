import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        self.connection = None

    def connect(self):
        if self.connection is None or not self.connection.is_connected():
            try:
                self.connection = mysql.connector.connect(
                    host="localhost",
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
        connection = self.connect()
        if connection:
            return connection.cursor(buffered=True)
        else:
            print("Failed to establish a connection.")
            return None

    def execute_query(self, query):
        cursor = self.get_cursor()
        if cursor:
            try:
                cursor.execute(query)
                result = cursor.fetchall()
                cursor.close()  # Ensure the cursor is closed after execution
                return result
            except Error as e:
                print(f"Query failed: {e}")
                cursor.close()
                return None
        else:
            print("No cursor available.")
            return None

db = Database()
