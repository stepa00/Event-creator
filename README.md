# Event-Creator

#### Video Demo: https://youtu.be/iHxsu18Xil4

#### Description:

"Event-Creator" is a web based application. It creates files in .ics format. Each created file contains an event that is compatible with all mainstream calendars like Outlook and iCalendar.

**Project targets** that me as an author tried to achieve:

1. Complete final project for CS50 Introduction to computer science course;
2. Create a project outside CS50 frameworks, packages and helpful functions;
3. Use my own Mac for production;
4. Familiarize myself with github and use it during the project;
5. Use on of the Google's APIs;
6. Create my own visual design for the website;
7. Use only functions created by me and import as little as possible.

**Files required for the application**:

1. app.py - main file of the application;
2. helper.py - file containing all functions created by author;
3. calendars.db - sqlite3 data base that includes two tables;
4. /static/styles.css - visual styling of the website created by author;
5. /templates - folder with 6 html files;
6. .gitignore - to prevent upload of all the files to the github;
7. README.md

**Framework** required for project to run:

1. Flask;
2. Python 3;
3. HTML;
4. CSS;
5. JavaScript;
6. Sqlite3;
7. Google Autocomplete API (not necessary)

**app.py** inherits its organization form previous assignments of cs50 course.
First, Flask is configured and session added to store data of the user.
Second, connection between sqlite3 database and application is created. It is stated that you should close the connection after but I have not find any problems with it and did not implement closer of the connection.
Next go different routes of the application for pages with GET and POST methods. Some routes only have POST methods when there are multiple actions available on one webpage. Almost all routes are secured with password except for 'login', 'register' and 'index'.

**helpers.py** consists of functions written by author, this file than imported into the main app.py.
'login_required' function taken from the course to prevent users from entering places without logging in.
'password_strength' based on recommendations from Microsoft on password security. Function checks for criteria and alerts user from using simple passwords and stops from creating accounts with low security.
'generate_file' create an ics file that is downloaded from the browser. Inside it simply concatenates strings and user inputs to form a file according to the standard RFC 5545.
'event_save_sql' saves event to the database, so user can see it later in history page.
'event_collector' function that collects user input form html forms. Function used in other functions as data supplier. Also, it changes time and date format, so it will not conflict with sqlite3 database, because it does not like symbols like '-', ':'.
'event_extractor' function gets data from database based on user. Only events created by user are extracted. There is an option to change username but function will still correctly collect all the data, as it is based on user's id.
'format_time' using string slices makes date and time look nice without using imported methods. Initial format is UTC yyyymmddThhmmssZ and function changes it to hh:mm dd/mm/yyyy.

**html templates** here I am using Jinja, JavaScript and CSS.
The main file is 'layout.html'. There is a place for the Google api for Autocomplete api. It is required for Location feature, where Google can complete the address of the event for you. Also, in the same file navigation bar is configured with a link to the author's github with the progress of this project (it took me a lot of time due to procrastination).
In 'index.html' there are two option of the page, for logged in and not logged in users. They are separated with Jinja and session attribute. Also, there is a script adopted from google's education website, for the api to properly function and constantly update based on user's input on the keyboard without reloading the webpage (pretty cool).
'login.html' page where user logs in and gets errors if he/she fails to provide a valid username or password.
'register.html' page where user registers on the web app. Passwords are hashed for the security.
'history.html' page with all the events created by user. Displayed events are only that current user has created.
'setting.html' allow user to change his/her password and username. Also, it allows user to completely delete his/her profile from the application, as well as, all the events that were created by this user.

**styles.ss** I wanted to create my own style of the web app using only standard css properties, so I can become better at it and to make the website look minimalist. 

**sqlite3 database calendars.db** includes two tables: users and events.
'users' has 'id', 'username' and 'hash'. 'id' is the main identifier on the website. 'username' is mainly for logging in for users and 'hash' is a hashed password.
'events' has:

- 'id' - personal id of the event, it is required by standard and would be useful for future developent;
- 'username' - useful for future development if invites are add to the form;
- 'summary' - name of the event; 
- 'description' - description of the event, not standardized area;
- 'dtstart', 'dtend' - start and finish time of the event, names according to the standard;
- 'location' - place of the event, can be filed with any information and does not required google api functioning;
- 'user_id' - needed to locate all the events created by user, if he will change his name in the settings in the process.

#### Basic structure fo ics file

1. BEGIN:VCALENDAR - This line marks the beginning of the iCalendar file.
2. VERSION:2.0 - This line specifies the version of iCalendar being used.
3. PRODID:identifier - This line identifies the software or application that generated the iCalendar file.
4. BEGIN:VEVENT - This line marks the beginning of a calendar event.
5. DTSTART:yyyy-mm-ddThh:mm:ss - This line specifies the start date and time of the event in ISO 8601 format.
6. DTEND:yyyy-mm-ddThh:mm:ss - This line specifies the end date and time of the event in ISO 8601 format.
7. SUMMARY:event summary - This line specifies a brief summary or title of the event.
8. DESCRIPTION:event description - This line provides a more detailed description of the event.
9. LOCATION:event location - This line specifies the location where the event will take place.
10. END:VEVENT - This line marks the end of the calendar event.
11. END:VCALENDAR - This line marks the end of the iCalendar file.
