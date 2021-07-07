import requests
import json
import html_to_json
import os.path, time
from bs4 import BeautifulSoup
from datetime import datetime

def error_db():
    print("[-] Error! Couldn't get the Google Hacking Database") 

# First, retrieve all dorks from exploit-db
def get_dorks():
    database_url = "https://www.exploit-db.com/google-hacking-database"

    # Need some headers for browser mimic
    # TODO make a variable User-Agent
    headers  = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "deflate, gzip, br",
        "Accept-Language": "en-US,en;q=0.5",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "X-Requested-With": "XMLHttpRequest",
        "Host": "www.exploit-db.com",
        "Connection": "keep-alive",
    }

    req_db = requests.get(database_url, headers=headers, verify=True)
    
    if req_db.status_code != 200:
        error_db()
        return

    json_page = req_db.json()
    # json hierarchy : data -> url_title -> intitle

    # 1. Filter by data json type
    page_data = json_page["data"]
 
    # 2. Filter by url_title type  
    for url in range(len(page_data)):
        iter_soup = BeautifulSoup(page_data[url]["url_title"], "html.parser") 
        # Filter the exact dorks we need
        dork = iter_soup.find("a").contents[0]
        print(dork)

    # Save dorks to a local file

def get_file_timestamp():
    # TODO scraper.py difference time 
    file_time = os.stat("README").st_mtime
    diff_time = (time.time() - file_time) / 86400
    print("days = ", diff_time)

    return diff_time

# Check if an update is needed
def update_check():
    time_chk = get_file_timestamp()

    # Time limit set to 1 day
    if time_chk < 1:
        print("[!] Your Google Hacking Database may be outdated. You can try to update it running scraper.py.")

get_dorks()
update_check()
get_file_timestamp()
