# @parse.py: reads the files in 'data' and makes mapping of month -> array of dates
from __future__ import print_function
import csv
import sys
import json
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# CONSTANTS FOR EACH MONTH
AUGUST = "August(08)"
SEPTEMBER = "September(09)"
OCTOBER = "October(10)"
NOVEMBER = "November(11)"
DECEMBER = "December(12)"
JANUARY = "January(01)"

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar'

# AUTHORIZE CALENDAR API #
store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
	flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
	creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))

# START OF ACTUAL CODE #
monthsParsed = [] 			# Array for all the months
datesParsed = []  			# Array of arrays for all the dates
monthToDateDict = dict()	# Mapping from months to their dates

filepath = sys.argv[1]

with open(filepath,'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='"')

	for row in reader:
		# For the first row (months):
		if('(' in row[0]):
			monthsParsed = row
		# For the second row (dates):
		else:
			for dates in row:
				datesArray = dates.split(';')
				datesArrayConverted = []
				for currentDate in datesArray:
					#Convert date from MM/DD/YYYY to YYYY-MM-DD
					if(currentDate): # If string is not empty
						dateConverted = datetime.datetime.strptime(currentDate, '%m/%d/%y').strftime('%Y-%m-%d')
						datesArrayConverted.append(dateConverted)
				datesParsed.append(datesArrayConverted)

	# Map the months to the dates (mapping: month -> array of dates)
	numberOfMonths = len(monthsParsed)
	for i in range(0, numberOfMonths):
		monthToDateDict[monthsParsed[i]] = datesParsed[i]

	print(monthToDateDict[AUGUST])
	print(monthToDateDict[SEPTEMBER])
	print(monthToDateDict[OCTOBER])
	print(monthToDateDict[NOVEMBER])
	print(monthToDateDict[DECEMBER])
	print(monthToDateDict[JANUARY])

# EVENT FORMAT:
event = {
  'summary': 'BLACKOUT',
  'start': {
    'date': '2018-08-18',
    'timeZone': 'America/New_York',
  },
  'end': {
    'date': '2018-08-18',
    'timeZone': 'America/New_York',
  }
}

# Parse and create blackout unique identifier
csvname = filepath.split("/")[1]
name = csvname.split(".")[0]
event['summary'] = 'BLACKOUT' + "_" + name

# Array of all months to loop through
monthsArray = [AUGUST, SEPTEMBER, OCTOBER, NOVEMBER, DECEMBER, JANUARY]

# LOOP THROUGH EACH MONTH AND MAKE BLACKOUT DATES
for month in monthsArray:
	for date in monthToDateDict[month]:
		event['start']['date'] = date
		event['end']['date'] = date
		print(json.dumps(event, indent=4, sort_keys=True))
		service.events().insert(calendarId='24a6mvtqt64nilso3q06kq19bc@group.calendar.google.com', body=event).execute()
