import requests
import json
import html_to_json
import os.path, time
from bs4 import BeautifulSoup
from datetime import datetime

def error_db():
    print("[-] Error! Couldn't get the User Agents Database")

def get_user_agents():
    user_agents_db = "https://developers.whatismybrowser.com/useragents/explore/operating_system_name/linux"

    # Initial header to browser mimic the request
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
        "Host" : "developers.whatismybrowser.com",
        "Connection": "close",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
    }

    ua_req_db = requests.get(user_agents_db, headers=headers, verify=True)

    if ua_req_db.status_code != 200:
        error_db()
        return

    json_page = ua_req_db.json()
    #json hierarchy :

if __name__ == "__main__":
    get_user_agents()
