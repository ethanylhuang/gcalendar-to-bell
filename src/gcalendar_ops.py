from pprint import pprint
import re
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime, time
from project_root import PROJECT_ROOT
from calendar_ops import CalendarEvent

# Constants
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
CALENDAR_ID = "c_e281ee0055e616856c4f83178cad4a88da4cd3e11bc8b5354efb1ea14f45617e@group.calendar.google.com"
SCHOOL_YEAR_START = datetime(2024, 8, 12, 0, 0)
SCHOOL_YEAR_END = datetime(2025, 6, 6, 23, 59, 59)


def get_all_events():
    credentials = service_account.Credentials.from_service_account_file(
        str(PROJECT_ROOT / "src" / "service-account.json"), scopes=SCOPES
    )
    service = build("calendar", "v3", credentials=credentials)

    start = SCHOOL_YEAR_START.isoformat() + "Z"
    end = SCHOOL_YEAR_END.isoformat() + "Z"

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
    date = event["start"].get("dateTime", event["start"].get("date"))
    return date.split("T")[0] if "T" in date else date


def create_schedule_event(letter, display_name=None):
    if display_name is None:
        display_name = f"Schedule {letter.upper()}"
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
        display_name = text.split(":")[1].strip() if ":" in text else None
        return create_schedule_event(letter, display_name)

    # PSAT events
    if "psat" in formatted_text:
        return CalendarEvent(
            display_name="psat-testing",
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
            display_name=f"finals-day-{day_num}",
            schedule_type="finals",
        )

    return None


def get_schedule_events():
    events = get_all_events()
    return filter_schedule_events(events)


if __name__ == "__main__":
    from tabulate import tabulate

    schedule_events = get_schedule_events()

    # Convert dictionary to list of lists for tabulate
    table_data = [
        [date, event.schedule_type, event.display_name]
        for date, event in schedule_events.items()
    ]

    print("\nSchedule Events:")
    print(
        tabulate(
            table_data,
            headers=["Date", "Schedule Type", "Display Name"],
            tablefmt="grid",
        )
    )
