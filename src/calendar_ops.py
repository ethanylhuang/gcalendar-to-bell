from dataclasses import dataclass


@dataclass
class CalendarEvent:
    schedule_type: str
    display_name: str


# load from .bell
def load_remote():
    pass


# load from calendar events from google calendar api
def load_local():
    pass
