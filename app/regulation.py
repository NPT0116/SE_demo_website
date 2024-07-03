from app.database import db
from datetime import datetime

class RegulationManager:
    def __init__(self):
        pass

    def get_minimum_deposit_money(self):
        """Load the latest minimum deposit amount."""
        query = "SELECT amount FROM minimum_deposit_money ORDER BY ID DESC LIMIT 1"
        cursor = db.get_cursor()
        if cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            if result:
                return result[0]

    def get_minimum_withdraw_day(self):
        """Load the latest minimum withdraw day setting."""
        query = "SELECT days FROM minimum_withdraw_day ORDER BY ID DESC LIMIT 1"
        cursor = db.get_cursor()
        if cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            if result:
                return result[0]

    def get_interest_rate(self, term_name):
        query = "SELECT interest_rate FROM terms WHERE term_name = %s"
        cursor = db.get_cursor()
        if cursor:
            try:
                cursor.execute(query, (term_name,))
                result = cursor.fetchone()
                if result:
                    return result[0]  # Return the interest rate found
                else:
                    return None  # Return None if no term is found
            except Exception as e:
                print("Error when trying to fetch interest rate:", e)  # Or use logging to log the error
            finally:
                cursor.close()


    def add_term(self, term_name):
        query = "INSERT INTO terms (term_name) VALUES (%s)"
        cursor = db.get_cursor()
        if cursor:
            try:
                cursor.execute(query, (term_name,))
                db.connection.commit()
            except Exception as e:
                print("Error when trying to add term:", e)  # Or use logging to log the error
            finally:
                cursor.close()

    def update_interest_rate(self, term_name, interest_rate):
        query = "UPDATE terms SET interest_rate = %s WHERE term_name = %s"
        cursor = db.get_cursor()
        if cursor:
            cursor.execute(query, (interest_rate, term_name))
            db.connection.commit()
            cursor.close()


    def add_minimum_deposit_money(self, amount):
        query = "INSERT INTO minimum_deposit_money (amount) VALUES (%s)"
        cursor = db.get_cursor()
        if cursor:
            cursor.execute(query, (amount,))
            db.connection.commit()
            cursor.close()

    def add_minimum_withdraw_day(self, days):
        query = "INSERT INTO minimum_withdraw_day (days) VALUES (%s)"
        cursor = db.get_cursor()
        if cursor:
            cursor.execute(query, (days,))
            db.connection.commit()
            cursor.close()
    def get_terms(self):
        query = "SELECT term_name FROM terms ORDER BY CAST(SUBSTRING_INDEX(term_name, ' ', 1) AS UNSIGNED) ASC;"
        terms = []
        cursor = db.get_cursor()
        if cursor:
            try:
                cursor.execute(query)
                results = cursor.fetchall()
                for row in results:
                    terms.append(row[0])  # Assuming term_name is the first column
            finally:
                cursor.close()
        return terms
    


regulation = RegulationManager()