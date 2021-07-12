import os
import time
import random
import numpy
import argparse
import googlesearch 
from pathlib import Path

def info_usage():
    print("Usage: python3 vulndork") 

def db_exists():
    ghdb_file = Path("ghdb.dorks")

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
            required=True,
            help="scan a web-site for dork vulns")
    parser.add_argument(
            '-m',
            dest="urls or file",
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
            '-l',
            dest="limit",
            action="store",
            required=False,
            help="set limit time between requests (1s by default)")

# Save output to a file (-o option from params)
def save_output(args, dorks_results):
    if args.outputfile:
        outfile = open(args.outputfile, "w")
        dorks_len = len(dorks_results)

        for i in range(dorks_len):
            print(dorks_results[i])
            outfile.write(dorks_results[i])

        outfile.close()

def parse_dorks(args, dfile):
    dorks_results = []

    # Set limit for requests
    if args.limit:
        limit = args.limit
    else:
        limit = 1

    if args.url:
        # Parse the file which contains the dorks and add the "site:" query into every line
        # Also send a request to google
        while True:
            current_dork = dfile.readline()
            add_site = "site:" + args.url + " " + current_dork
            add_site = add_site.strip('\n')
 
            dorks_results = googlesearch.search(
                    add_site,
                    start=0,
                    num=2,
                    pause=limit)

            if not current_dork:
                # TODO Raport the results
                # Create a list containing vulnerable dorks
                print("[+] All dorks parsed")
                break

            for result in dorks_results:
                 print(result)

    return dorks_results

if __name__ == "__main__":
    if db_exists() == True:
        dorks_file = open("ghdb.dorks", "r")

        # Create parser for arguments
        parser = argparse.ArgumentParser(
                description='Vulndork v0.1 - web-site vulnerability scanner based on Google Dorks',
                epilog="Vulndork is a web-site vulnerability scanner which uses the Google Hacking Database, available on exploit-db")

        add_params(parser)
        args = parser.parse_args()

        # Parse dorks from dorks file
        dorks_results = parse_dorks(args, dorks_file)

        # Save output into a file, in case of '-o' option was selected
        save_output(args, dorks_results)
        dorks_file.close()

    else:
        print(" ")
