from config import Config
from datetime import datetime
import psycopg2
import psycopg2.extras


def open_database():
    try:
        connection_string = Config.DB_CONNECTION_STR
        connection = psycopg2.connect(connection_string)
        connection.autocommit = True
    except psycopg2.DatabaseError as exception:
        print(exception)
    return connection


def connection_handler(function):
    def wrapper(*args, **kwargs):
        connection = open_database()
        # we set the cursor_factory parameter to return with a dict cursor (cursor which provide dictionaries)
        dict_cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        ret_value = function(dict_cur, *args, **kwargs)
        dict_cur.close()
        connection.close()
        return ret_value
    return wrapper


@connection_handler
def register_user(cursor, user_name, password):
    cursor.execute("""SELECT username
                      FROM users;""")
    table = cursor.fetchall()
    existing_users = []
    for dictionary in table:
        existing_users.append(dictionary["username"])
    if user_name in existing_users:
        return False
    cursor.execute("""INSERT INTO users (username, password)
                      VALUES(%s, %s);""", (user_name, password))
    return True


@connection_handler
def get_user_id(cursor, user_name):
    cursor.execute("""SELECT id
                      FROM users
                      WHERE username = %s;""", (user_name,))
    new_user_id = cursor.fetchone()
    new_user_id = new_user_id['id']
    return new_user_id


@connection_handler
def get_user_by_name(cursor, username):
    cursor.execute("""SELECT username, password, id
                      FROM users
                      WHERE username = %s;""", (username,))
    return cursor.fetchone()


@connection_handler
def add_vote(cursor, planet_id, planet_name, user_id):
    cursor.execute("INSERT INTO planet_votes (planet_id, planet_name, user_id, submission_time) VALUES "
                   "(%s, %s, %s, %s);", (planet_id, planet_name, user_id, datetime.now().replace(microsecond=0)))
