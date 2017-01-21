
import re
import os
import time
import pickle
import urllib
import subprocess


from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup


def fetch_google_images(search_terms):
    ''' Downloads google image search results (roughly the first 100)
    based on a list of search terms. Saves the results in folders,
    where the folder names correspond to the search terms.
    '''
    # ------------- set up only once for all search terms: -------------
    driver = webdriver.Firefox()
    driver.get("https://images.google.com")
    # ------------------------------------------------------------------

    for search_term in search_terms:
        elem = driver.find_element_by_name("q")
        elem.clear()
        elem.send_keys(search_term)
        elem.send_keys(Keys.RETURN)

        while search_term not in driver.title:
            time.sleep(.5)

        page_source = driver.page_source

        # ------ from here on out all clean --------

        soup = BeautifulSoup(page_source, 'html.parser')
        candidates = soup.find_all('div', class_="rg_meta")

        image_urls = []

        for tag in candidates:
            crap = tag.string
            regex = re.search(
                'https?://.*?\.(png|jpg|jpeg|gif)\"',
                crap,
                re.IGNORECASE)

            if regex is not None:
                first_match = crap[regex.start():regex.end() - 1]
                image_urls.append(first_match)

        for incr, url in enumerate(image_urls):
            subdir = search_term.replace(' ', '_')
            folder = os.path.join('images', subdir)
            os.system(f'mkdir -p {folder}')

            file_ending = url[url.rfind('.'):]
            filename = str(incr).zfill(3) + file_ending
            file = os.path.join(folder, filename)
            # os.system(f"wget {url} -O {file}")
            # os.system(f"aria2c {url} -o {file}")
            cmd = ['aria2c', url, '-o', file,
                   '--max-tries=2',
                   '--retry-wait=1',
                   '--connect-timeout=5',
                   '--timeout=20',
                   ]
            # subprocess is better:
            subprocess.call(cmd)

    # aaaall the way at the end:
    driver.close()
