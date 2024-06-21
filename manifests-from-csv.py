# Required metadata fields:
# - display_template
# - objectid
# - parentid field in which each child object is assigned a value equal to the objectid of its parent
# - pid
# - title
# - infojson field with links to info.json files using IIIF image api
# - object_location
# If csv has data on the height and width of each object, the getdimensions portion can be commented out and height and width can be redefined to pull from that field instead.
# This script creates v3 manifests.
# As written, this script requires the Live Server VSCode extension

import csv
from iiif_prezi3 import Manifest
import requests
import json

# Pull height and width of each image from its info.json file
def getdimensions(infojson):
    response = requests.get(infojson).json()
    height = response["height"]
    width = response["width"]
    return height, width

# Read metadata csv file (as long as such a file with the correct name is in the same folder as this script)
# Creates a dictionary of objects, appending children to their parents and including non-multiples as standalone objects
working_data = {}
with open('wpa_clean.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader: 
        if row['display_template'] == 'multiple':
            working_data[row['objectid']] = {'parent': row, 'children': []}
        elif row['parentid']:
            working_data[row['parentid']]['children'].append(row)
        else:
            working_data[row['objectid']] = {'parent': row, 'children': []}

# Start constructing manifest, including constructing a URL based on the parent's pid
for index,(manifestid,values) in enumerate(working_data.items()):
    title = 'title'
    url = "https://digitalcollections.lib.iastate.edu/iiif/2/isu:{}".format(values['parent']['pid'] + "/manifest.json")
    manifest = Manifest(id=url, label={"en":[values['parent']['title']]})

#   Runs the above-defined getdimensions function on each child
#   Create canvas for each child named after its objectid
#   Define image to be placed on canvas as child's object_location
    for index,child in enumerate(values['children']):
        infojson = child['info_json']
        height, width = getdimensions(infojson)
        canvasid = "https://digitalcollections.lib.iastate.edu/canvas/{}".format(child['objectid'])
        object_location = child['object_location']
        print(object_location)
        canvas = manifest.make_canvas(id=canvasid, height=height, width=width, label=child['title'])
        anno_page = canvas.add_image(image_url=object_location,
                                    
                                    anno_page_id="https://digitalcollections.lib.iastate.edu/canvas/{}".format(child['objectid'] + "/1"),
                                    anno_id="https://digitalcollections.lib.iastate.edu/canvas/{}".format(child['objectid'] + "/annotation/image"),
                                    format="image/jpg",
                                    height=height,
                                    width=width
                                    )
        
#   Saves the json file, prints the name of the file that has just been saved, and continues until all json files have been created.        
    with open('manifest-'+values['parent']['pid']+'.json', 'w') as f:
        print(manifest.json(indent=2),file=f)
#       Uncomment the below line for testing        
        #break