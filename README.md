# vulndork

## Introduction

## Installation

For the installation step, you will just need python3. Vulndork is written with Python 2.7.18

```
git clone https://github.com/cataiovita/vulndork/
cd vulndork
pip install -r requirements.txt
```

## API Rating

Google will start to block the requests after a limit between 6 and 10 (with low time delay between requests). So we need to increase the time delay and also add a random jitter. Also, a random language selector is used and an IP address rotator.

## IP address rotator

Having a low API Rating, we will need to rotate the IP addresses for every request. For this, vulndork uses tor package:

```sudo apt-get install tor```

We need to open the ```/etc/tor/torrc``` file and uncomment the ```ControlPort 9051``` line.

## Usage

First, we need to extract all dorks from [exploit-db dorks](https://www.exploit-db.com/google-hacking-database). So, you have to run ``scraper.py`` script with the following command:

``python3 scraper.py``

All the GHDB will be saved into a directory called dorks then will be stored into different files, taken by dork category. 

### Categories

There are 14 dork categories, stored inside a dictionary and saved in different files. We can run vulndork without argument and the dork file will be, by default, ghdb.dorks. We need to specifify the site with the ```-u``` port.

```python3 vulndork.py -u web-site.com```

## Improvement

A significant improvement of this tool will be to remove the high delay between requests. You can do that by using some of [AWS Lambda functions](https://aws.amazon.com/lambda/).
