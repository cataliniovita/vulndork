# vulndork

## Introduction

**Vulndork** is an OSINT tool, based on Google Dorks. Google dorks are specific filters applied to google search strings. Exploit-db have a public database of dorks, called [Google Hacking Database](https://www.exploit-db.com/google-hacking-database) and vulndork use this database, trying to make continuous google searches to check for vulnerable pages. A specific possible dork which indicates a vulnerable web-site looks like:

```inurl /admin/login.php intitle panel admin```

This dork indicates that is looking for a login.php page inside admin directory, having panel admin in the title of the page. This could be a possible attack vector, so a vulnerability is found.

## Installation

For the installation step, you will just need python3. Vulndork is written with Python 2.7.18

```
git clone https://github.com/cataiovita/vulndork/
cd vulndork
pip install -r requirements.txt
```

## API Rating

Google will start to block the requests after a limit between 6 and 10 (with low time delay between requests). So we need to increase the time delay and also add a random jitter for every requests. Also, we're using an User-Agents rotator, a google language randomizer and an IP Address rotator.

## IP address rotator

### Install tor package

+ Having a low API Rating, we will need to rotate the IP addresses for every request. For this, vulndork uses tor package:

```sudo apt-get install tor```

We need to open the ```/etc/tor/torrc``` file and uncomment the ```ControlPort 9051``` line.

### Set a password for TOR

#### 1. Generate TOR password

+ Tor is using a hashed password, so to generate it use the command below. We will need to insert the hashed password inside the tor config file.

```tor --hash-password "passwordhere"```

#### 2. Edit config file

+ Open the ```/etc/tor/torrc``` file with your favorite text editor and comment the line set before:

```#CookieAuthentication 0```

+ Find the ```#HashedControlPassword 16:2283409283049820409238409284028340238409238``` line and uncomment it and replace the password hash with **your password** generated at step 1 and save the changes.

```HashedControlPassword 16:113BD60B17CD1E98609013B4426860D576F7096C189184808AFF551F65```

#### 3. Restart TOR service

+ Restart TOR service and now it should be an available TOR network connection.

```sudo /etc/init.d/tor restart```

## Usage

+ First, we need to extract all dorks from [exploit-db dorks](https://www.exploit-db.com/google-hacking-database). So, you have to run ``scraper.py`` script with the following command:

``python3 scraper.py``

All the GHDB will be saved into a directory called dorks then will be stored into different files, taken by dork category. 

### Categories

+ There are 14 dork categories, stored inside a dictionary and saved inside different files. We can run vulndork without argument and the dork file will be, by default, ghdb.dorks. Vulndork also uses a language randomization, cloning a gist which contains google-language format list. To use vulndork in minimal form, we need to specifify the site with the ```-d``` argument.

```python3 vulndork.py -d web-site.com```

### Time delay

+ Vulndork also has an extra delay which can be added, if Google is blocking you. You can add, for example, an extra delay of 10 seconds between the requests.  

```python3 vulndork.py -d web-site.com -f dorks/footholds.dork -r 10```

### Language rotator

+ For every google search, vulndork rotates the google-lanaguages codes, doing this using a list, contained into a gist. This method helps the API Rating, and reduce the change to get a 429 response. This gist is cloned inside the script:

[google language codes](https://gist.github.com/cataiovita/8b60240ca6daaedd5a9f20f34617b4a7)

### TOR ip address rotator

+ You can use TOR, after you get through the steps above, using the ``-p`` parameter, representing the password of TOR.

```python3 vulndork.py -d web-site.com -p passwordhere```

## Improvement

A significant improvement of this tool will be to remove the high delay between requests. You can do that by using some of [AWS Lambda functions](https://aws.amazon.com/lambda/).
