# OSM Query Processor
from OSMPythonTools.overpass import Overpass, overpassQueryBuilder
from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.data import Data, dictRangeYears, ALL
from collections import OrderedDict
import re, pprint, time
import osm2geojson
import geojson
import geopandas as gpd

class OSMQueryResult:
    _geometry = None
    _overpass_query = None
    _overpass_json = None

    def __init__(self): pass
    def execute(self, query, timeFilter=None):
        # NOTE: Remove [out:json][timeout:25]; from query
        # TODO: Should we try/retry a few times based on cache or timeouts on big queries
        self._geometry = ""
        self._overpass_query = Overpass().query(query, timeout=100)
        self._overpass_json = self._overpass_query.toJSON()
        # json2shapes = osm2geojson.json2shapes(result.toJSON())
        return self

    def geojson(self):
        return osm2geojson.json2geojson(self._overpass_query.toJSON())

    def summary(self):
        geometry = None
        for elem in self._overpass_json['elements']:
            elem_type = elem.get("type")
            if elem_type and elem_type == "node":
                print(elem.get("tags"))
                # geometry = geojson.Point((elem.get("lon"), elem.get("lat")))
                # feature = geojson.Feature(id=elem['id'],
                #                           geometry=geometry,
                #                           properties=elem.get("tags"))

    def write(self):
        with open("response-latest.geojson", 'w') as outfile:
            geojson.dump(self.geojson(), outfile, indent=4)

    def geojson_nodes(self):
        features = []
        geometry = None
        for elem in self._overpass_json['elements']:
            elem_type = elem.get("type")
            if elem_type and elem_type == "node":
                geometry = geojson.Point((elem.get("lon"), elem.get("lat")))
                feature = geojson.Feature(id=elem['id'], geometry=geometry, properties=elem.get("tags"))
                features.append(feature)
        return geojson.FeatureCollection(features)

    def geojson_ways(self):
        t = self.geojson_nodes()
        all_nodes = gpd.GeoDataFrame(t['features'])
        features = []
        geometry = None
        for elem in self._overpass_json['elements']:
            elem_type = elem.get("type")
            if elem_type and elem_type == "way":
                coords = []
                for node_id in elem['nodes']:
                    pnt = all_nodes[all_nodes['id'] == node_id]['geometry'].iloc[0]
                    coords.append((pnt.x, pnt.y))
                geometry = geojson.LineString(coords)
                feature = geojson.Feature(id=elem['id'], geometry=geometry, properties=elem.get("tags"))
                features.append(feature)
        return geojson.FeatureCollection(features)
        # if json2shapes:
        #     shapes = []
        #     for shape_obj in json2shapes:
        #         shapes.append(shape_obj.get('shape'))
        #         # summarize the json..
        #         # - tag summary counts
        #         # - node/way/relation count

if __name__ == "__main__":

    # lat_max,lon_min,lat_min,lon_max = 47.617581, 7.606412, 47.586086, 7.668244
    # overpass_query = '''
    # (

    # way[highway=motorway]({lat_min}, {lon_min}, {lat_max}, {lon_max});
    # way[highway= trunk]({lat_min}, {lon_min}, {lat_max}, {lon_max});
    # way[highway=primary]({lat_min}, {lon_min}, {lat_max}, {lon_max});
    # way[highway=secondary]({lat_min}, {lon_min}, {lat_max}, {lon_max});
    # way[highway=tertiary]({lat_min}, {lon_min}, {lat_max}, {lon_max});
    # way[highway=unclassified]({lat_min}, {lon_min}, {lat_max}, {lon_max});
    # way[highway=residential]({lat_min}, {lon_min}, {lat_max}, {lon_max});
    # way[highway=service]({lat_min}, {lon_min}, {lat_max}, {lon_max});
    # way[highway=motorway_link]({lat_min}, {lon_min}, {lat_max}, {lon_max});
    # way[highway=trunk_link]({lat_min}, {lon_min}, {lat_max}, {lon_max});
    # way[highway=primary_link]({lat_min}, {lon_min}, {lat_max}, {lon_max});
    # way[highway=secondary_link]({lat_min}, {lon_min}, {lat_max}, {lon_max});
    # way[highway=tertiary_link]({lat_min}, {lon_min}, {lat_max}, {lon_max});
    # way[highway=unclassified_link]({lat_min}, {lon_min}, {lat_max}, {lon_max});
    # way[highway=residential_link]({lat_min}, {lon_min}, {lat_max}, {lon_max});
    # way[highway=service_link]({lat_min}, {lon_min}, {lat_max}, {lon_max});
    # way[highway=living_street]({lat_min}, {lon_min}, {lat_max}, {lon_max});
    # way[highway=track]({lat_min}, {lon_min}, {lat_max}, {lon_max});
    # way[highway=escape]({lat_min}, {lon_min}, {lat_max}, {lon_max});
    # way[highway=road]({lat_min}, {lon_min}, {lat_max}, {lon_max});
    # );
    # out body;
    # >;
    # out skel qt;
    # '''.format(lat_min=lat_min,
    #            lon_min=lon_min,
    #            lat_max=lat_max,
    #            lon_max=lon_max)

    overpass_query = """
    (
        node["brand:wikidata"="Q37158"]["amenity"="cafe"](40.69977176830021,-74.04047012329102,40.790679480243526,-73.9156723022461);
        way["brand:wikidata"="Q37158"]["amenity"="cafe"](40.69977176830021,-74.04047012329102,40.790679480243526,-73.9156723022461);
        relation["brand:wikidata"="Q37158"]["amenity"="cafe"](40.69977176830021,-74.04047012329102,40.790679480243526,-73.9156723022461);
    );
    out body;
    >;
    out skel qt;
    """

    result = OSMQueryResult().execute(overpass_query)
    print(result.summary())
    result.write()


# result = OSMQueryResult().execute("""
# (
#     node["brand:wikidata"="Q37158"]["amenity"="cafe"](40.69977176830021,-74.04047012329102,40.790679480243526,-73.9156723022461);
#     way["brand:wikidata"="Q37158"]["amenity"="cafe"](40.69977176830021,-74.04047012329102,40.790679480243526,-73.9156723022461);
#     relation["brand:wikidata"="Q37158"]["amenity"="cafe"](40.69977176830021,-74.04047012329102,40.790679480243526,-73.9156723022461);
# );
# out body;
# >;
# out skel qt;
# """)
# print(result.geojson_ways())


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
