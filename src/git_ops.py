from git import Repo
import shutil
import os
from constants import PROJECT_ROOT, REMOTE_SCHEDULE_PATH, REMOTE_URL


def sync_schedules():

    TEMP_DIR = REMOTE_SCHEDULE_PATH.parent.parent / "temp_schedules"
    TARGET_DIR = REMOTE_SCHEDULE_PATH.parent

    # Clone repository
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    Repo.clone_from(REMOTE_URL, str(TEMP_DIR))

    # Copy LAHS directory
    if os.path.exists(TARGET_DIR):
        shutil.rmtree(TARGET_DIR)
    shutil.copytree(TEMP_DIR / "lahs", TARGET_DIR)

    # Cleanup
    shutil.rmtree(TEMP_DIR)


if __name__ == "__main__":
    sync_schedules()
