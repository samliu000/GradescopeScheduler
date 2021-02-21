from __future__ import print_function
from datetime import datetime
import pickle
import os.path
import requests
from scheduler import login
from scheduler import get_courses
from scheduler import getAssignments
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']
gsID = None

print("hi")
# Access calendar
def access():
    creds = None

    # If authorization already occurred
    if os.path.exists('token.pkl'):
        with open('token.pkl', 'rb') as token:
            creds = pickle.load(token)

    #If not
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

        pickle.dump(creds, open("token.pkl", "wb"))
        creds = pickle.load(open("token.pkl", "rb"))

    # Calendar objecet
    service = build('calendar', 'v3', credentials=creds)
    r = requests.get('https://www.googleapis.com/calendar/v3/users/me/calendarList/calendarId')

    calendarExists = False
    page_token = None

    #loops through calendars in list
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()

        #Checks if calendar already exists, if not keep looping
        for calendar_list_entry in calendar_list['items']:
            if calendar_list_entry['summary'] == 'Gradescope Calendar': 
                calendarExists = True
                print('Calendar exists!')
                gsID = calendar_list_entry['id']
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break
    
    #If calendar doesn't exist, make one
    if calendarExists == False:
        gsCalendar = {
            'summary': 'Gradescope Calendar',
            'timeZone': 'America/Los_Angeles'
        }
        print('Calendar does not exist! New calendar created.')
        created_calendar = service.calendars().insert(body=gsCalendar).execute()
        gsID = created_calendar['id']
    
    print("daSession reached")
    # get list of assignment
    daSession = requests.Session()

    print("Enter your email: ")
    email = input()
    print(email)
    print("Enter your password: ")
    password = input()
    print(password)

    login(daSession, email,password)

    allCourseURLs = get_courses(daSession)
    
    allCourseAssignments = []
    for courseUrl in allCourseURLs:
      temp = getAssignments(courseUrl, daSession)
      allCourseAssignments.extend(temp)
    
    for hi in allCourseAssignments:
        if (hi == None) or (hi.dueDateTime == "") or (hi.title == ""):
            continue
        print(hi.title + "\n"  + hi.dueDateTime)
        processSingleAssignment(gsID, hi.title, hi.dueDateTime, service)

    

def parseDate(date):
    print("Parsing Date: " + date)
    #Splits string
    subStrs = date.split(" ", 2)
    months_dict = {
           'Jan' : '01',
           'Feb' : '02',
           'Mar' : '03',
           'Apr' : '04',
           'May' : '05',
           'Jun' : '06',
           'Jul' : '07',
           'Aug' : '08',
           'Sep' : '09',
           'Oct' : '10',
           'Nov' : '11',
           'Dec' : '12',
    }

    # Sets month and day -> convert with datetime
    month = months_dict.get(subStrs[0])
    day = subStrs[1]
    dT = "2021" + "-" + month + "-" + day
    
    return dT
       

def processSingleAssignment(id, title, date, service):

    # Parse date and set event
    dT = parseDate(date)
    event = {
        'summary': title,
        'start': {
            'date': dT,
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'date': dT,
            'timeZone': 'America/Los_Angeles',
        },
    }
    
    #insert event
    event = service.events().insert(calendarId=id, body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))

access()