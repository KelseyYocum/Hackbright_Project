from pyquery import PyQuery as pq
from lxml import etree
import urllib
import requests

# mirror path http://thetvdb.com
# http://thetvdb.com/data/series/121361/default/1/1
# where d is a xml doc
# series banner http://thetvdb.com/banners/graphical/121361-g19.jpg
# episode img http://thetvdb.com/banners/episodes/121361/3254641.jpg
# search http://thetvdb.com/api/GetSeries.php?seriesname=<seriesname>

r = requests.get('http://thetvdb.com/data/series/121361/default/1/1')
print 'r', r
xml_doc = r.text
xml_doc = xml_doc.encode("utf-8")

pyQ = pq(xml_doc, parser = "xml")

#print pyQ("Writer").text().split('|')
#print pyQ("Episode").eq(5).find('FirstAired')
print pyQ('SeriesName')



def parser(external_series_id):
    r = requests.get('http://thetvdb.com/data/series/'+external_series_id+'/all/')
    xml_doc = r.text
    xml_doc = xml_doc.encode('utf-8')
    pyQ = pq(xml_doc, parser = 'xml')

    return pyQ


