from app.database import db
from datetime import datetime

class RegulationManager:
    def __init__(self):
        self.load_current_settings()

    def load_current_settings(self):
        """Load the current settings for terms and regulations."""
        self.load_current_terms()
        self.load_current_deposit()
        self.load_current_withdraw_day()
    def load_current_terms(self):
        """Load the latest terms from the database."""
        self.terms = {}
        query = "SELECT term_name, interest_rate FROM terms ORDER BY created_at DESC"
        cursor = db.get_cursor()
        if cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            for term in results:
                if term[0] not in self.terms:  # Ensure only the latest for each term is added
                    self.terms[term[0]] = term[1]

    def load_current_deposit(self):
        """Load the latest minimum deposit amount."""
        query = "SELECT amount FROM minimum_deposit_money ORDER BY created_at DESC LIMIT 1"
        cursor = db.get_cursor()
        if cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            if result:
                self.minimum_deposit_money = result[0]

    def load_current_withdraw_day(self):
        """Load the latest minimum withdraw day setting."""
        query = "SELECT days FROM minimum_withdraw_day ORDER BY created_at DESC LIMIT 1"
        cursor = db.get_cursor()
        if cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            if result:
                self.minimum_withdraw_day = result[0]



    def add_term(self, term_name):
        query = "INSERT INTO terms (term_name) VALUES (%s)"
        cursor = db.get_cursor()
        if cursor:
            try:
                cursor.execute(query, (term_name,))
                cursor.connection.commit()
            except Exception as e:
                print("Error when trying to add term:", e)  # Or use logging to log the error
            finally:
                cursor.close()

    def update_interest_rate(self, term_name, interest_rate):
        query = "UPDATE terms SET interest_rate = %s WHERE term_name = %s"
        cursor = db.get_cursor()
        if cursor:
            cursor.execute(query, (interest_rate, term_name))
            cursor.connection.commit()
            cursor.close()


    def add_minimum_deposit_money(self, amount):
        query = "INSERT INTO minimum_deposit_money (amount) VALUES (%s)"
        cursor = db.get_cursor()
        if cursor:
            cursor.execute(query, (amount,))
            cursor.connection.commit()
            cursor.close()

    def add_minimum_withdraw_day(self, days):
        query = "INSERT INTO minimum_withdraw_day (days) VALUES (%s)"
        cursor = db.get_cursor()
        if cursor:
            cursor.execute(query, (days,))
            cursor.connection.commit()
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