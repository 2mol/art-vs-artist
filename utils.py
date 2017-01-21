import pandas as pd

DATAFRAME_FILE = 'artist_dataframe.csv'

ARTIST_ATTRIBUTES = ['birthyear', 'gender', 'ambiguous_name']
# ARTIST_TYPES = ['painter', 'sculptor', 'photographer', 'illustrator']

# PAINTER      = 0x01
# SCULPTOR     = 0x02
# PHOTOGRAPHER = 0x04
# ILLUSTRATOR  = 0x08
# OTHER        = 0x10

COLUMNS = ARTIST_ATTRIBUTES #+ ARTIST_TYPES

# ------------------------------------------------------------------

artist_dataframe = pd.DataFrame(columns = COLUMNS)
artist_dataframe.index.name = 'Name'





artist_dataframe.sort('birthyear')
