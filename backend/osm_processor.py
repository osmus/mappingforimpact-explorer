# OSM Query Processor
from OSMPythonTools.overpass import Overpass, overpassQueryBuilder
from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.api import Api
from OSMPythonTools.data import Data, dictRangeYears, ALL
from collections import OrderedDict, defaultdict
import re, pprint, time
import osm2geojson
import geojson
import geopandas as gpd
from cachetools import LRUCache, cachedmethod
from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring
import xml.etree.ElementTree as ET

cachesize = 1000


class OSMService:
    _cache = LRUCache(maxsize=cachesize)
    _geometry = None
    _overpass_query = None
    _overpass_json = None

    def __init__(self):
        pass

    @cachedmethod(lambda self: self._cache)
    def osmByIdSummary(self, type, id):
        tags = {}
        properties = {}
        api = Api()
        node = api.query('%s/%s' % (str(type), str(id)))  # 'way/270883815'
        root = ET.fromstring(node.toXML())
        # print(node.toXML())
        root_way = root.find("way")
        root_node = root.find("node")
        root_relation = root.find("relation")
        if root_way: properties = root_way.attrib
        if root_node: properties = root_node.attrib
        if root_relation: properties = root_relation.attrib
        for elem in root.findall('.//way/tag'):
            tags[elem.get('k')] = elem.get('v')
        for elem in root.findall('.//node/tag'):
            tags[elem.get('k')] = elem.get('v')
        for elem in root.findall('.//relation/tag'):
            tags[elem.get('k')] = elem.get('v')
        return dict(tags=tags, properties=properties)

    @cachedmethod(lambda self: self._cache)
    def execute(self, query, timeFilter=None):
        # NOTE: Remove [out:json][timeout:25]; from query
        # NOTE: Should we try/retry a few times based on cache or timeouts on big queries
        self._geometry = ""
        self._overpass_query = Overpass().query(query,
                                                shallow=False,
                                                timeout=100)
        self._overpass_json = self._overpass_query.toJSON()
        # json2shapes = osm2geojson.json2shapes(result.toJSON())
        return self

    def geojson(self):
        return osm2geojson.json2geojson(self._overpass_query.toJSON())

    def summary(self):
        summary = {
            "total_element_count": 0,  # Quantity of entities
            "total_way_count": 0,
            "total_node_count": 0,
            "total_relation_count": 0,
            # Quantity of users who created or modified entities
            "total_user_modified_count": 0,
            "user_modified_count": defaultdict(int)
            # Change over time for above
        }
        merged_tags = defaultdict(list)
        merged_elements = defaultdict(list)
        for elem in self._overpass_json['elements']:
            elem_type = elem.get("type")
            elem_id = elem.get("id")
            lookup = self.osmByIdSummary(elem_type, elem_id)
            summary["total_element_count"] += 1
            user = lookup["properties"].get("user", None)
            if user:
                summary["total_user_modified_count"] += 1
                summary["user_modified_count"][user] += 1
            summary["total_%s_count" % (elem_type)] += 1
            if elem.get("tags"):
                for k, v in elem.get("tags").items():
                    if v not in merged_tags[k]:
                        merged_tags[k].append(v)
                    merged_elements[str("=".join([k, v]))].append(
                        str("%s/%s" % (elem_type, elem_id)))
        return dict(
            summary=dict(summary),
            merged_tags=dict(merged_tags),
            merged_elements=dict(merged_elements),
        )

    def write(self):
        with open("osm-response-latest.geojson", 'w') as outfile:
            geojson.dump(self.geojson(), outfile, indent=4)
        with open("osm-response-summary.json", 'w') as outfile:
            geojson.dump(self.summary(), outfile, indent=4)

    def geojson_nodes(self):
        features = []
        geometry = None
        for elem in self._overpass_json['elements']:
            elem_type = elem.get("type")
            if elem_type and elem_type == "node":
                geometry = geojson.Point((elem.get("lon"), elem.get("lat")))
                feature = geojson.Feature(id=elem['id'],
                                          geometry=geometry,
                                          properties=elem.get("tags"))
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
                    pnt = all_nodes[all_nodes['id'] ==
                                    node_id]['geometry'].iloc[0]
                    coords.append((pnt.x, pnt.y))
                geometry = geojson.LineString(coords)
                feature = geojson.Feature(id=elem['id'],
                                          geometry=geometry,
                                          properties=elem.get("tags"))
                features.append(feature)
        return geojson.FeatureCollection(features)


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
        relation["brand:wikidata"="Q37158"]["amenity"="cafe"](40.69977176830021,-74.04047012329102,40.790679480243526,-73.9156723022461);
        way["brand:wikidata"="Q37158"]["amenity"="cafe"](40.69977176830021,-74.04047012329102,40.790679480243526,-73.9156723022461);
    );
    out body;
    >;
    out skel qt;
    """
    # print(overpass_query)
    result = OSMService().execute(overpass_query)
    result.write()
    # print(result.summary())