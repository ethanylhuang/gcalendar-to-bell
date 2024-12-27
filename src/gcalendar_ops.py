import re
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime, time
from project_root import PROJECT_ROOT


def get_all_events():
    SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
    CALENDAR_ID = "c_e281ee0055e616856c4f83178cad4a88da4cd3e11bc8b5354efb1ea14f45617e@group.calendar.google.com"

    credentials = service_account.Credentials.from_service_account_file(
        str(PROJECT_ROOT / "src" / "service-account.json"), scopes=SCOPES
    )
    service = build("calendar", "v3", credentials=credentials)

    calendar = service.calendars().get(calendarId=CALENDAR_ID).execute()
    # print(calendar["summary"])

    today = datetime.combine(datetime.today(), time.min).isoformat() + "Z"
    start = datetime(2024, 8, 12, 0, 0).isoformat() + "Z"
    end = datetime(2025, 6, 6, 23, 59, 59).isoformat() + "Z"

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


def filter_schedule_events(events):
    schedule_events = []
    for event in events["items"]:
        event_name = event["summary"]
        if event_name:
            event["summary"] = parse_schedule_string(event_name)
            if event["summary"] != None:
                schedule_events.append(event)
    return schedule_events


def parse_schedule_string(text: str) -> str | None:
    no_school_pattern = re.compile(r"(?i)\bno\s+school\b")
    if no_school_pattern.search(text):
        return "no-school"

    schedule_letter_pattern = re.compile(r"(?i)\bschedule\s+([A-Za-z])\b")
    match = schedule_letter_pattern.search(text)
    if match:
        letter = match.group(1).lower()
        return f"schedule-{letter}"

    day_pattern = re.compile(r"(?i)\b([A-Za-z])\s+day\b")
    match = day_pattern.search(text)
    if match:
        letter = match.group(1).lower()
        return f"schedule-{letter}"

    finals_pattern = re.compile(r"(?i)\bfinals:\s*([\d,\s]+)\b")
    match = finals_pattern.search(text)
    if match:
        periods_str = match.group(1)
        periods_str = re.sub(r"\s+", "", periods_str)

        if periods_str == "1,6,7":
            return "finals-day-1"
        elif periods_str == "2,5":
            return "finals-day-2"
        elif periods_str == "3,4":
            return "finals-day-3"
        else:
            return "finals-day-unknown"

    return None


def get_schedule_events():
    events = get_all_events()
    schedule_events = filter_schedule_events(events)
    return schedule_events


if __name__ == "__main__":
    schedule_events = get_schedule_events()
    print("\nSchedule-related events:")
    for event in schedule_events:
        date_str = (
            event["start"].get("dateTime", event["start"].get("date", "")).split("T")[0]
        )
        print(f"{event['summary']} {date_str}")
