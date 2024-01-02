#File Date Updater

#This script recursively goes through a directory structure located at './downloaded_files'.
#The structure is yyyy/mm/dd.
#	or each file found, it updates the file's modification date to match the date indicated by the directory structure.

import os
import datetime
import calendar
import sys

def update_file_dates(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_date = get_file_date(root)
            update_file_date(file_path, file_date)
#            print("Updated file: {}".format(file_path))

def get_file_date(directory):
    # Extract the year, month, and day from the directory path
    date_parts = [int(part) for part in directory.split(os.sep) if part.isdigit()]
    year = date_parts[0]
    month = date_parts[1] if len(date_parts) > 1 else 1
    day = date_parts[2] if len(date_parts) > 2 else 1
    return datetime.datetime(year, month, day)

def update_file_date(file_path, new_date):
    new_timestamp = calendar.timegm(new_date.timetuple())
    os.utime(file_path, (new_timestamp, new_timestamp))

# Check if the root_dir parameter is provided
if len(sys.argv) < 2:
    print("Error: The root_dir parameter is required.")
    print("Please provide the root directory path.")
    sys.exit(1)

root_dir = sys.argv[1]

print("Starting file date update...")

update_file_dates(root_dir)

print("File date update completed.")
