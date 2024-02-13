import psycopg2
import config
import textprint
import lass

DIRECTORY = 'prints/survey'

def connect(config):
    try:
        with psycopg2.connect(**config) as connection:
            print('Connected to the PostgreSQL database server.')
            return connection
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def create_table(connection, table_sql):
    try:
        cursor = connection.cursor()
        cursor.execute(table_sql)
        connection.commit()
        cursor.close()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def list_tables(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        tables = cursor.fetchall()
        cursor.close()
        return tables
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def drop_table(connection, table_name):
    try:
        cursor = connection.cursor()
        cursor.execute("DROP TABLE " + table_name)
        connection.commit()
        cursor.close()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def list_all_in_table(connection, table_name):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM " + table_name)
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def add_to_table(connection, table_name, username, text):
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO " + table_name + " (username, text) VALUES (%s, %s)", (username, text))
        connection.commit()
        cursor.close()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def formatted_table(connection, table_name):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM " + table_name)
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def formatted_print(connection, table_name):
    contents = list_all_in_table(connection, table_name)
    ret = ""
    for content in contents:
        ret += content[0] + "\n" + content[1] + "\n\n"
    return ret

if __name__ == '__main__':
    configurations = config.load_config()
    conn = connect(configurations)
    cursor = conn.cursor()
    # db_name = configurations['database']
    
    table_name = 'prints'
    table_sql = '''CREATE TABLE IF NOT EXISTS ''' + table_name + ''' (
        id SERIAL PRIMARY KEY,
        username TEXT NOT NULL,
        text VARCHAR(20000) NOT NULL
    )'''

    create_table(conn, table_sql)

    # files = textprint.all_files(DIRECTORY)
    # for file in files:
    #     paragraphs = lass.break_file_into_paragraphs(file)
    #     for paragraph in paragraphs:
    #         add_to_table(conn, table_name, lass.get_file_author(file), paragraph)

    print(formatted_print(conn, table_name))
    conn.commit()
    cursor.close()
    conn.close()