
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3 


# Configure application
app = Flask(__name__)
app.debug = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure sqlite3 database
connection = sqlite3.connect("calendars.db")
cursor = connection.cursor()


# TODO: something about cashing. See if can function without it.
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
# @login_required
def index():
    # TODO: create form for the event
    return render_template("index.html")


@app.route("/login")
def login():
    # TODO: create a login page
    return render_template("login.html")


@app.route("/register")
def register():
    # TODO: create a register page
    return render_template("register.html")


@app.route("/history")
def history():
    # TODO: create history of events 
    # make a button to recreaet an old event
    return render_template("history.html")


@app.route("/settings")
def settings():
    # TODO: create settings with password change
    # and deleting the history of events
    return render_template("settings.html")


@app.route("/logout")
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

if __name__ == "__main__":
    app.run()