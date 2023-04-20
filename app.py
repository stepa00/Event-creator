import sqlite3 

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import password_strength


# Configure application
app = Flask(__name__)
app.debug = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure sqlite3 database
connection = sqlite3.connect("calendars.db", check_same_thread=False)
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


@app.route("/register", methods=["GET", "POST"])
def register():
    # Reached via GET
    if request.method == "GET":
        return render_template("register.html")
    
    # Reached via POST
    else:
        # TODO: create a register page
        # Get the password from the form
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Check submited username
        if not username:
            # TODO: alert username wasn't submited
            return render_template("register.html"), print("alert username wasn't submited")
        
        # Check username existance in database
        cursor.execute("""SELECT * FROM users WHERE username = ?""", (username,))
        rows = cursor.fetchall()
        if rows:
            # TODO: alert username already exists
            return render_template("register.html"), print("alert: username already exists")

        # Check password strength
        if not password_strength(password):
            # TODO: alert: password should include ...
            return render_template("register.html"), print("alert: password is not strong")

        # Check password conformation
        if password != confirm_password:
            # TODO: alert: password wasn't confirmed
            return render_template("register.html"), print("alert: password wasn't confirmed")

        # Hash the password and add to database
        hashed_password = generate_password_hash(password)
        cursor.execute("""INSERT INTO users (username, hash) VALUES (?, ?)""", (username, hashed_password))
        connection.commit()

        # Insert password into database
        # TODO: go to login page
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