"""Database operations to store history data"""
import os
import sqlite3

class LocalHistory:
    """
    Local fixer database based on dates the user queried the API
    """
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        self.directory_check()

    def create_tables(self, path):
        """Creates the necessary table"""
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE rates
                          (retrieved_at DATE, tox TEXT, fromx TEXT, rate DOUBLE)''')
        self.connection.commit()

    def directory_check(self):
        """
        Checks whether the directory to store the history exists. If it doesn't, then create it.
        """
        if not os.path.exists(os.getenv('APPDATA') + '\\fixer'):
            os.mkdir(os.getenv('APPDATA') + '\\fixer')
        if not os.path.isfile(os.getenv('APPDATA') + '\\fixer\\history.db'):
            self.create_tables(self.db_path)
        else:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()

    def close(self):
        """Commits and then closes the connection to sqlite3"""
        self.connection.commit()
        self.connection.close()

    def get_rate(self, tox, fromx, when):
        """Tries to get a currency rate conversion at a certain date"""
        args = (tox, fromx, when)
        self.cursor.execute('SELECT * FROM rates WHERE tox=? AND fromx=? AND retrieved_at=?', args)
        return self.cursor.fetchone()

    def get_rates(self, tox, fromx):
        """Gets all conversions from X to Y"""
        args = (tox, fromx)
        self.cursor.execute('SELECT * FROM rates WHERE tox=? AND fromx=?\
                             ORDER BY retrieved_at ASC', args)
        return self.cursor.fetchall()

    def store_rate(self, tox, fromx, when, rate):
        """Stores the conversion for later use"""
        args = (when, tox, fromx, rate)
        self.cursor.execute('INSERT INTO rates VALUES (?, ?, ?, ?)', args)
        self.connection.commit()
