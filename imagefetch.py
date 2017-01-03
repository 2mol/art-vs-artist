import re, os, urllib, subprocess
import pickle

import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup

STARTFROM = 'Olivia Peguero'

# ------------- set up: ----------

driver = webdriver.Firefox()
driver.get("https://images.google.com")

# --------------------------------

with open('artist_list.pickle', 'rb') as f:
    artist_list = pickle.load(f)

skip_number = artist_list.index(STARTFROM)

for artist_name in artist_list[skip_number:]:
    elem = driver.find_element_by_name("q")
    elem.clear()
    elem.send_keys(artist_name)
    elem.send_keys(Keys.RETURN)

    while artist_name not in driver.title:
        time.sleep(1)

    page_source = driver.page_source

    # ------ from here on out all clean --------

    soup = BeautifulSoup(page_source, 'html.parser')
    candidates = soup.find_all('div', class_="rg_meta")

    image_urls = []

    for tag in candidates:
        crap = tag.string
        regex = re.search('https?://.*?\.(png|jpg|jpeg|gif)\"', crap, re.IGNORECASE)
        if regex is not None:
            first_match = crap[regex.start():regex.end()-1]
            image_urls.append(first_match)

    for incr, url in enumerate(image_urls):
        subdir = artist_name.replace(' ', '_')
        folder = os.path.join('images', subdir)
        os.system(f"mkdir -p {folder}")

        file_ending = url[url.rfind('.'):]
        filename = str(incr).zfill(3) + file_ending
        file = os.path.join(folder, filename)
        # os.system(f"wget {url} -O {file}")
        # os.system(f"aria2c {url} -o {file}")
        cmd = ['aria2c', url, '-o', file,
               '--max-tries=2',
               '--retry-wait=1',
               '--connect-timeout=5',
               '--timeout=20',]
        # subprocess is better:
        subprocess.call(cmd)


# aaaall the way at the end: 
driver.close()
