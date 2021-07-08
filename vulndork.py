import os
import time
import random
import numpy
import argparse
from googlesearch import search
from pathlib import Path

def info_usage():
    print("Usage: python3 vulndork") 
    
def db_exists():
    ghdb_file = Path("ghd.dorks")

    try:
        abs_path = ghdb_file.resolve(strict=True)
    except FileNotFoundError:
        print("[-] Google Hacking Database not found on your system. Run $ python3 scraper.py to retrieve the dorks")
        return False
    else:
        update_check()
        return True

# Calculate file timestamp for update_check
def get_file_timestamp():
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


if __name__ == "__main__":
    if db_exists() == True:
        ghdb_file = Path("ghd.dorks")
        dorks_file = open("ghd.dorks", "r")

        parser = argparse.ArgumentParser(description='Usage scraper.py [-h] [-d] <url>')
        parser.add_argument('-d', dest="domain", action="store", required=False, help="Scan a domain for dork vulns")
        args = parser.parse_args()

        if args.domain:
            # Parse the file which contains the dorks and add the "site:" query into every line
            # Also send a request to google
            while True:
                current_dork = dorks_file.readline()
                add_site = "site:" + args.domain + " " + current_dork
                add_site = add_site.strip('\n')
                #print(add_site)

                if not current_dork:
                    # TODO Raport the results
                    # Create a list containing vulnerable dorks
                    print("[+] All dorks parsed")
                    break 

        else:
            print("Yea")
            
        dorks_file.close()
    
    query = "site:cymed.ro"
    d_results = search(query, num_results=100)

    for result in d_results:
        if result is None:
            print("No page found")
        else:
            print(result)
