
# structure:
    # open artist names db
    # call search function
    # call downloader function for search results

from selenium import webdriver

from fetch_images import google_images_results, download_image_urls


# open db with list of names...
artist_names = []

driver = webdriver.Firefox()
driver.get("https://images.google.com")

for name in artist_names:
    '''
    '''

    urls = google_images_results(google_images_driver=driver, search_term=name)

    download_image_urls(image_url_list=urls)

driver.close()
