import requests
import json
import html_to_json
import os.path, time
from bs4 import BeautifulSoup
from datetime import datetime

def error_db():
    print("[-] Error! Couldn't get the Google Hacking Database") 

def gather_done():
    print("[+] Local GHD succesfully updated")

def category_list():
    category = {
        "/dorks/web_server_detection.dorks": "Web Server Detection",
        "/dorks/footholds.dorks": "Footholds",
        "/dorks/sensitive_directories.dorks": "Sensitives Directories",
        "/dorks/vulnerable_files.dorks": "Vulnerable Files",
        "/dorks/network_or_vulnerability_data.dorks": "Network or Vulnerability Data",
        "/dorks/file_containing_password.dorks": "File Containing Passwords",
        "/dorks/file_containing_usernames.dorks": "File Containing Usernames",
        "/dorks/file_containing_juicy_info.dorks": "File Containing Juicy Info",
        "/dorks/advisories_and_vulnerabilities.dorks": "Advisories and Vulnerabilities",
        "/dorks/vulnerable_servers.dorks": "Vulnerable Servers",
        "/dorks/error_messages.dorks": "Error Messages",
        "/dorks/pages_containing_login_portals.dorks": "Pages Containing Login Portals",
        "/dorks/various_online_devices.dorks": "Various Online devices",
        "/dorks/sensitive_online_shopping_info.dorks": "Sensitive Online Shopping Info",
    }

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
    
    for category in page_data:
        page_cat = category["category"]
        print(page_cat["cat_title"])

    # 2. Filter by url_title type  
    for url in range(len(page_data)):
        # Take the title
        title_soup = BeautifulSoup(page_data[url]["url_title"], "html.parser") 
        # Filter the exact dorks we need
        dork = title_soup.find("a").contents[0]
        dorks_file.write(dork)
        dorks_file.write("\n")
        
    return dorks_file

if __name__ == "__main__":
    get_dorks()
    gather_done()
