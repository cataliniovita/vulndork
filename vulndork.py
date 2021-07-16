import os
import time
import sys
import numpy
import argparse
import requests
import googlesearch 
from pathlib import Path
from stem import Signal
from stem.control import Controller

def info_usage():
    print("Usage: python3 vulndork") 

def error_gs():
    print("[-] Error! Couldn't send the get request") 

def db_exists():
    ghdb_file = Path("ghdb.dorks")

    try:
        abs_path = ghdb_file.resolve(strict=True)
    except FileNotFoundError:
        return False
    else:
        update_check()
        return True

# Calculate file timestamp for update_check
def get_file_timestamp():
    file_time = os.stat("README.md").st_mtime
    diff_time = (time.time() - file_time) / 86400

    return diff_time

# Check if an update is needed
def update_check():
    time_chk = get_file_timestamp()

    # Time limit set to 1 day
    if time_chk > 1:
        print("[!] Your local Google Hacking Database may be outdated. You can try to update it by running $ python3 scraper.py")
    # Convert to hours and print an update message
    else:
        hour_time = time_chk * 24
        if hour_time < 1:
            hour_time = hour_time + 1
            print("[!] Your local Google Hacking Database was updated", int(hour_time), "hour ago") 
        else:
            print("[!] Your local Google Hacking Database was updated", int(hour_time), "hours ago") 

# Add parameters to our program
def add_params(parser):
    parser.add_argument(
            '-u',
            dest="url",
            action="store",
            required=False,
            help="scan a web-site for dork vulns")
    parser.add_argument(
            '-m',
            dest="urlsfile",
            action="store",
            required=False,
            help="scan multiple clients for dork vulns")
    parser.add_argument(
            '-o',
            dest="outputfile",
            action="store",
            required=False,
            help="save scan result to file")
    parser.add_argument(
            '-d',
            dest="delay",
            action="store",
            required=False,
            help="set delay time between requests (1s by default)")

# Save output to a file (-o option from params)
def save_output(args, dorks_results):
    if args.outputfile:
        outfile = open(args.outputfile, "w")
        dorks_len = len(dorks_results)

        for i in range(dorks_len):
            print(dorks_results[i])
            outfile.write(dorks_results[i])

        outfile.close()

# Create a tor session
def tor_session_cfg():
    session = requests.session()
    session.proxies = {'http': 'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050'}
    return session

# Scrape the google search
def google_search(query):
    base_query = "https://google.com/search?q="
    print("Yes")

    headers = {
        "Host": "google.com",
        "Connection": "close",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
    }

    base_query = base_query + "a"
    req_gs = requests.get(base_query, headers=headers, verify=True, allow_redirects=False)

    print(req_gs.status_code)

    if req_gs.status_code != 200:
        error_gs()
        return

    json_gs = req_gs.json()

    print(json_gs)

def parse_dorks(args, dfile, multiple_str):
    dorks_results = []
    # Set delay for requests
    if args.delay:
        delay = int(args.delay)
    else:
        delay  = 1

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
    # Parse the file which contains the dorks and add the "site:" query into every line
    # Also send a request to google
    while True:
        current_dork = dfile.readline()
            
        if args.urlsfile:
            add_site = multiple_str + " " + current_dork
            add_site = add_site.strip('\n')
            print(add_site)
        elif args.url:
            add_site = "site:" + args.url + " " + current_dork
            add_site = add_site.strip('\n')
        else:
            print("[-] No url or multiple urls found")
            return
 
        dorks_results = googlesearch.search(
                add_site,
                start=0,
                num=4,
                pause=int(delay),
                user_agent=user_agent)

        if not current_dork:
            # TODO Raport the results
            # Create a list containing vulnerable dorks
            print("[+] All dorks parsed")
            break

        for result in dorks_results:
            print(result)

    return dorks_results

def multiple_clients(args):
    try:
        c_file = open(args.urlsfile, "r")
        ret_file = open(args.urlsfile, "r")
    except FileNotFoundError:
        print("[-] File " + "\"" + args.urlsfile + "\"" + " not found on your system")
        return ""

    # Create an increment to get last line
    client_string = ""
    incr = 0
    len_f = len(ret_file.readlines()) 
    # Create multiple queries for clients
    if args.urlsfile:
        while True:
            client = c_file.readline()
            incr += 1

            if not client:
                break

            client_string += "site:"
            client_string += client
            client_string = client_string.rstrip("\n")

            if incr != len_f:
                client_string += " | "

    return client_string
 
def test_stem():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password='your password set for tor controller port in torrc')
        print("Success!")
        controller.signal(Signal.NEWNYM)
        print("New Tor connection processed")

if __name__ == "__main__":
    if db_exists() == True:
        dorks_file = open("ghdb.dorks", "r")

        ## Create parser for arguments
        #parser = argparse.ArgumentParser(
        #        description='Vulndork v0.1 - web-site vulnerability scanner based on Google Dorks',
        #        epilog="Vulndork is a web-site vulnerability scanner which uses the Google Hacking Database, available on exploit-db")

        ## Add parameters to the parser
        #add_params(parser)
        #args = parser.parse_args()

        #if len(sys.argv) > 1:
        #    multiple_cstr = ""
        #    # Check for multiple clients scan
        #    if args.urlsfile:
        #        multiple_cstr = multiple_clients(args)
        #    # Parse dorks from dorks file
        #    dorks_results = parse_dorks(args, dorks_file, multiple_cstr)
        #    # Save output into a file, in case of '-o' option was selected
        #    save_output(args, dorks_results)
        #else:
        #    print("usage: vulndork.py [-h] [-u URL] [-m URLSFILE] [-o OUTPUTFILE] [-d DELAY]")
        #    print("use vulndork.py --help for more info")
        #
        #google_search("yup")

        session = tor_session_cfg()

        session = tor_session_cfg()
        print(session.get("http://httpbin.org/ip").text)
        # Above should print an IP different than your public IP

        # Following prints your normal public IP
        print(requests.get("http://httpbin.org/ip").text)

        test_stem()

    else:
        print("[-] Google Hacking Database not found. Run $ python3 scraper.py to retrieve the dorks")
