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

    def query(self, sql_command, params = None):
        self.cursor.execute(sql_command, params or ())
        return self.fetchall()

    def update_xp(self, xp, date, accept_all = False):
        """Add the CP on a date specified in isoformat (YYYY-MM-DD)"""
        self.execute("""INSERT INTO xp_tracker VALUES (:name, :date, :date)""", 
                {'database' : self.database, 'name' : self.username, 'date' : date, 'xp' : xp})
        pass

def main():
    database = ':memory:'

    with pokemonGOtracker(database, 'bmm') as pokeGOtracker:

        pokeGOtracker.execute("""
            CREATE TABLE xp_tracker (
                name text,
                date text,
                xp INT
            )
            """
            )

        pokeGOtracker.update_xp(10000, '2023-04-23')
        pokeGOtracker.update_xp(20000, '2023-04-24')
        pokeGOtracker.update_xp(25000, '2023-04-25')
        print('Added values')
        rows = pokeGOtracker.query("""SELECT * FROM xp_tracker WHERE name='bmm' ORDER BY date DESC""")
        print(rows)

if __name__ == '__main__':
    main()
