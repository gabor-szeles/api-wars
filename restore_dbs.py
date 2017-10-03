import psycopg2
from config import Config


def main():
    connection = psycopg2.connect(Config.DB_CONNECTION_STR)
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(open("sql_data/create_tables.sql", "r").read())

if __name__ == "__main__":
    main()
