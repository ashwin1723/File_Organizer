import os
import shutil
import datetime
from pathlib import Path

# Define directories
DOWNLOADS_DIR = str(Path.home() / 'Downloads')

# File type mappings
FILE_CATEGORIES = {
    'download_doc': ['.pdf', '.doc', '.docx', '.txt'],
    'download_applications': ['.exe', '.msi', '.dmg', '.apk'],
    'download_mp3and4': ['.mp3', '.mp4', '.mkv', '.avi']
}

# Create folder name based on the week
def get_weekly_folder_name():
    today = datetime.date.today()
    return today.strftime('%Y_%m_%d')

# Organize files into specific folders
def organize_files():
    # Create weekly folder inside Downloads
    week_folder_name = get_weekly_folder_name()
    weekly_folder_path = os.path.join(DOWNLOADS_DIR, week_folder_name)
    os.makedirs(weekly_folder_path, exist_ok=True)

    # Create category subfolders
    category_folders = {}
    for category, extensions in FILE_CATEGORIES.items():
        category_folder_path = os.path.join(weekly_folder_path, category)
        os.makedirs(category_folder_path, exist_ok=True)
        category_folders[category] = category_folder_path

    # Move files based on their extensions
    for file_name in os.listdir(DOWNLOADS_DIR):
        file_path = os.path.join(DOWNLOADS_DIR, file_name)

        if os.path.isfile(file_path):
            file_extension = os.path.splitext(file_name)[1].lower()
            for category, extensions in FILE_CATEGORIES.items():
                if file_extension in extensions:
                    shutil.move(file_path, os.path.join(category_folders[category], file_name))
                    break

# Check for the last execution and run if necessary
LOG_FILE = os.path.join(DOWNLOADS_DIR, 'organizer_log.txt')

def has_already_run():
    if not os.path.exists(LOG_FILE):
        return False

    with open(LOG_FILE, 'r') as f:
        last_run_date = f.read().strip()

    try:
        last_run = datetime.datetime.strptime(last_run_date, '%Y-%m-%d').date()
        return last_run == datetime.date.today()
    except ValueError:
        return False

# Update the log file with today's date

def update_log():
    with open(LOG_FILE, 'w') as f:
        f.write(datetime.date.today().strftime('%Y-%m-%d'))

if __name__ == '__main__':
    if not has_already_run():
        organize_files()
        update_log()

