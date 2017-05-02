
import re
import os
import time
import pickle
import urllib
import subprocess
import tempfile

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup


def get_image_urls(search_terms=None):
    ''' Call the google image fetcher for list of search terms
    '''
    driver = webdriver.Firefox()
    driver.get("https://images.google.com")

    for search_term in search_terms:
        urls = google_images_result_urls(
            driver=driver,
            search_term=search_term
        )

        yield search_term, urls

    driver.close()


def google_images_result_urls(driver=None, search_term=None):
    ''' Performs a google images search for the given search term,
    returning a list of the image URLs on the first page (usually 100).
    '''
    image_urls = []

    elem = driver.find_element_by_name("q")
    elem.clear()
    elem.send_keys(search_term)
    elem.send_keys(Keys.RETURN)

    # wait for our results page to load:
    while search_term not in driver.title:
        time.sleep(.1)

    while driver.page_source.count("rg_meta") < 120:
    # go to bottom of page to get some more search results
        driver.find_element_by_xpath('//body').send_keys(Keys.END)
        time.sleep(.5)

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


def download_images(image_urls=None, search_term=None):
    '''
    Download a list of URLs (doesn't strictly have to be images)
    Written to take a list as argument, because we can just let
    the downloader take care of parallel fetching.
    '''
    subdir = search_term.replace(' ', '_')
    folder = os.path.join('images', subdir)
    os.system(f'mkdir -p {folder}')

    url_folder = 'url_lists'
    os.system(f'mkdir -p {url_folder}')
    url_list_file = os.path.join(url_folder, f'{subdir}.txt')

    with open(url_list_file, 'w') as f:
        f.write('\n'.join(image_urls))

    cmd = [
        'aria2c',
        '-i', url_list_file,
        '-d', folder,
        '--max-tries=2',
        '--retry-wait=1',
        '--connect-timeout=5',
        '--timeout=20',
    ]

    subprocess.Popen(cmd)

