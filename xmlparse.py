
import sys
reload(sys)
sys.setdefaultencoding("utf-8")  

from xml.etree.ElementTree import ElementTree as ET
from xml.etree.ElementTree import parse
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import Element

import codecs

input_xml = codecs.open('feeds.xml','r', encoding="utf-8")
tree = parse(input_xml)
root = tree.getroot()


def indent(elem, level=0):
    i = "\n" + level*"  "
    if elem is not None:
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def add_feed(feedname, feedurl):
    feed = SubElement(root, "feed")
    name = SubElement(feed, "name")
    name.text = feedname
    url = SubElement(feed, "url")
    url.text = feedurl


add_feed("feed 1", "link 1")
add_feed("feed 2", "link 2")
add_feed("feed 3", "link 3")

indent(root)
tree.write("resultado.xml", encoding="utf-8")


