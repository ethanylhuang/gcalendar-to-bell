import re
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime
from constants import (
    PROJECT_ROOT,
    SCHOOL_YEAR_START,
    SCHOOL_YEAR_END,
    SERVICE_ACCOUNT_PATH,
    CALENDAR_ID,
)
from utils import print_schedule_events
from models import CalendarEvent

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def get_all_events():
    credentials = service_account.Credentials.from_service_account_file(
        str(SERVICE_ACCOUNT_PATH), scopes=SCOPES
    )
    service = build("calendar", "v3", credentials=credentials)

    start = SCHOOL_YEAR_START.isoformat() + "T00:00:00Z"
    end = SCHOOL_YEAR_END.isoformat() + "T23:59:59Z"

    events = (
        service.events()
        .list(
            calendarId=CALENDAR_ID,
            timeMin=start,
            timeMax=end,
            singleEvents=True,
            orderBy="startTime",
            maxResults=2500,
        )
        .execute()
    )

    return events


def extract_date(event):
    start_date = event["start"].get("dateTime", event["start"].get("date"))
    end_date = event["end"].get("dateTime", event["end"].get("date"))

    start_obj = datetime.strptime(
        start_date.split("T")[0] if "T" in start_date else start_date, "%Y-%m-%d"
    ).date()

    end_obj = datetime.strptime(
        end_date.split("T")[0] if "T" in end_date else end_date, "%Y-%m-%d"
    ).date()

    # If end date is same as start date, or if it's the next day (due to all-day event handling),
    # return single date
    if start_obj == end_obj or (end_obj - start_obj).days <= 1:
        return start_obj.strftime("%-m/%-d/%Y")
    else:
        return start_obj.strftime("%-m/%-d/%Y") + "-" + end_obj.strftime("%-m/%-d/%Y")


def create_schedule_event(letter, display_name=None):
    return CalendarEvent(
        display_name=display_name,
        schedule_type=f"schedule-{letter}",
    )


def filter_schedule_events(events):
    schedule_events = {}
    for event in events["items"]:
        parsed_event = parse_schedule_event(event)
        if parsed_event is not None:
            date = extract_date(event)
            schedule_events[date] = parsed_event
    return schedule_events


def parse_schedule_event(event: dict) -> CalendarEvent:
    text = event["summary"]
    formatted_text = text.lower()
    formatted_text = "".join(e for e in formatted_text if e.isalnum())

    # No School events
    if "noschool" in formatted_text:
        display_name = text.split("No School: ")[1]
        return CalendarEvent(
            display_name=display_name,
            schedule_type="holiday",
        )

    # Schedule letter events
    schedule_letter_pattern = re.compile(r"schedule([a-z])")
    match = schedule_letter_pattern.search(formatted_text)
    if match:
        letter = match.group(1)
        display_name = (
            text.split(": Schedule")[0].strip()
            if ": Schedule" in text
            else (
                text.split("Schedule ")[1].split(":")[1].strip()
                if "Schedule " in text and ":" in text
                else None
            )
        )
        return create_schedule_event(letter, display_name)

    # PSAT events
    if "psat" in formatted_text:
        return CalendarEvent(
            display_name="PSAT Testing",
            schedule_type="psat",
        )

    # Letter day events
    day_pattern = re.compile(r"^([a-z])day$")
    match = day_pattern.search(formatted_text)
    if match:
        return create_schedule_event(match.group(1))

    # Finals events
    finals_pattern = re.compile(r"finals([\d]+)")
    match = finals_pattern.search(formatted_text)
    if match:
        periods_str = re.sub(r"\s+", "", match.group(1))
        finals_map = {"167": "1", "25": "2", "34": "3"}
        day_num = finals_map.get(periods_str, "unknown")
        return CalendarEvent(
            display_name=f"Finals Day {day_num}",
            schedule_type=f"finals-day-{day_num}",
        )

    return None


def get_schedule_events():
    events = get_all_events()
    return filter_schedule_events(events)


if __name__ == "__main__":
    schedule_events = get_schedule_events()
    print_schedule_events(schedule_events)
