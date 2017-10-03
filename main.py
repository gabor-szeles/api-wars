from flask import Flask, render_template, redirect, request, session, url_for
import requests
import json

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def route_index():
    planets = requests.get("https://swapi.co/api/planets").json()
    if request.method == "POST":
        new_page = request.form["next_page"]
        planets = requests.get(new_page).json()
    next_page = planets["next"]
    prev_page = planets["previous"]
    planets = planets["results"]
    return render_template("planets.html", planets=planets, next_page=next_page, prev_page=prev_page)


if __name__ == "__main__":
    app.secret_key = "you!never!guess!this"
    app.run(
        debug=True,  # Allow verbose error reports
        port=5000  # Set custom port
    )
