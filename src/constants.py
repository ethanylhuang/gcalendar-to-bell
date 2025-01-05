from pathlib import Path
from datetime import date

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent

REMOTE_SCHEDULE_PATH = PROJECT_ROOT / "src" / "schedules" / "lahs" / "calendar.bell"
# School year
SCHOOL_YEAR_START = date(2024, 8, 12)
SCHOOL_YEAR_END = date(2025, 6, 6)

# Github repo
REMOTE_URL = "https://github.com/nicolaschan/schedules.git"

# Google Calendar
CALENDAR_ID = "c_e281ee0055e616856c4f83178cad4a88da4cd3e11bc8b5354efb1ea14f45617e@group.calendar.google.com"
SERVICE_ACCOUNT_PATH = PROJECT_ROOT / "service-account.json"
