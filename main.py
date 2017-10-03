from flask import Flask, render_template, redirect, request, session, url_for
import requests
import json
import psycopg2
import psycopg2.extras
import bcrypt

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    planets = requests.get("https://swapi.co/api/planets").json()
    if request.method == "POST":
        new_page = request.form["next_page"]
        planets = requests.get(new_page).json()
    next_page = planets["next"]
    prev_page = planets["previous"]
    planets = planets["results"]
    return render_template("planets.html", planets=planets, next_page=next_page, prev_page=prev_page)


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    valid_login = True
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get_user_by_name(username)
        if user:
            valid_password = check_password(password, user['password'])
            if valid_password:
                session['username'] = username
                session['user_id'] = user['id']
                return redirect(url_for('index'))
            if not valid_password:
                valid_login = False
        if not user:
            valid_login = False
    return render_template("login.html", valid_login=valid_login)


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('index'))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    new_user = True
    if request.method == 'POST':
        user_name = request.form.get("user_name")
        password = request.form.get("password")
        hashed_password = get_hashed_password(password)
        new_user = register_user(user_name, hashed_password)
        if new_user:
            session['username'] = user_name
            session['user_id'] = get_user_id(user_name)
            return redirect("/")
    return render_template("registration.html", new_user=new_user)


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


def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode("utf-8")


def check_password(plain_text_password, hashed_text_password):
    hashed_bytes_password = hashed_text_password.encode("utf-8")
    # Check hased password. Useing bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


@connection_handler
def get_user_id(cursor, user_name):
    cursor.execute("""SELECT id
                      FROM users
                      WHERE username = %s;""", (user_name,))
    new_user_id = cursor.fetchone()
    new_user_id = new_user_id['id']
    return new_user_id


if __name__ == "__main__":
    app.secret_key = "you!never!guess!this"
    app.run(
        debug=True,  # Allow verbose error reports
        port=5000  # Set custom port
    )
