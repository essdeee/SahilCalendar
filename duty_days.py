from __future__ import print_function
import csv
import sys
import json
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar'

# AUTHORIZE CALENDAR API #
store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
	flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
	creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))

# Lists all events for given calendar ID
page_token = None
while True:
  events = service.events().list(calendarId='24a6mvtqt64nilso3q06kq19bc@group.calendar.google.com', pageToken=page_token).execute()
  for event in events['items']:
    print(event['summary'])
    print(event['end']['date'])
  page_token = events.get('nextPageToken')
  if not page_token:
    break