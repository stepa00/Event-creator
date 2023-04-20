
"""
Creates ics file with the event which parameters should be inserted
"""
# Constant
event = {}
event['dtstart'] = '20080212'
event['dtend'] = '20080213'
event['dtstamp'] = '20150421T141403'

# Create ics file
def generate_file(event):

    # Create a ics file
    f = open("event.ics", mode="w")

    # Beginning of the file
    f.write('BEGIN:VCALENDAR\n'
            'VERSION:2.0\n'
            'PRODID:Event-creator\n'
            'CALSCALE:GREGORIAN\n'
            'METHOD:PUBLISH\n'
            'BEGIN:VEVENT\n')
    
    #TODO insert data required for calendar to work
    f.write(f'DTSTART:{event["dtstart"]}\n'
            f'DTEND:{event["dtend"]}\n'
            f'DTSTAMP:{event["dtstamp"]}\n')
    
    f.write('END:VEVENT\n'
            'END:VCALENDAR')

    # Close file
    f.close()

    return
        

# Generate ics file
generate_file(event)