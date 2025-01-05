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
