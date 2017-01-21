
import re
import pandas as pd

DATAFRAME_FILE = 'artist_dataframe.csv'

ARTIST_ATTRIBUTES = ['birthyear', 'artist_types', 'gender', 'ambiguous_name']
# ARTIST_TYPES = ['painter', 'sculptor', 'photographer', 'illustrator']

# PAINTER      = 0x01
# SCULPTOR     = 0x02
# PHOTOGRAPHER = 0x04
# ILLUSTRATOR  = 0x08
# OTHER        = 0x10

# ARTIST_TYPES = {
#     'painter':      0x01,
#     'sculptor':     0x02,
#     'photographer': 0x04,
#     'illustrator':  0x08,
# }

COLUMNS = ARTIST_ATTRIBUTES  # + ARTIST_TYPES


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

