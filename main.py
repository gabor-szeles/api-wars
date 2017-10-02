from flask import Flask, render_template, redirect, request, session, url_for
import requests

app = Flask(__name__)


@app.route("/")
def route_index():
    planets = requests.get("https://swapi.co/api/planets").json()
    planets = planets["results"]
    return render_template("planets.html", planets=planets)


if __name__ == "__main__":
    app.secret_key = "you!never!guess!this"
    app.run(
        debug=True,  # Allow verbose error reports
        port=5000  # Set custom port
    )
