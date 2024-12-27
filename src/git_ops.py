from git import Repo
import shutil
import os
from project_root import PROJECT_ROOT


def sync_schedules():

    REMOTE_URL = "https://github.com/nicolaschan/schedules.git"
    TEMP_DIR = PROJECT_ROOT / "src" / "schedules" / "temp_schedules"
    TARGET_DIR = PROJECT_ROOT / "src" / "schedules" / "lahs"

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
