from config import Config
from datetime import datetime
import psycopg2
import psycopg2.extras
import os
import psycopg2
import urllib


def open_database():
    try:
        urllib.parse.uses_netloc.append('postgres')
        url = urllib.parse.urlparse(os.environ.get('DATABASE_URL'))
        connection = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
            )
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


@connection_handler
def get_stats(cursor):
    cursor.execute("""SELECT planet_name, COUNT(planet_name) AS votes
                      FROM planet_votes
                      GROUP BY planet_name
                      ORDER BY votes DESC""")
    stats = cursor.fetchall()
    return stats
