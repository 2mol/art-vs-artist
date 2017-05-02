
# structure:
    # open artist names db
    # call search function
    # call downloader function for search results

from selenium import webdriver
import pandas as pd

from fetch_images import get_image_urls, download_images

#np.save('all_urls-2017-04-02.npy', all_urls)
#read_dictionary = np.load('all_urls-2017-04-02.npy').item()

if __name__ == '__main__':
    ''' Run image fetching from start to finish
    '''

    df_artists = pd.DataFrame.from_csv('artist_dataframe.csv')

    artist_names = list(df_artists.index)

    #all_urls = dict(list(get_image_urls(search_terms=artist_names)))

    for artist_name, url_list in get_image_urls(search_terms=artist_names):
        download_images(image_urls=url_list, search_term=artist_name)

    #return all_urls
