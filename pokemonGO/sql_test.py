import sqlite3

def create_db(database):
    connection = sqlite3.connect(database)

    return connection

def create_table(cursor, sql_query):
    cursor.execute(sql_query)

    return cursor

if __name__ == '__main__':
    database = 'test/bmm.db'
    connection = create_db(database)
    cursor = connection.cursor()
    sql_query = '''CREATE TABLE bmmpokemon(date text, xp INT)'''

    cursor = create_table(cursor, sql_query)

