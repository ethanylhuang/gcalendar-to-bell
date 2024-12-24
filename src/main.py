from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime, time

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CALENDAR_ID = 'c_e281ee0055e616856c4f83178cad4a88da4cd3e11bc8b5354efb1ea14f45617e@group.calendar.google.com'

credentials = service_account.Credentials.from_service_account_file(
    'service-account.json',
    scopes=SCOPES
)
service = build('calendar', 'v3', credentials=credentials)

calendar = service.calendars().get(calendarId=CALENDAR_ID).execute()
print(calendar['summary'])

today = datetime.combine(datetime.today(), time.min).isoformat() + 'Z'
events = service.events().list(
   calendarId=CALENDAR_ID,
   timeMin=today,
   singleEvents=True,
   orderBy='startTime'
).execute()

print("\nToday's events:")
for event in events['items']:
    print(event['summary'])
