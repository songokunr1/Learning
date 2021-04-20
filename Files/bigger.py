import os
import shutil
from datetime import datetime, timedelta
import pathlib


def backups(ext: str, directory_path=os.getcwd(), destination=os.getcwd()):
    files_to_backup = []
    three_days_ago = datetime.now() - timedelta(days=3)
    for path_to_dir, dirs, files in os.walk(directory_path):
        for file in files:
            path_to_file = os.path.join(path_to_dir, file)
            if pathlib.Path(path_to_file).suffix == "." + ext:
                if file_modification_date := datetime.fromtimestamp(os.path.getmtime(path_to_file)):
                    files_to_backup.append(path_to_file)
    path_to_backup_dir = os.path.join(destination, "Backup")
    try:
        os.mkdir(path_to_backup_dir)
    except FileExistsError as error:
        pass
    path_to_backup_dir = os.path.join(path_to_dir, f"copy-{datetime.now().strftime('%Y %m %d')}")
    try:
        os.mkdir(path_to_backup_dir)
    except FileExistsError as error:
        pass
    for path_to_file in files_to_backup:
        shutil.copy(path_to_file, path_to_backup_dir)
