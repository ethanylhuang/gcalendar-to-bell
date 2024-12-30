from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime, time
from gcalendar_ops import get_schedule_events
from git_ops import sync_schedules


def main():
    schedule_events = get_schedule_events()
    for date, event in schedule_events.items():
        print(date, event.display_name, event.schedule_type)


if __name__ == "__main__":
    main()
