import sqlite3 

from flask import Flask, flash, redirect, render_template, request, session, send_file
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import password_strength, login_required, generate_file, event_save_sql, event_extractor, format_time


# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure sqlite3 database
connection = sqlite3.connect("calendars.db", check_same_thread=False)
cursor = connection.cursor()


@app.route("/", methods=["GET", "POST"])
def index():
    # Reached via GET
    if request.method == "GET":
        return render_template("index.html")
    # Reached via POST
    else:
        if session["username"]:
            event_save_sql(session)
        generate_file()
        return send_file("ics_output/event.ics", as_attachment=True)


@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any username
    session.clear()

    error = None
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
        session["username"] = row[1]
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
        
        # Check username existence in database
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


@app.route("/history", methods=["GET", "POST"])
@login_required
def history():

    # Change time format for output
    rows = event_extractor(session["username"])
    history = []
    for row in rows:
        history.append(list(row))
    for event in history:
        event[3] = format_time(event[3])
        event[4] = format_time(event[4])
    return render_template("history.html", rows = history)
        

@app.route("/settings")
@login_required
def settings():
    # TODO: create settings with password change
    # and deleting the history of events
    return render_template("settings.html")


@app.route("/change_password", methods=["POST"])
@login_required
def change_password():
    # Change password:
    # Get input from form
    old_password = request.form.get("old_password")
    new_password = request.form.get("new_password")
    conf_new_password = request.form.get("conf_new_password")

    # Check if old and new passwords entered
    if not old_password or not new_password:
        error = "Enter Old and New passwords."
        return render_template ("settings.html", error=error)
    
    # Check conformation password
    if new_password != conf_new_password:
        error = "Passwords do not match."
        return render_template("settings.html", error=error)
    
    # Check if old password is correct;
    cursor.execute("""SELECT * FROM users WHERE username = ?""", (session["username"],))
    row = cursor.fetchone()

    if not check_password_hash(row[2], old_password):
        error = "Username or password is incorrect."
        return render_template("settings.html", error=error)

    # Check if new password is strong;
    check = password_strength(new_password, row[2])
    if check != True:
        error = check
        return render_template("register.html", error=error)

    # Hash password
    hashed_new_password = generate_password_hash(new_password)


    # Change old password for new.
    cursor.execute("""UPDATE users SET hash = ? WHERE id = ?""", (hashed_new_password, session["user_id"]))

    return render_template("settings.html")


@app.route("/change_username", methods=["POST"])
@login_required
def change_username():
    # Get input from form
    new_username = request.form.get("new_username")

    # Check for the same usernames
    cursor.execute("""SELECT * FROM users WHERE username = ?""", (new_username,))
    row = cursor.fetchone()
    if row != None:
        error = "Username already exists."
        return render_template("settings.html", error=error)
    
    # Change username
    cursor.execute("""UPDATE users SET username = ? WHERE id = ?""", (new_username, session["user_id"]))
    connection.commit()

    return render_template("settings.html")


@app.route("/delete_account", methods=["POST"])
def delete_account():
    # Delete history
    cursor.execute("""DELETE FROM events WHERE user_id = ?""", (session["user_id"],))
    connection.commit()

    # Delete account
    cursor.execute("""DELETE FROM users WHERE id = ?""", (session["user_id"],))
    connection.commit()

    session.clear()

    return render_template("login.html")


@app.route("/logout")
def logout():

    # Forget any username
    session.clear()

    # Redirect user to login form
    return redirect("/")


if __name__ == "__main__":
    app.run()
