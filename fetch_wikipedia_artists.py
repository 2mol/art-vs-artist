import pickle

import wikipedia

artists = []

women_20cen = wikipedia.page('List of 20th-century women artists')

ambiguous = False
all_fields = set()
relevant_fields = {'painter', 'sculptor', 'photographer', 'illustrator'}

artist_lines = []
for line in women_20cen.content.splitlines():
    if '(' in line and '),' in line:
        artist_lines.append(line)

for line in artist_lines:
    fields = set()
    year_info = line[line.rfind("(")+1 : line.rfind(")")]
    name_info, field_info = line.split('(' + year_info + ')')
    
    name_crap = name_info[name_info.find("(")+1 : name_info.find(")")]
    if name_crap.lower() == 'artist': ambiguous = True
    else: ambiguous = False

    for potential_field in field_info.split(','):
        potential_field = potential_field.strip()
        if potential_field == '': continue
        all_fields.add(potential_field)
        for relevant_field in relevant_fields:
            if relevant_field in potential_field:
                fields.add(relevant_field)
#            else:
#                fields.add('other')

    name = name_info.replace('(' + name_crap + ') ', '').strip()

    year_info_idx = year_info.find('18')
    if year_info_idx == -1:
        year_info_idx = year_info.find('19')
    birthyear = year_info[year_info_idx : year_info_idx + 4]

    gender = 'f'

    if fields == set(): continue

    artist_info = [name, fields, birthyear, gender, ambiguous]
    artists.append(artist_info)

artist_names = [artist[0] for artist in artists]

with open('artitst.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(artist_names))

with open('artist_list.pickle', 'wb') as f:
    pickle.dump(artist_names, f)


#ignored_categories = all_fields - categories