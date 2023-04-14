"""
A script to produce a JSON file with all the metadata you need to create a new private article.
Run after creating figshare_models.py (see create_models.readme).
This script takes researcher_metadata.csv as input.
Extracts metadata from the csv, and creates a pydantic object with
those metadata as attributes. 
"""

from pandas import read_csv, isnull
import pydantic
import figshare_models

def filter_records(column, match):
    """
    Filter rows collected from the spreadsheet where a certain column matches a certain number or word (match). 
    Return a list of dictionaries, or an empty list if no matches.
    If we know there should be only match, e.g. title, we can extract the 0th element from the resulting list.
    """
    return( [ d for d in records if d[column] == match ] )

def get_dicts_from_records(myrecords):
    """ For items with multiple attributes, create a dict for each item. E.g. each author."""
    item_order = sorted(set( d['id'] for d in myrecords ))
    item_dicts = []
    for i in item_order:
        current_records = [ d for d in myrecords if d['id'] == i ]
        current_dict = {}
        for d in current_records:
            current_dict[d['Attr_key']] = d['Attr_value']
        item_dicts.append(current_dict)
    return(item_dicts)




# read in the metadata
data = read_csv('researcher_metadata_figshare.csv', dtype={'id':'Int32'}) # stop pandas from automatically converting int to float
records = data.to_dict(orient='records')
for d in records: # stupid pandas doesn't let me change NA to something else when I read in the data
    for k, v in d.items():
        if isnull(v):
            d[k] = None
# records looks like:
# [
#     {'Attr': 'authors', 'id': 1, 'Attr_key': 'full_name', 'Attr_value': 'Virginia Scarlett'}, 
#     {'Attr': 'authors', 'id': 1, 'Attr_key': 'figshare_id', 'Attr_value': '14526911'}, 
#     {'Attr': 'authors', 'id': 1, 'Attr_key': 'orcid_id', 'Attr_value': '0000-0002-4156-2849'}, 
#     {'Attr': 'authors', 'id': 1, 'Attr_key': 'url_name', 'Attr_value': 'Virginia_Scarlett'}, 
#     {'Attr': 'authors', 'id': 2, 'Attr_key': 'full_name', 'Attr_value': 'William Shakespeare'}, 
#     {'Attr': 'title', 'id': None, 'Attr_key': 'title', 'Attr_value': 'My cool dataset'}, 
#     ...
# ]

# First, title.
title = filter_records('Attr', 'title')[0]['Attr_value']
# Next, description.
desc = filter_records('Attr', 'description')[0]['Attr_value']
# Next, keywords.
keyw_records = filter_records('Attr', 'keywords')
keyw = [ record['Attr_value'] for record in keyw_records ]
# Next, categories.
cat_records = filter_records('Attr', 'categories')
cat_dicts = get_dicts_from_records(cat_records) # looks like: [{'categories': '24748', 'categories_by_source_id': '320999'}, {'categories': '24169', 'categories_by_source_id': '310112'}]
cats = [ int(d['categories']) for d in cat_dicts ]
cat_src = [ str(d['categories_by_source_id']) for d in cat_dicts ]


# Next, authors.
# From the create private article section of figshare API docs:
# "Can contain the following fields: id, name, first_name, last_name, email, orcid_id. 
# If an id is supplied, it will take priority and everything else will be ignored. 
# No more than 10 authors. For adding more authors use the specific authors endpoint."
auth_records = filter_records('Attr', 'authors')
auth_dicts = get_dicts_from_records(auth_records) # looks like: [{'name': 'Virginia Scarlett', 'id': '14526911'}, {'url_name': 'William _Shakespeare', 'name': 'William Shakespeare'}]
for d in auth_dicts:
    for k, v in d.items():
        if k == 'id':
            d[k] = int(v)

auth_objs = [ figshare_models.Author(**d) for d in auth_dicts ]

# Next, defined_type.
dt = filter_records('Attr', 'defined_type')[0]['Attr_value']

my_private_article = figshare_models.Model(
    title = title,
    description = desc,
    is_metadata_record = True,
    metadata_reason = "Data file to be uploaded separately via API",
    tags = keyw,
    keywords = keyw,
    references = [],
    categories = cats,
    categories_by_source_id = cat_src,
    authors = auth_objs,
    defined_type = dt
    )

# Now we have a handy python object. We can access attributes like my_private_article.title, and add attributes fairly easily. 
# Pydantic has tons of ways to manipulate these objects, e.g. enforce a certain datetime encoding, export to dict e.g. my_item.dict(), and other useful stuff

# Apparently the figshare API doesn't like "null" fields, so I am just removing these attributes.
attrs_to_remove = [
    'custom_fields',
    'custom_fields_list',
    'funding',
    'funding_list',
    'license',
    'doi',
    'handle',
    'resource_doi',
    'resource_title',
    'timeline',
    'group_id'
]

for e in attrs_to_remove:
    exec(f'del my_private_article.{e}')

# let's export to json and write to a file.
with open('researcher_metadata.json', 'w') as outF:
    outF.write(my_private_article.json(indent=4))

