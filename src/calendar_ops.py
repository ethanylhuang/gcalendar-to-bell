from gcalendar_ops import get_schedule_events
from constants import SCHOOL_YEAR_START, SCHOOL_YEAR_END, REMOTE_SCHEDULE_PATH
from datetime import date, datetime
from models import CalendarEvent
from pathlib import Path
from utils import print_schedule_events


def load_local():
    return get_schedule_events()


def load_remote(path: Path):
    return deserialize_bell(path)


# returns schedule_type, display_name if "#" in event_str
def parse_event_str(event_str: str) -> CalendarEvent:
    if "#" in event_str:
        schedule_type, display_name = event_str.split("#", 1)
        return CalendarEvent(
            schedule_type=schedule_type.strip(), display_name=display_name.strip()
        )
    else:
        return CalendarEvent(schedule_type=event_str.strip(), display_name=None)


# load from .bell
def deserialize_bell(file_path: Path) -> dict[date, CalendarEvent]:
    schedule_events = {}
    with open(file_path) as file:
        for line in file:
            date_range = False
            try:
                date_str, event = line.strip().split(" ", 1)
                if "-" in date_str:
                    date_range = True
            except ValueError:
                continue

            if date_range:
                date_start = date_str.split("-")[0]
                date_end = date_str.split("-")[1]
                try:
                    date_start = datetime.strptime(date_start, "%m/%d/%Y").date()
                    date_end = datetime.strptime(date_end, "%m/%d/%Y").date()
                except ValueError:
                    continue
                date = (
                    date_start.strftime("%-m/%-d/%Y")
                    + "-"
                    + date_end.strftime("%-m/%-d/%Y")
                )

                if date_start >= SCHOOL_YEAR_START and date_end <= SCHOOL_YEAR_END:
                    event = parse_event_str(event)
                    schedule_events[date] = event

            # Not a date range
            else:
                try:
                    date = datetime.strptime(date_str, "%m/%d/%Y").date()
                except ValueError:
                    continue
                if date >= SCHOOL_YEAR_START and date <= SCHOOL_YEAR_END:
                    event = parse_event_str(event)
                    schedule_events[date.strftime("%-m/%-d/%Y")] = event
    return schedule_events


def serialize_bell(schedule_events: dict[date, CalendarEvent], file_path: Path):
    with open(file_path, "w") as file:
        for date, event in schedule_events.items():
            if event.display_name:
                file.write(f"{date} {event.schedule_type} # {event.display_name}\n")
            else:
                file.write(f"{date} {event.schedule_type}\n")


def compare_schedules(local, remote) -> bool:
    for date, event in local.items():
        if date not in remote:
            return False
        if event.schedule_type != remote[date].schedule_type:
            return False
    return True


if __name__ == "__main__":
    remote_schedule_events = load_remote(REMOTE_SCHEDULE_PATH)
    print_schedule_events(remote_schedule_events)
    local_schedule_events = load_local()
    print_schedule_events(local_schedule_events)
    print(compare_schedules(local_schedule_events, remote_schedule_events))
