
# OSM Query Processor
from OSMPythonTools.overpass import Overpass, overpassQueryBuilder
from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.data import Data, dictRangeYears, ALL
from collections import OrderedDict
import re, pprint

def osmQueryProcessor(query, timeFilter=None):
    # print(re.sub(r'(\/\*[\w\'\s\r\n\*]*\*\/)|(\/\/[\w\s\']*)|(\<![\-\-\s\w\>\/]*\>)', '', query))
    # Fetches current OpenStreetMap entities that match given tags in
    #   a given geographic area (e.g. using the Overpass API)
    # RETURN:
    # Computes statistics on the data including:
        # Quantity of entities
        # Quantity of users who created or modified entities
        # Change over time for above
    # Writes statistics to file in a standard data format
    # Writes entities to file in a standard geospatial data format (e.g. GeoJSON)
    # Upload file to S3 or other destination
    # OUTPUT: Config/MapModel
    # MapModel: {
    # - summaryDataLocations
    # - geoJSON map data
    # - summary data (# of entities, # of tags, aggregations, counts, etc.)
    # }

    if not query: raise Exception("Query needed")
    overpass = Overpass()
    result = overpass.query(query)
    pprint.pprint(result.toJSON())

if __name__ == "__main__":
    osmQueryProcessor("""
    (
        node["brand:wikidata"="Q37158"]["amenity"="cafe"](40.69977176830021,-74.04047012329102,40.790679480243526,-73.9156723022461);
        way["brand:wikidata"="Q37158"]["amenity"="cafe"](40.69977176830021,-74.04047012329102,40.790679480243526,-73.9156723022461);
        relation["brand:wikidata"="Q37158"]["amenity"="cafe"](40.69977176830021,-74.04047012329102,40.790679480243526,-73.9156723022461);
    );
    out body;
    >;
    out skel qt;
    """)
