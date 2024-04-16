import psycopg2

def create_table():
    conn = psycopg2.connect("dbname='database1' user='postgres' password