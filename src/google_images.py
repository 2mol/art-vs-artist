""" Connects to google images, performs a search and gets
the results, specifically their image urls.
"""

import re
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup


def get_image_urls(search_input, max_results=100):
    """
    """
    if isinstance(search_input, str):
        search_inputs = [search_input]
    elif isinstance(search_input, list):
        search_inputs = search_input
    else:
        raise Exception("pass either a string or a list as search term")

    return perform_search_google_images(
        search_inputs,
        max_results=max_results
    )



# utility functions


def perform_search_google_images(search_inputs, max_results=None):
    ''' Iterator that returns a list of urls for each search term.
    '''
    driver = webdriver.Firefox()

    try:
        driver.get("https://images.google.com")

        for search_term in search_inputs:
            urls = search_google_images(
                driver=driver,
                search_term=search_term,
                max_results=max_results
            )

            yield search_term, urls

    finally:
        driver.close()


def search_google_images(driver=None, search_term=None, max_results=None):
    ''' Performs a google images search for the given search term,
    returning a list of the image URLs on the first page.
    '''
    image_urls = []

    elem = driver.find_element_by_name("q")
    elem.clear()
    elem.send_keys(search_term)
    elem.send_keys(Keys.RETURN)

    # wait for our results page to load:
    while search_term not in driver.title:
        time.sleep(.1)

    time.sleep(.5)

    while driver.page_source.count("rg_meta") < max_results * 1.2:
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

    return image_urls[0:max_results]


if __name__ == '__main__':

    urls = list(
        get_image_urls("picasso", max_results=100)
        )

    print(len(urls))
    print(urls)
