from flask import Flask, render_template, redirect, request, session, url_for
import requests
import json
import database
import data_handler



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


@app.route('/login', methods=['GET', 'POST'])
def login():
    valid_login = True
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = database.get_user_by_name(username)
        if user:
            valid_password = data_handler.check_password(password, user['password'])
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
        hashed_password = data_handler.get_hashed_password(password)
        new_user = database.register_user(user_name, hashed_password)
        if new_user:
            session['username'] = user_name
            session['user_id'] = database.get_user_id(user_name)
            return redirect("/")
    return render_template("registration.html", new_user=new_user)


if __name__ == "__main__":
    app.secret_key = "you!never!guess!this"
    app.run(
        debug=True,  # Allow verbose error reports
        port=5000  # Set custom port
    )
