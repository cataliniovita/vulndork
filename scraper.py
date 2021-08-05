import requests
import json
import html_to_json
import os.path, time
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime

def error_db():
    print("[-] Error! Couldn't get the Google Hacking Database") 

def gather_done():
    print("[+] Local GHD succesfully updated")

def category_list():
    category = {
        "Web Server Detection": "dorks/web_server_detection.dorks",
        "Footholds": "dorks/footholds.dorks", 
        "Sensitive Directories": "dorks/sensitive_directories.dorks",
        "Vulnerable Files": "dorks/vulnerable_files.dorks",
        "Network or Vulnerability Data": "dorks/network_or_vulnerability_data.dorks",
        "Files Containing Passwords": "dorks/file_containing_password.dorks",
        "Files Containing Usernames": "dorks/files_containing_usernames.dorks",
        "Files Containing Juicy Info": "dorks/files_containing_juicy_info.dorks",
        "Advisories and Vulnerabilities": "dorks/advisories_and_vulnerabilities.dorks",
        "Vulnerable Servers": "dorks/vulnerable_servers.dorks",
        "Error Messages": "dorks/error_messages.dorks",
        "Pages Containing Login Portals": "dorks/pages_containing_login_portals.dorks",
        "Various Online Devices": "dorks/various_online_devices.dorks",
        "Sensitive Online Shopping Info": "dorks/sensitive_online_shopping_info.dorks",
    }
        
    if os.path.isfile("./dorks"):
        os.mkdir("./dorks") 

        for file_cat in category.values():
            open(file_cat, "a")
        
    return category

# First, retrieve all dorks from exploit-db
def get_dorks():
    database_url = "https://www.exploit-db.com/google-hacking-database"

    # Need some headers for browser mimic
    # TODO make a variable User-Agent
    headers = {
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

    # Save dorks to a local file
    dorks_file = open("ghdb.dorks", "w")

    # 1. Filter by data json type
    page_data = json_page["data"]
    cat_list = category_list()

    for category in page_data:
        page_cat = category["category"]
        find_file = str(page_cat["cat_title"])
        #print(page_cat["cat_title"])
        #print(cat_list.get(find_file))

    with open("dorks/footholds.dorks", "a") as f:
        f.write("a")

    # 2. Filter by url_title type  
    for url in range(len(page_data)):
        # Take the title
        title_soup = BeautifulSoup(page_data[url]["url_title"], "html.parser") 
        # Filter the exact dorks we need
        # Write all dorks to a default file
        dork = title_soup.find("a").contents[0]

        page_cat = category["category"]
        str(page_cat["cat_title"])     

        # Retrieve file specific to name of category
        # Use with block (close automatically)
        cat_name = cat_list.get(page_data[url]["category"]["cat_title"])

        with open(cat_name, "a") as cat_file:
            cat_file.write(dork)
            cat_file.write("\n")

        dorks_file.write(dork)
        dorks_file.write("\n")

        
        # Write to each separate file in /dorks dir
        
    return dorks_file

if __name__ == "__main__":
    get_dorks()
    gather_done()
