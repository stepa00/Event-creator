# Event-creator

Web based application espoused to create events for MacOS calendar

## Project target

Create web based application that will allow user to create and download event files in format of `.ics`.

## Project framework

- Flask
- Python 3
- HTML
- CSS
- Bootstrap

## Road map

1. Python program generating ics.
2. Python server development.
3. Website design with bootstrap
4. HTML and CSS based web design
5. Connection of server and HTML forms
6. Testing

## Basic structure fo ics file

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

## TODO

1. Display history of events;
   - Page;
   - Sqlite extraction;
2. Make a delete option for event;
   - how to get id of an event in the line with button of delete?
   - NO SUCH feature;

3. WORK ON setttings menu;
   - create a page;
   - create buttons;
   - allow to change password;
   - delete account;
   - change name;

4. Make a nice looking site.
