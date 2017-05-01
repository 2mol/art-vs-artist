
import re
import os
import time
import pickle
import urllib
import subprocess


from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup


def google_images_results(google_images_driver=None, search_term=None):
    ''' Performs a google images search for the given search term,
    returning a list of the image URLs on the first page (usually 100).
    '''
    image_urls = []

    #google_images_driver.get("https://images.google.com")
    # not stricly necessary, just assume that we already opened an image search

    driver = google_images_driver

    elem = driver.find_element_by_name("q")
    elem.clear()
    elem.send_keys(search_term)
    elem.send_keys(Keys.RETURN)

    # wait for our results page to load:
    while search_term not in driver.title:
        time.sleep(.5)

    body = driver.find_element_by_xpath('//body')

    while driver.page_source.count("rg_meta") < 120:
    # go to bottom of page to get some more search results
        body.send_keys(Keys.END)
        time.sleep(.5)

    # give the page a second to load the results:
    time.sleep(1)

    page_source = driver.page_source

    # ------ from here on out all clean --------

    soup = BeautifulSoup(page_source, 'html.parser')
    candidates = soup.find_all('div', class_="rg_meta")

    for tag in candidates:
        crap = tag.string
        regex = re.search(
            'https?://.*?\.(png|jpg|jpeg|gif)\"',
            crap,
            re.IGNORECASE,
        )

        if regex is not None:
            first_match = crap[regex.start():regex.end() - 1]
            image_urls.append(first_match)

    return image_urls[0:100]


def download_image_urls(image_urls=None):
    '''
    Download a list of URLs (doesn't strictly have to be images)
    Written to take a list as argument, because we can just let
    the downloader take care of parallel fetching.
    '''
    for incr, url in enumerate(image_urls):
        subdir = search_term.replace(' ', '_')
        folder = os.path.join('images', subdir)
        os.system(f'mkdir -p {folder}')

        file_ending = url[url.rfind('.'):]
        filename = str(incr).zfill(3) + file_ending
        file = os.path.join(folder, filename)

        cmd = [
            'aria2c', url, '-o', file,
            '--max-tries=2',
            '--retry-wait=1',
            '--connect-timeout=5',
            '--timeout=20',
        ]

        subprocess.call(cmd)

