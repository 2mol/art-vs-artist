import os, urllib
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup

driver = webdriver.Firefox()
driver.get("https://images.google.com")
#assert "Python" in driver.title
elem = driver.find_element_by_name("q")
#elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
#assert "No results found." not in driver.page_source

page_source = driver.page_source

# ------ from here on out all clean --------

soup = BeautifulSoup(page_source, 'html.parser')
candidates = soup.find_all('div', class_="rg_meta")

# for res in re.finditer("https?://.*\.(png|jpg|jpeg|gif)", re.IGNORECASE)

image_urls = []

for tag in candidates:
    crap = tag.string
    regex = re.search("https?://.*\.(png|jpg|jpeg|gif)", crap, re.IGNORECASE)
    if regex is not None:
        image_urls.append(crap[regex.start():regex.end()])

# for res in re.finditer("(?P<url>https?://[^\s]+)", s):
#     urls.append(s[res.start():res.end()+1])

for incr, url in enumerate(image_urls):
    subdir = '' # make this request dependent (i.e artist name)
    file_ending = url[url.rfind('.'):]
    filename = str(incr).zfill(3) + file_ending
    filepath = os.path.join('images', subdir, filename)
    os.system(f"wget {url} -O {filepath}")



# aaaall the way at the end: 
driver.close()