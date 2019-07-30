""" Connects to google images, performs a search and gets
the results, specifically their image urls.
"""

import re
import time

import selenium
from selenium.webdriver.common.keys import Keys


from bs4 import BeautifulSoup


def iter_search_google_images(search, max_results=None):
    ''' Iterator that returns a list of urls for each search term.
    '''

    search_inputs = search if isinstance(search, list) else [search]

    driver = selenium.webdriver.Firefox()

    try:
        driver.get("https://images.google.com")

        try:
            for search_term in search_inputs:
                urls = _search_google_images(
                    driver=driver,
                    search_term=search_term,
                    max_results=max_results
                )

                yield search_term, urls

        except Exception as e:
            print(f'failed for {search_term}')
            print(e)

    except Exception as e:
        print('total fail...')
        print(e)
    finally:
        driver.close()


def _search_google_images(driver=None, search_term=None, max_results=None):
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

    while driver.page_source.count("rg_meta") < max_results * 1.2:
        # go to bottom of page to get some more search results
        try:
            driver.find_element_by_xpath('//body').send_keys(Keys.END)
        except selenium.common.exceptions.NoSuchElementException:
            pass
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

manual_list = [
    "Lisa Hanawalt","Niki de Saint Phalle","James Turrell",
    "Pablo Picasso","Picasso","Wassily Kandinsky",
    "Francis Bacon","Leonardo DaVinci","Michelangelo",
    "Frida Kahlo","Artemisia Gentileschi","Joan Mitchell",
    "Jackson Pollock","Gustav Klimt","Egon Schiele",
    "Marlene Dumas","Tracey Emin","Jenny Saville",
    "Bridget Riley","Yves Klein","Alphonse Mucha",
    "Aubrey Beardsley","James Ensor","Edvard Munch",
    "Camille Claudel"
]

if __name__ == '__main__':
    """ just for testing
    """
    terms = manual_list

    print(f"== searching google images for {len(terms)} terms")

    for term, urls in iter_search_google_images(terms, max_results=100):
        print(term)
        print(f'<< found {len(urls)} urls <<-----------------')

    print("== success.")
