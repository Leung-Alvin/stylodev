import psycopg2
import config
import textprint
import lass

DIRECTORY = 'prints/survey'
FIELDS_FILE = 'table_fields.txt'

def connect(config):
    try:
        with psycopg2.connect(**config) as connection:
            print('Connected to the PostgreSQL database server.')
            return connection
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def create_table(connection, table_name, file):
    fields = get_table_header(file)
    command = '''CREATE TABLE IF NOT EXISTS ''' + table_name + ''' (\n''' + fields + '''\t)'''
    try:
        cursor = connection.cursor()
        cursor.execute(command)
        connection.commit()
        print("Created table " + table_name)
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
        print("Dropped table " + table_name)
        cursor.close()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def select_all_in_table(connection, table_name):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM " + table_name)
        rows = cursor.fetchall()
        cursor.close()
        print("Selected ALL " + str(cursor.rowcount) + " rows")
        return rows
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

# def add_to_table(connection, table_name, username, text, word_count):
#     parameters = " (" + ', '.join(get_parameters('table_fields.txt')) + ") VALUES (" + ', '.join(['%s' for i in range(len(get_parameters('table_fields.txt')))]) + ")"
#     try:
#         cursor = connection.cursor()
#         cursor.execute("INSERT INTO " + table_name + parameters, (username, text, word_count, 0))
#         connection.commit()
#         cursor.close()
#         return cursor.rowcount
#     except (psycopg2.DatabaseError, Exception) as error:
#         print(error)

def add_to_table(connection, table_name, input_params):
    parameters = " (" + ', '.join(get_parameters('table_fields.txt')) + ") VALUES (" + ', '.join(['%s' for i in range(len(get_parameters('table_fields.txt')))]) + ")"
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO " + table_name + parameters, input_params)
        connection.commit()
        cursor.close()
        return cursor.rowcount
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def formatted_print(connection, table_name):
    contents = select_all_in_table(connection, table_name)
    ret = ""
    for content in contents:
        ret += str(content[2]) + "\nBy: " + str(content[1]) + "\n\n"
    return ret

def select_from_table(connection, table_name, column, value):
    try:
        cursor = connection.cursor()
        # cursor.execute("SELECT * FROM " + table_name + " WHERE " + column + " ILIKE %s", (value,))
        cursor.execute("SELECT * FROM " + table_name + " WHERE " + column + " ILIKE "+ "'%" + value + "%'")
        rows = cursor.fetchall()
        cursor.close()
        print("Selected " + str(cursor.rowcount) + " rows")
        return rows
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def delete_from_table(connection, table_name, column, value):
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM " + table_name + " WHERE " + column + " = %s", (value,))
        connection.commit()
        print("Deleted " + str(cursor.rowcount) + " rows")
        cursor.close()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def load_directory(conn, directory):
    files = textprint.all_files(directory)
    count = 0
    for file in files:
        paragraphs = lass.break_file_into_paragraphs(file)
        for paragraph in paragraphs:
            count += add_to_table(conn, table_name, (lass.get_file_author(file), paragraph, len(paragraph.split()),0))
    print("Added " + str(count) + " rows")

def formatted_rows(rows):
    ret = ""
    for row in rows:
        ret += str(row[2]) + "\nBy: " + str(row[1]) + " " + str(row[3]) + "\n\n"
    return ret

def get_table_header(file):
    columns = []
    lines = []
    with open(file, 'r') as f:
        lines = f.readlines()
    for line in lines:
        string = '\t'+str(line.replace('\n',''))+',\n'
        columns.append(string)
        # columns.append(line)
        # columns.append(',\n')
    ret = ''.join(columns)
    ret = ret[:-2]
    return ret
    # with open(file, 'r') as f:
    #     columns = f.readlines()
    #     return ',\n'.join(columns)

def get_parameters(file):
    columns = []
    lines = []
    with open(file, 'r') as f:
        lines = f.readlines()
    for line in lines:
        if line.__contains__('SERIAL') or line.__contains__('PRIMARY KEY'):
            continue
        else:
            columns.append(line.split()[0])
    return columns

def initialize_sample_table(connection, table_name, file, directory):
    create_table(connection, table_name, file)
    if select_all_in_table(connection, table_name) == []:
        load_directory(connection, directory)
    else:
        print("Table already has data")

if __name__ == '__main__':
    configurations = config.load_config()
    conn = connect(configurations)
    cursor = conn.cursor()
    # db_name = configurations['database']
    
    table_name = 'prints'
    # table_sql = '''CREATE TABLE IF NOT EXISTS ''' + table_name + ''' (
    #     id SERIAL PRIMARY KEY,
    #     username TEXT NOT NULL,
    #     text VARCHAR(20000) NOT NULL,
    #     word_count INT, 
    #     )'''
    # print(" (username, text, word_count) VALUES (%s, %s, %s)")

    # rad = " (" + ', '.join(get_parameters('table_fields.txt')) + ") VALUES (" + ', '.join(['%s' for i in range(len(get_parameters('table_fields.txt')))]) + ")"
    # print(rad)


    # rad = get_table_header('table_fields.txt')
    # part = '''CREATE TABLE IF NOT EXISTS ''' + table_name + ''' (\n''' + get_table_header('table_fields.txt') + '''\t)'''
    # print(rad)
    # print(part)
    # print('---')
    # print(repr(table_sql))
    # print('---')
    # print(part==table_sql)

    initialize_sample_table(conn, table_name, FIELDS_FILE, DIRECTORY)
    # select_all_in_table(conn, table_name)
    # drop_table(conn, table_name)
    
    # create_table(conn, table_name, FIELDS)


    # load_directory(conn, DIRECTORY)

    # print(formatted_print(conn, table_name))

    works = select_from_table(conn, table_name, 'username', 'ale')

    # delete_from_table(conn, table_name, 'username', 'aleung')
    
    print(formatted_rows(works))

    # print(select_all_in_table(conn, table_name)[3])

    # drop_table(conn, table_name)

    conn.commit()
    cursor.close()
    conn.close()