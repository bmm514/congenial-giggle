import sqlite3

def create_db(database):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    return connection, cursor

def create_table(cursor, sql_command):
    cursor.execute(sql_command)

def insert_xp(name, date, xp, connection, cursor):
    with connection:
        cursor.execute("""INSERT INTO xp_tracker VALUES (:name, :date, :xp)""",
                {'name' : name, 'date' : date, 'xp' : xp})

def main():
    database = ':memory:'
    connection, cursor = create_db(database)
    create_query = '''CREATE TABLE xp_tracker(
        name text, 
        date text, 
        xp INT
        )'''

    try:
        create_table(cursor, create_query)
    except sqlite3.OperationalError:
        print('Table already created, continue...')

    insert_xp('bmm', "2023-04-24", 10000, connection, cursor)
#    insert_query = '''INSERT INTO xp_tracker 
#        VALUES ("bmm", "2023-04-24", 10000)
#        '''
#    cursor = run_sql(cursor, insert_query)
#
#    insert_query = '''INSERT INTO xp_tracker 
#        VALUES ("r", "2023-04-24", 100000)
#        '''
#    cursor = run_sql(cursor, insert_query)
#
    select_query = """SELECT * FROM xp_tracker WHERE date='2023-04-24'"""
#
    cursor.execute(select_query)
#
    print(cursor.fetchall())
#
#    connection.commit()
    connection.close()

if __name__ == '__main__':
    main()
