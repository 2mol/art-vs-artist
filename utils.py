
import re
import pandas as pd

DATAFRAME_FILE = 'artist_dataframe.csv'

ARTIST_ATTRIBUTES = ['birthyear', 'artist_types', 'gender', 'ambiguous_name']

ARTIST_TYPES = {'painter', 'sculptor', 'photographer', 'illustrator',
                # calligrapher, graphic designer, textile printer,
                # watercolour painter, printmaker, muralist, ...
                }

COLUMNS = ARTIST_ATTRIBUTES


def empty_artist_dataframe():
    artist_dataframe = pd.DataFrame(columns=COLUMNS)
    # we index the dataframe by name because it makes no sense
    # to consider non-unique names anyway:
    artist_dataframe.index.name = 'Name'
    # artist_dataframe.sort('birthyear')
    return artist_dataframe


def load_artists():
    return pd.DataFrame.from_csv(DATAFRAME_FILE)


def save_artists(df):
    df.to_csv(DATAFRAME_FILE)


def set_to_string(things):
    cleaned_string = re.sub('({|}| )', '', str(things))
    return cleaned_string


def set_from_string(string):
    return set(string.split(','))

