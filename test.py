import lass as l
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def format_print(paragraphs):
    print("--------------------")
    for paragraph in paragraphs:
        print(paragraph)
        print("--------------------")

def main():
    # path = "survey/abeaubien_-_mundanely.txt"
    # paragraphs = l.break_file_into_paragraphs(path)
    # print(l.get_file_author(path))
    con = psycopg2.connect("user=test password='test'")
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = con.cursor()
    name_db = "test"
    sql = "CREATE DATABASE " + name_db
    cursor.execute(sql)
    

if __name__ == "__main__":
    main()