from flask import Flask, render_template, redirect, request, session, url_for, jsonify
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
        valid_login = data_handler.authenticate(username, password)
        if valid_login:
            return redirect(url_for('index'))
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


@app.route('/vote', methods=['POST'])
def vote_planet():
    planet_id = request.form["planetid"]
    planet_name = request.form["planetname"]
    user_id = request.form["userid"]
    database.add_vote(planet_id, planet_name, user_id)
    return ""


@app.route('/get_vote_stats')
def get_voting_statistics():
    stats = database.get_stats()
    return jsonify(stats=stats)


if __name__ == "__main__":
    app.secret_key = "you!never!guess!this"
    app.run(
        debug=True,  # Allow verbose error reports
        port=5000  # Set custom port
    )
