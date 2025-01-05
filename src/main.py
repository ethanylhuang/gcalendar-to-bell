from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime, time
from calendar_ops import compare_schedules, load_local, load_remote, serialize_bell
from constants import REMOTE_SCHEDULE_PATH
from git_ops import sync_schedules
from utils import print_schedule_events


def main():
    local_schedule_events = load_local()
    print("Local Schedule Events:")
    print_schedule_events(local_schedule_events)
    sync_schedules()
    remote_schedule_events = load_remote(REMOTE_SCHEDULE_PATH)
    print("Remote Schedule Events:")
    print_schedule_events(remote_schedule_events)


if __name__ == "__main__":
    main()
