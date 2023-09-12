from functools import wraps
import sqlite3

from flask import redirect, render_template, request, session
from datetime import datetime


# Asks to login users without session 
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# Check password strength
def password_strength(password, username):
    # https://learn.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/password-must-meet-complexity-requirements
    
    # Check if username is in password
    if username.lower() in password.lower():
        return "Password should not include username."
    
    # Check if has uppercase letters
    if not (any(char.isupper() for char in password)):
        return "Password should include uppercase letters."
    
    # Check if has lowercase letters
    if not (any(char.islower() for char in password)):
        return "Password should include lowercase letters."
    
    # Check if has base digits
    if not (any(char.isdigit() for char in password)):
        return "Password should include digits."
    
    # Check if has special characters
    special_characters = ['~','!','@','#','$','%','^','&','*','_','-',
                          '+','=','`','|','\\','(',')','{','}','[',']',
                          ':',';','"',"'",'<','>',',','.','?','/']
    if not (any(char in special_characters for char in password)):
        return "Password should include special characters."
    
    # Check minimum length of 8 characters
    if len(password) < 8:
        return "Password should be longer than 8 characters."
    
    return True


def generate_file():

    event = {}
    # Request data from the form
    event["summary"] = request.form.get("summary")
    event["dtstart"] = request.form.get("dtstart")
    event["dtend"] = request.form.get("dtend")
    event["description"] = request.form.get("description")
    event["location"] = request.form.get("location")

    # Change time format
    event["dtstart"] = event["dtstart"].replace("-", "")
    event["dtstart"] = event["dtstart"].replace(":", "")
    event["dtstart"] = event["dtstart"] + "00Z"
    event["dtend"] = event["dtend"].replace("-", "")
    event["dtend"] = event["dtend"].replace(":", "")
    event["dtend"] = event["dtend"] + "00Z"


    # Create a ics file
    f = open("ics_output/event.ics", mode="w")

    # Beginning of the file
    f.write('BEGIN:VCALENDAR\n'
            'VERSION:2.0\n'
            'PRODID:Event-creator\n'
            'CALSCALE:GREGORIAN\n'
            'METHOD:PUBLISH\n'
            'BEGIN:VEVENT\n')
    
    #TODO insert data required for calendar to work
    f.write(f'SUMMARY:{event["summary"]}\n'
            f'DESCRIPTION:{event["description"]}\n'
            f'DTSTART:{event["dtstart"]}\n'
            f'DTEND:{event["dtend"]}\n'
            f'LOCATION:{event["location"]}\n')
    
    f.write('END:VEVENT\n'
            'END:VCALENDAR')

    # Close file
    f.close()

    return


def event_save_sql(session):

    event = event_collector()

    connection = sqlite3.connect("calendars.db", check_same_thread=False)
    cursor = connection.cursor()

    cursor.execute("""INSERT INTO events (username, summary, description, dtstart, dtend, location, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                   (str(session["username"]),
                    event["summary"],
                    event["description"],
                    str(event["dtstart"]),
                    str(event["dtend"]),
                    event["location"],
                    session["user_id"]))
    
    connection.commit()

    return


def event_collector():

    event = {}
    # Request data from the form
    event["summary"] = request.form.get("summary")
    event["dtstart"] = request.form.get("dtstart")
    event["dtend"] = request.form.get("dtend")
    event["description"] = request.form.get("description")
    event["location"] = request.form.get("location")

    # Change time format
    event["dtstart"] = event["dtstart"].replace("-", "")
    event["dtstart"] = event["dtstart"].replace(":", "")
    event["dtstart"] = event["dtstart"] + "00Z"
    event["dtend"] = event["dtend"].replace("-", "")
    event["dtend"] = event["dtend"].replace(":", "")
    event["dtend"] = event["dtend"] + "00Z"

    return event


def event_extractor(username):
# Extract data from sqlite3 database into a list

    connection = sqlite3.connect("calendars.db", check_same_thread=False)
    cursor = connection.cursor()

    cursor.execute("""SELECT id, summary, description, dtstart, dtend, location FROM events WHERE username = ?""", (username,))
    rows = cursor.fetchall()

    return rows

def format_time(date_time):
# Change time formate to dd/mm/yyyy
    time = date_time[9:11] + ':' + date_time[11:13]
    date = date_time[6:8] + '/' + date_time[4:6] + '/' + date_time[:4]
    time_date = time + ' ' + date
    return(time_date)
