from xml.dom import minidom

#import sys
#reload(sys)
#sys.setdefaultencoding("utf-8")  

xml = minidom.parse('feeds.xml')

feeds = xml.getElementsByTagName('feed')

for f in feeds:
    name = f.getElementsByTagName('name')[0].firstChild.nodeValue
    #name = f.getElementsByTagName('url')[0].firstChild.nodeValue
   
    
#inserindo um nodo    
root = xml.getElementsByTagName('feeds')[0]
feed = xml.createElement('feed')
name = xml.createElement('name')
namevalue = xml.createTextNode('nome do feed')
name.appendChild(namevalue)
feed.appendChild(name)
root.appendChild(feed)
print root

import codecs
filexml = codecs.open('feeds.xml','w', encoding="utf-8")
xmlcontent = xml.toprettyxml()
print xmlcontent
import re
text_re = re.compile('>\n\s+([^<>\s].*?)\n\s+</', re.DOTALL)    
pretty_xml = text_re.sub('>\g<1></', xmlcontent)
xml.writexml(filexml)
filexml.close()
