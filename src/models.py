from dataclasses import dataclass


@dataclass
class CalendarEvent:
    schedule_type: str
    display_name: str
