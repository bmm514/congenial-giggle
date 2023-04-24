import sqlite3

def create_db(database):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    return connection, cursor

class pokemonGOtracker:
    def __init__(self, database):
        self._connection = sqlite3.connect(database)
        self._cursor = self._connection.cursor()

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

def main():
    database = ':memory:'

    pokeGOtracker = pokemonGOtracker(database)

    pokeGOtracker.execute("""
        CREATE TABLE xp_tracker (
            name text,
            date text,
            xp INT
        )
        """
        )

    pokeGOtracker.execute("""INSERT INTO xp_tracker VALUES ('bmm', '2023-04-23', 10000)""")
    pokeGOtracker.execute("""INSERT INTO xp_tracker VALUES ('bmm', '2023-04-24', 20000)""")
    print('Added values')
    rows = pokeGOtracker.query("""SELECT * FROM xp_tracker WHERE name='bmm' ORDER BY date DESC""")
    print(rows)

if __name__ == '__main__':
    main()
