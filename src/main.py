from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime, time
from gcalendar_ops import get_schedule_events
from git_ops import sync_schedules


def main():
    schedule_events = get_schedule_events()
    sync_schedules()
    print("Finished fetching schedule from api and syncing schedules to remote repo")
    # for event in schedule_events:
    #     print(event["summary"])


if __name__ == "__main__":
    main()
