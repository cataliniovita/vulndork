import os
import time
import random
import numpy
from pathlib import Path

def db_exists():
   ghdb_file = Path("ghd.dorks")

   try:
       abs_path = ghdb_file.resolve(strict=True)
   except FileNotFoundError:
       print("[-] Google Hacking Database not found on your system. Run $ python3 scraper.py to take it")
       return False
   else:
       update_check()
       return True

# Calculate file timestamp for update_check
def get_file_timestamp():
    # TODO scraper.py difference time
    file_time = os.stat("ghd.dorks").st_mtime
    diff_time = (time.time() - file_time) / 86400

    return diff_time

# Check if an update is needed
def update_check():
    time_chk = get_file_timestamp()

    # Time limit set to 1 day
    if time_chk > 1:
        print("[!] Your local Google Hacking Database may be outdated. You can try to update it running scraper.py")
    # Convert to hours and print an update message
    else:
        hour_time = time_chk * 24
        if hour_time < 1:
            hour_time = hour_time + 1
            print("[!] Your local Google Hacking Database was updated", int(hour_time), "hour ago") 

        else:
            print("[!] Your local Google Hacking Database was updated", int(hour_time), "hours ago") 

db_exists()
