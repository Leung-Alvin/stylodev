import psycopg2
import config

def connect(config):
    try:
        with psycopg2.connect(**config) as connection:
            print('Connected to the PostgreSQL database server.')
            return connection
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


if __name__ == '__main__':
    configurations = config.load_config()
    conn = connect(configurations)
    cursor = conn.cursor()
    db_name = configurations['database']
    table_sql = '''CREATE TABLE IF NOT EXISTS ''' + db_name + ''' (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        price REAL NOT NULL
    )'''
    postgres_insert_query = ''' INSERT INTO ''' + db_name + ''' (publisher_id,
    publisher_name, publisher_estd, publsiher_location, publsiher_type)
    VALUES (%s,%s,%s,%s,%s)'''
    record_to_insert = [(1, 'Packt', 1950,
                        'chennai', 'books'),
                        (22, 'Springer', 1950,
                        'chennai', 'books'),
                        (23, 'Springer', 1950,
                        'chennai', 'articles'),
                        (54, 'Oxford', 1950,
                        'chennai', 'all'),
                        (52, 'MIT', 1950,
                        'chennai', 'books'),
                        (10, 'RCT', 1992,
                        'Mumbai', 'all'),
                        (6, 'ICT', 1995,
                        'Delhi', 'article'),
                        (7, 'PICT', 1955,
                        'Pune', 'article')
                        ]
    for i in record_to_insert:
        cursor.execute(postgres_insert_query, i)
        conn.commit()
        count = cursor.rowcount
    print(count, "Record inserted successfully \
    into publisher table")
    cursor.execute(table_sql)
    conn.commit()
    cursor.close()
    conn.close()