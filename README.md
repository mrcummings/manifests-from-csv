# manifests-from-csv
generates IIIF manifests using a csv as input

## To use:
1. This script assumes that you have a metadata csv formatted to work with CollectionBuilder CSV. If you aren't already, you should become familiar with the required and suggested fields and their parameters. Read more here: https://collectionbuilder.github.io/cb-docs/docs/metadata/csv_metadata/
2. CB fields required for this script are: objectid, title, display_template, object_location
3. Non-CB fields required for this script are:
    - infojson: URL for the object's info.json file created from IIIF image API. Like object_location, leave blank if display_template value is "multiple".
    - parentid: if display_template value is "multiple," leave blank. If object is a child of a multiple parent, use the objectid of the parent as its parentid.
    - pid: unique identifier that is meaningful at the institution level (as opposed to objectid, which is probably only meaningful at the collection level)
4. Drop your metadata csv into this folder
5. Change "wpa_clean" in line 16 to the name of your csv
4. Run the program. Manifests named "manifest-{pid}.json" will populate in this folder.


## Things to know
- This script creates v3 manifests.
- If your csv includes the height and width (in pixels) of your objects, then you don't need the getdimensions function or the infojson field in your metadata. You may comment out lines 7-11 and define height and width in line 37 as values from your csv instead if you wish.
- For development purposes, you may wish to install the Live Server VSCode extension. Then you can use a local server address to use these manifests in your own project. 