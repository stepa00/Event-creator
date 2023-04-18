
"""
Creates ics file with the event which parameters should be inserted
"""


# Create ics file
def generate_file():

    # Create a ics file
    f = open("event.ics", mode="w")

    # Beginning of the file
    f.write('BEGIN:VCALENDAR\n'
            'VERSION:2.0\n'
            'PRODID:-//ZContent.net//Zap Calendar 1.0//EN\n'
            'CALSCALE:GREGORIAN\n'
            'METHOD:PUBLISH\n'
            'BEGIN:VEVENT\n')
    
    #TODO insert data
    
    f.write('END:VEVENT\n'
            'END:VCALENDAR')

    # Close file
    f.close()

    return
        

# Generate ics file
generate_file()