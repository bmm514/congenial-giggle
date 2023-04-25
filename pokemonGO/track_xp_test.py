import sqlite3

def create_db(database):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    return connection, cursor

class pokemonGOtracker:
    def __init__(self, database, username):
        self._connection = sqlite3.connect(database)
        self._cursor = self._connection.cursor()
        self._username = username
        self._database = database

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    @property
    def connection(self):
        return self._connection

    @property
    def cursor(self):
        return self._cursor

    @property
    def username(self):
        return self._username

    @property
    def database(self):
        return self._database

    def commit(self):
        self.connection.commit()

    def close(self, commit = True):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql_command, params=None):
        self.cursor.execute(sql_command, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql_command, params = None, fetchall = True):
        self.cursor.execute(sql_command, params or ())
        if fetchall:
            return self.fetchall()
        else:
            return self.fetchone()

    def update_xp(self, xp, date, accept_all = False):
        """Add the XP on a date specified in isoformat (YYYY-MM-DD)"""
        #still need to add in xp_checker, probably use ORDER BY then select top result and compare
        replace_xp = 'n'
        if not accept_all:
            current_xp = self.query("""SELECT xp FROM xp_tracker WHERE date = :date""", 
                    {'date' : date}, 
                    fetchall = False)

            if current_xp is not None:
                replace_xp = input(f'Replace the current xp, {current_xp[0]}, on {date} with {xp}? y/n?') #To terminal
        else:
            replace_xp = 'y'

        if replace_xp == 'y':
            self.execute("""REPLACE INTO xp_tracker VALUES (:username, :date, :xp)""", 
                    {'username' : self.username, 'date' : date, 'xp' : xp})
        else:
            self.execute("""INSERT OR IGNORE INTO xp_tracker VALUES (:username, :date, :xp)""", 
                    {'username' : self.username, 'date' : date, 'xp' : xp})

def main():
    database = ':memory:'

    with pokemonGOtracker(database, 'bmm') as pokeGOtracker:

        pokeGOtracker.execute("""
            CREATE TABLE xp_tracker (
                username text,
                date text,
                xp INT
            )
            """
            )

        pokeGOtracker.execute("""
        CREATE UNIQUE INDEX xp_tracker_unique_username_date ON xp_tracker (username, date)
        """
        )

        pokeGOtracker.update_xp(10000, '2023-04-23',accept_all = False)
        pokeGOtracker.update_xp(20000, '2023-04-24',accept_all = False)
        pokeGOtracker.update_xp(25000, '2023-04-25',accept_all = False)
        pokeGOtracker.update_xp(45000, '2023-04-25', accept_all=True)
        rows = pokeGOtracker.query("""SELECT * FROM xp_tracker WHERE username='bmm' ORDER BY date DESC""")
        print(rows)

if __name__ == '__main__':
    main()
