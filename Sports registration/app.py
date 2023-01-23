# Implements a registration form, storing registrants in a SQLite database, with support for deregistration

from tokenize import Name
from cs50 import SQL
from flask import Flask, redirect, render_template, request
from datetime import date

app = Flask(__name__)

db = SQL("sqlite:///data/froshims.db")

SPORTS = [
    "Basketball",
    "Soccer",
    "Ultimate Frisbee"
]


@app.route("/")
def index():
    return render_template("index.html", sports=SPORTS)


@app.route("/deregister", methods=["POST"])
def deregister():
    
    # Forget registrant
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM registrants WHERE id = ?", id)
    return redirect("/registrants")


@app.route("/register", methods=["POST"])
def register():

    # Validate submission
    name = request.form.get("name")
    sport = request.form.get("sport")
    dob = request.form.get("dob")
    now = date.today().year
    birthyear = int(dob[:4])
    age = now - birthyear
    if not name or not dob or sport not in SPORTS:
        return render_template("failure.html")

    # Remember registrant
    db.execute("INSERT INTO registrants (name, sport, dob, age) VALUES(?, ?, ?, ?)", name, sport, dob, age)

    # Confirm registration
    return redirect("/registrants")


@app.route("/registrants")
def registrants():
    registrants = db.execute("SELECT * FROM registrants")
    return render_template("registrants.html", registrants=registrants)

if __name__ == "__main__" :
    app.run()
