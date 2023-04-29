import sqlite3 

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import password_strength, login_required, generate_file


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


@app.route("/", methods=["GET", "POST"])
def index():
    # Reached via GET
    if request.method == "GET":
        return render_template("index.html")
    # Reached via POST
    else:
        # Get form inputs
        event = {}
        event["summary"] = request.form.get("summary")
        event["dtstart"] = request.form.get("dtstart")
        event["dtend"] = request.form.get("dtend")
        event["description"] = request.form.get("description")
        print(event)
        generate_file(event)

        return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    error = None
    # TODO: create a login page
    # Reached via GET
    if request.method == "GET":
        return render_template("login.html")
    # Reached via POST
    else:
        # Get input from the form
        username = request.form.get("username")
        password = request.form.get("password")

        # Check if username entered
        if not username:
            error = "Enter username."
            return render_template("login.html", error=error)

        # Check if password entered
        if not password:
            error = "Enter password."
            return render_template("login.html", error=error)

        # Check user exists and password
        cursor.execute("""SELECT * FROM users WHERE username = ?""", (username,))
        row = cursor.fetchone()
        if not row:
            error = "Username or password is incorrect."
            return render_template("login.html", error=error)
        if not check_password_hash(row[2], password):
            error = "Username or password is incorrect."
            return render_template("login.html", error=error)
        
        # Remember which user has logged in
        session["user_id"] = row[0]

        return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
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

        # Check if username entered
        if not username:
            error = "Enter username."
            return render_template("register.html", error=error)
        
        # Check username existance in database
        cursor.execute("""SELECT * FROM users WHERE username = ?""", (username,))
        row = cursor.fetchone()
        if row:
            error = "Name already exists."
            return render_template("register.html", error=error)
        
        # Check if password was entered
        if not password:
            error = "Enter password."
            return render_template("register.html", error=error)

        # Check password strength
        check = password_strength(password, username)
        if check != True:
            # TODO: add discription
            error = check
            return render_template("register.html", error=error)
        
        # Check password conformation
        if password != confirm_password:
            error = "Passwords do not match."
            return render_template("register.html", error=error)


        # ---Success--- 
        # Hash the password and add to database
        hashed_password = generate_password_hash(password)
        cursor.execute("""INSERT INTO users (username, hash) VALUES (?, ?)""", (username, hashed_password))
        connection.commit()

        return redirect("/login")


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