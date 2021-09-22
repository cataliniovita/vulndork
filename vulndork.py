import os
import re
import git
import time
import sys
import argparse
import requests
import googlesearch 
from random import randint
from googlesearch import search
from time import sleep
from pathlib import Path
from stem import Signal
from stem.control import Controller
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from PyQt5 import QtWidgets, uic

def banner():
    print("""
                 _            _             _
                | |          | |           | |
     _   _ _   _| | ____   __| | ___   ____| |  _
    | | | | | | | ||  _ \ / _  |/ _ \ / ___| |_/ )
     \ V /| |_| | || | | ( (_| | |_| | |   |  _ (
      \_/ |____/ \_|_| |_|\____|\___/|_|   |_| \_)
                                v0.1
            """)

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

# Create a user agent list with 100 default size
def user_agent_rotate():
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]

    user_agent_rot = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=1555)

    # Return user_agent_rotator
    return user_agent_rot

# Check if an update is needed
def update_check():
    # Print vulndorks's banner
    banner()
    time_chk = get_file_timestamp()

    # Time limit set to 1 day
    if time_chk > 100:
        print("[!] Your local Google Hacking Database may be outdated. You can try to update it by running $ python3 scraper.py")
    # Convert to hours and print an update message
    else:
        hour_time = time_chk * 24
        if hour_time < 0:
            hour_time = hour_time + 1
            print("[!] Your local Google Hacking Database was updated", int(hour_time), "hour ago") 

# Add parameters to our program
def add_params(parser):
    parser.add_argument(
            '-d',
            dest="domain",
            action="store",
            required=False,
            help="scan a web-site for dork vulns")
    parser.add_argument(
            '-f',
            dest="dorksfile",
            action="store",
            required=False,
            help="choose dorks file")
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
            '-r',
            dest="randomdelay",
            action="store",
            required=False,
            help="set delay time between requests (40s by default)")
    parser.add_argument(
            '-p',
            dest="password",
            action="store",
            required=False,
            help="password for TOR (ip address rotator)")

# Clone the language code repo
def language_code():
    try:
        lang_file = open("8b60240ca6daaedd5a9f20f34617b4a7/google-language-codes", "r")
    except FileNotFoundError:
        git.Git(".").clone("https://gist.github.com/cataiovita/8b60240ca6daaedd5a9f20f34617b4a7")
        lang_file = open("8b60240ca6daaedd5a9f20f34617b4a7/google-language-codes", "r")

    lang_list = []

    while True:
        current_lang = lang_file.readline()
        code = current_lang[current_lang.find('\'') + len('\''):current_lang.rfind(':')]
        code = code.rstrip('\'')

        lang_list.append(code)

        if not current_lang:
            print("[*] Language codes gist cloned")
            return lang_list

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

    ip_response = session.get("http://httpbin.org/ip")

    try:
        print("[!] Your IP address is being renewed...")
        print("[+] Your renewed IP address is {0}".format(ip_response.json()['origin']))
    except json.decoder.JSONDecodeError:
        print("[-] Can't print renewed IP address")

    return session

def parse_dorks(args, dfile, multiple_str):
    dorks_results = []
    # Set delay for requests
    if args.randomdelay:
        delay = int(args.randomdelay)
    # Default delay - 40 s
    else:
        delay = 40

    current_num = 1
    d_len = dorks_len(dfile)
    dfile = open(args.dorksfile, "r")

    # Generate language codes list
    language_list = language_code()

    # Parse the file which contains the dorks and add the "site:" query into every line
    # Also send a request to google
    while True:
        current_dork = dfile.readline()
        dorks_results = []
            
        print("[*] Current dork is: " + current_dork.strip("\n") + " (" + str(current_num) + "/" + str(d_len) + ")")

        # Create a new tor session if password argument selected
        if args.password != '' and args.password != None:
            session = tor_session_cfg()
            renew_ip(args)
                
        current_num += 1

        # Rotate user agent
        user_agent_rotator = user_agent_rotate()
        user_agent = user_agent_rotator.get_random_user_agent()
        print("[+] Your User Agent is: " + user_agent)

        if args.urlsfile:
            add_site = multiple_str + " " + current_dork
            add_site = add_site.strip('\n')
            print(add_site)
        elif args.domain:
            add_site = "site:" + args.domain + " " + current_dork
            add_site = add_site.strip('\n')
        else:
            print("[-] No url or multiple urls found")
            return
 
        # Randomize a jitter
        rand_time = randint(1, 12)
        print("[!] Random delay is " + str(rand_time) + " seconds")
        delay += rand_time

        # Randomize language code
        code = language_list[randint(0, len(language_list) - 2)]

        # Make the proper google search
        dorks_results += googlesearch.search(
                add_site,
                lang=code,
                stop=1,
                num=1,
                pause=int(delay),
                user_agent=user_agent)

        if not current_dork:
            # TODO Raport the results
            # Create a list containing vulnerable dorks
            print("[+] All dorks parsed")
            break

        # Print vulnerable sites
        if dorks_results:
            print("[*] Vulnerable links found:")
            for result in dorks_results:
                print(result)
        # Sleep 1 second if we don't find any results (need for renew_ip delay)
        else:
            time.sleep(2)

        print("")

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
 
def renew_ip(args):
    # Grab the TOR password from args
    password = args.password

    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password=password)
        controller.signal(Signal.NEWNYM)

def dorks_len(dfile):
    dork_len = 0

    while dfile.readline():
        dork_len += 1
        
    return dork_len

if __name__ == "__main__":
    if db_exists() == True:
        # Create parser for arguments
        parser = argparse.ArgumentParser(
                description='Vulndork v0.1 - web-site vulnerability scanner based on Google Dorks',
                epilog="Vulndork is a web-site vulnerability scanner which uses the Google Hacking Database, available on exploit-db")

        # Add parameters to the parser
        add_params(parser)
        args = parser.parse_args()

        # Choose file (by default ghdb.dorks - all dorks file)
        if args.dorksfile:
            dorks_file = open(args.dorksfile, "r")
        else:
            dorks_file = open("ghdb.dorks", "r")

        if len(sys.argv) > 1:
            multiple_cstr = ""
            # Check for multiple clients scan
            if args.urlsfile:
                multiple_cstr = multiple_clients(args)
            # Parse dorks from dorks file
            dorks_results = parse_dorks(args, dorks_file, multiple_cstr)
            # Save output to a file, in case of '-o' option was selected
            save_output(args, dorks_results)
        else:
            print("usage: vulndork.py [-h] [-d DOMAIN] [-f DORKSFILE] [-m URLSFILE] [-o OUTPUTFILE] [-r RANDOM DELAY]")
            print("use vulndork.py --help for more info")
        
    else:
        print("[-] Google Hacking Database not found. Run $ python3 scraper.py to retrieve the dorks")
