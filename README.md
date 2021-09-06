# vulndork

## Introduction

## Installation

## Usage

First, we need to extract all dorks from [exploit-db dorks](https://www.exploit-db.com/google-hacking-database). So, you have to run ``scraper.py`` script with the following command:

``python3 scraper.py``

All the GHDB will be saved into a directory called dorks then will be stored into different files, taken by dork category. 

## API Rating

Google will start to block the requests after a limit between 6 and 10 (with low time delay between requests). So we need to increase the time delay and also add a random jitter.

Google also has blocked much of all TOR nodes so the rotations between TOR ip's is also unefficient.

1. create a python scraper to extract all google hacking database -> https://www.exploit-db.com/google-hacking-database	
scraper.py
2. tor connection -> https://linuxaria.com/howto/how-to-anonymize-the-programs-from-your-terminal-with-torify
3. create the ip rotator


## Improvement

A significant improvement of this tool will be to remove the high delay between requests. You can do that by using some of [AWS Lambda functions](https://aws.amazon.com/lambda/).
