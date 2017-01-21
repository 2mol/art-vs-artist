from imagefetch import fetch_google_images

with open('artist_list.pickle', 'rb') as f:
    artist_list = pickle.load(f)

skip_number = artist_list.index('Olivia Peguero')

search_terms = artist_list[skip_number:]

fetch_google_images(search_terms)

