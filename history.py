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
        self.connection = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE rates
                          (retrieved_at DATE, fromx TEXT, tox TEXT, rate DOUBLE)''')
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

    def get_rate(self, fromx, tox, when):
        """Tries to get a currency rate conversion at a certain date"""
        args = (fromx.upper(), tox.upper(), when)
        self.cursor.execute('SELECT * FROM rates WHERE fromx=? AND tox=? AND retrieved_at=?', args)
        return self.cursor.fetchone()

    def get_rates(self, fromx, tox):
        """Gets all conversions from X to Y"""
        args = (fromx, tox)
        self.cursor.execute('SELECT * FROM rates WHERE fromx=? AND tox=?\
                             ORDER BY retrieved_at ASC', args)
        return self.cursor.fetchall()

    def set_rate(self, fromx, tox, when, rate):
        """Stores the conversion for later use"""
        args = (when, fromx.upper(), tox.upper(), rate)
        self.cursor.execute('INSERT INTO rates VALUES (?, ?, ?, ?)', args)
        self.connection.commit()

    def rate_exists(self, fromx, tox, when):
        """Checks if rate is already stored"""
        args = (fromx.upper(), tox.upper(), when)
        self.cursor.execute('SELECT * FROM rates WHERE fromx=? AND tox=? AND retrieved_at=?', args)
        result = self.cursor.fetchall()
        if not result:
            return False
        return True
