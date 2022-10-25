
# OSM Query Processor

from OSMPythonTools.overpass import Overpass, overpassQueryBuilder
from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.data import Data, dictRangeYears, ALL
from collections import OrderedDict
import re


def osmQuerProcessorById(queryId):
    pass

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
    # resultElements = result.elements()[0]
    print(result)
    print(type(result), dir(result))
    print(result.toJSON())

    print(result.countNodes())
    print(result.nodes())

    print(result.countRelations())
    print(result.relations())

    print(result.countElements())
    print(result.elements())

    print(result.countAreas())
    print(result.areas())

    print(result.countWays())
    print(result.ways())
    # <class 'OSMPythonTools.overpass.OverpassResult'> ['_OverpassResult__count', '_OverpassResult__elementsOfType', '_OverpassResult__get', '_OverpassResult__get2', '_Response__get', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_cacheMetadata', '_elements', '_json', '_queryString', 'areas', 'cacheTimestamp', 'cacheVersion', 'copyright', 'countAreas', 'countElements', 'countNodes', 'countRelations', 'countWays', 'elements', 'generator', 'isValid', 'nodes', 'queryString', 'relations', 'remark', 'timestamp_area_base', 'timestamp_osm_base', 'toJSON', 'version', 'ways']
    # print(resultElements)
    # print(resultElements.tag('name:en'))



# def osmQueryProcessorTesting(query, timeFilter=None):
#     if not query: raise Exception("Query needed")
#     overpass = Overpass()
#     result = overpass.query(query)
#     stephansdom = result.elements()[0]
#     print(result)
#     print(stephansdom)
#     print(stephansdom.tag('name:en'))
#     # # "Saint Stephen's Cathedral"
#     # print('%s %s, %s %s' % (stephansdom.tag('addr:street'), stephansdom.tag('addr:housenumber'), stephansdom.tag('addr:postcode'), stephansdom.tag('addr:city')))
#     # # 'Stephansplatz 3, 1010 Wien'
#     # print(stephansdom.tag('building'))
#     # # 'cathedral'
#     # print(stephansdom.tag('denomination'))
#     # # 'catholic'


#     nominatim = Nominatim()
#     areaId = nominatim.query('New York, NY').areaId()
#     print(areaId)


#     # overpass = Overpass()
#     query = overpassQueryBuilder(area=areaId, elementType='node', selector='"natural"="tree"', out='count')
#     result = overpass.query(query)
#     print(result)
#     print(result.countElements())
#     # 137830

#     # result = overpass.query(query, date='2013-01-01T00:00:00Z', timeout=60)
#     # print(result.countElements())
#     # # 127689

#     query = overpassQueryBuilder(area=areaId, elementType=['way', 'relation'], selector='"natural"="water"', includeGeometry=True)
#     result = overpass.query(query)
#     print(result)


#     firstElement = result.elements()[0]
#     print(firstElement.geometry())
#     # {"coordinates": [[[16.498671, 48.27628], [16.4991, 48.276345], ... ]], "type": "Polygon"}


#     # dimensions = OrderedDict([
#     #     ('year', dictRangeYears(2022, 2017.5, 1)),
#     #     ('city', OrderedDict({
#     #         'berlin': 'Berlin, Germany',
#     #         'paris': 'Paris, France',
#     #         'vienna': 'Vienna, Austria',
#     #     })),
#     # ])


#     # overpass = Overpass()
#     # def fetch(year, city):
#     #     areaId = nominatim.query(city).areaId()
#     #     query = overpassQueryBuilder(area=areaId, elementType='node', selector='"natural"="tree"', out='count')
#     #     return overpass.query(query, date=year, timeout=60).countElements()
#     # data = Data(fetch, dimensions)
#     # print(data)

#     # data.plot(city=ALL, filename='example4.png')


#     # print(data.select(city=ALL).getCSV())
#     # # year,berlin,paris,vienna
#     # # 2013.0,10180,1936,127689
#     # # 2014.0,17971,26905,128905
#     # # 2015.0,28277,90599,130278
#     # # 2016.0,86769,103172,132293
#     # # 2017.0,108432,103246,134616

#     pass


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
    pass
