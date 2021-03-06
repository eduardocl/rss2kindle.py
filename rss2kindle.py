# -*- coding: utf-8 -*-
__author__ = "Eduardo Lopes"
__email__ = "eduardocl@gmail.com"


import zipfile
import datetime
import xml.etree.ElementTree as ET
import cStringIO
import urllib2
import os
import platform
import imghdr
import codecs
  
import sys
reload(sys)
sys.setdefaultencoding("utf-8")  
  
from bs4 import BeautifulSoup


container_xml = """<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
"""

coverpage_tpl=""" <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
        <meta name="cover" content="true"/>
        <title>Cover</title>
        <style type="text/css" title="override_css">
            @page {padding: 0pt; margin:0pt}
            body { text-align: center; padding:0pt; margin: 0pt; }
        </style>
         <link rel="stylesheet" type="text/css" href="./styles.css">
    </head>
    <body>

      <h1>rss2kindle.py</h1>
      <h2> %(dateofday)s </h2>

        <div>
            <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1"
            width="100%%" height="100%%" viewBox="0 0 590 750" preserveAspectRatio="none">
                <image width="590" height="750" xlink:href="cover.jpg"/>
            </svg>
        </div>
    </body>
</html>
"""


content_opf = """<?xml version='1.0' encoding='utf-8'?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="uuid_id" version="2.0">
  <metadata xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
   xmlns:opf="http://www.idpf.org/2007/opf" xmlns:dcterms="http://purl.org/dc/terms/" 
   xmlns:dc="http://purl.org/dc/elements/1.1/">

    <dc:publisher>rss2kindle.py</dc:publisher>
    <dc:description> Generated by rss2kindle.py </dc:description>
    <dc:language>pt_BR</dc:language>
    <dc:creator opf:file-as="rss2kindle.py" opf:role="aut">rss2kindle.py</dc:creator>
    <dc:title>rss2kindle.py</dc:title>
    <meta name="cover" content="cover"/>
    <dc:date> %(generated_date)s </dc:date>
    <dc:contributor opf:role="bkp">rss2kindle.py</dc:contributor>
    <dc:identifier id="uuid_id" opf:scheme="uuid">72ebf8f1-9a52-4b8a-8013-cd5f54166b2a</dc:identifier>
    <meta name="rss2kindle:publication_type" content="periodical:unknown:Notícias"/>

     <x-metadata>
      <output content-type="application/x-mobipocket-subscription-magazine" encoding="utf-8"/>
    </x-metadata>

  </metadata>
    <item href="cover.jpg" id="cover" media-type="image/jpeg"/>
    <item id="epub.embedded.font" href="Tciaar.ttf" media-type="application/x-font-ttf"/>
    
     <manifest>

       <item href="coverpage.xhtml" id="coverpage" media-type="application/xhtml+xml"/>
       <item href="toc.ncx" id="tocncx" media-type="application/x-dtbncx+xml"/>
       <item href="contents.html" id="contents" media-type="application/xhtml+xml"/>

       %(items)s

     </manifest>

     <spine toc="tocncx">
       <itemref idref="coverpage"/>
       <itemref idref="contents"/>

       %(itemrefs)s

     </spine>

     <guide>
      <reference href="contents.html" type="toc" title="Table of Contents"/>
     </guide>

</package>
"""

manifest_item_tpl = """<item href="%(link)s" id="id%(id)s" media-type="%(mimetype)s"/>
"""
spine_item_tpl = """<itemref idref="id%(id)s"/>
"""


article_content_tpl = """<html>
<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
<link rel="stylesheet" type="text/css" href="./styles.css">
</head>
<body class="tciaar">
  <h1>%(title)s</h1><br/>
  <p style="font-size:8pt"> %(author)s </p><br/>
  <p style="font-size:8pt"> %(published)s </p><br/>
  %(content)s
  <p style="font-size:10pt">
    <i>%(footer)s</i>
  </p>
</body>
</html>
"""

contents_html_tpl = """<html>
  <head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
    <title>Table of Contents</title>
    <link rel="stylesheet" href="./styles.css">
  </head>
  <body class="tciaar">
    <h1>rss2kindle.py</h1>

    %(articles_links)s

  </body>
  </html>
"""

toc_ncx_tpl = """<?xml version='1.0' encoding='utf-8'?>
<ncx xmlns:mbp="http://mobipocket.com/ns/mbp" xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="eng">
  <head>
    <meta content="45112bf4-0a26-406d-8207-148c3350e36c" name="dtb:uid"/>
    <meta content="3" name="dtb:depth"/>
    <meta content="rss2kindle.py" name="dtb:generator"/>
    <meta content="0" name="dtb:totalPageCount"/>
    <meta content="0" name="dtb:maxPageNumber"/>
  </head>
  <docTitle>
    <text>RSS Feeds Generated by python</text>
  </docTitle>
  <navMap>

	 <navPoint playOrder="0" class="periodical" id="periodical">

		<navLabel>
		<text>Table of Contents</text>
		</navLabel>
		<content src="contents.html"/>

    %(navpoints)s

    </navPoint>

   </navMap>
</ncx>
"""

feed_nav_point_tpl = """
  <navPoint class="section" id="num_%(order)s" playOrder="%(order)s">
     <navLabel>
         <text>%(title)s</text>
     </navLabel>
     <content src="%(link)s"/>

        %(article_navpoints)s

   </navPoint>
"""

article_navpoint_tpl = """
      <navPoint class="article" id="num_%(order)s" playOrder="%(order)s">
          <navLabel>
            <text>%(article_title)s</text>
          </navLabel>
          <content src="%(article_link)s"/>
          <mbp:meta name="description"> %(description)s </mbp:meta>
          <mbp:meta name="author">%(author)s</mbp:meta>
        </navPoint>
"""

def inc(counter, amount=1):
  return counter + amount


def get_today():
    """Returns the current data formatted as d/m/y """
    hoje = datetime.date.today();
    return "{0}/{1}/{2}".format(hoje.day, hoje.month, hoje.year)


class Entry:
  def __init__(self, title, content, author, publishdate, description):
    self.title = title.encode("utf-8")
    self.content = content.encode("utf-8")
    self.author = author.encode("utf-8")
    self.publishdate = publishdate.encode("utf-8")
    self.description = description.encode("utf-8")

  def __repr__(self):
    return "Title: %s, filename: %s " % (self.title, self.filename)


class Feed:
	def __init__(self, name, url):
		self.name = name
		self.url = url
		self.entries = []

	def add_entry(self, entry):
		self.entries.append(entry)

	def __repr__(self):
		return "Feed: %s, url: %s, entries: %s" % (self.name, len(self.entries))


class Epub:
  def __init__(self):
    self.feeds = []
    self.images = []

  def save(self, filename="rss2kindle.epub"):
    epubfile = zipfile.ZipFile(filename, "w")
    epubfile.writestr("mimetype", "application/epub+zip")
    epubfile.writestr("META-INF/container.xml", container_xml)

    today = datetime.date.today()
    datestr = "{0}/{1}/{2}".format(today.day, today.month, today.year)
    epubfile.writestr("coverpage.xhtml", coverpage_tpl % {"dateofday": datestr})
    epubfile.write("cover.jpg")

    article_counter = 0
    
    os.system("rm -rf temp")
    os.system("mkdir temp")
    for feed in self.feeds:
      image_counter = 0  
      for entry in feed.entries:
        print "Downloading images for article:{0} [{1}]".format(entry.title, feed.name)
        html = BeautifulSoup(entry.content)
        images = html.find_all("img")
        #print "url", url
        #tokens = url.split("/")
        #feeder = "/".join(tokens[0:len(tokens)-1])

        for image in images:
            img_url = image['src']
            img_name = "{0}_image_{1}".format(feed.name,image_counter)
            img_name = img_name.replace(" ", "_")
            img_tmp_name = "temp/" + img_name
            try:
                f = open(img_tmp_name, "wb")
                f.write(urllib2.urlopen(img_url).read())
                f.close()
                imgtype = imghdr.what(img_tmp_name)
                #print imgtype
                img_tgt_name = "images/" + img_name + "." + imgtype
                epubfile.write("temp/" + img_name, img_tgt_name)
                image['src'] = img_tgt_name
                self.images.append(("image/" + imgtype, img_tgt_name))
                image_counter = inc(image_counter)
                #print img_url
            except:
                print "Error when trying to dowload images from", entry.title, feed.name
                continue
        
                   
        data = {'title': entry.title,
                'content': html,
                'author': entry.author,
                'published': entry.publishdate,
                'footer': 'generated by rss2kindle.py'
                }
                
        article = (article_content_tpl % data)
        epubfile.writestr("article_{0}.html".format(article_counter), article)
        article_counter = inc(article_counter)

    contentshmtl, contentopf, tocncx = self.__create_contents()
    epubfile.writestr("content.opf", contentopf)
    epubfile.writestr("contents.html", contentshmtl)
    epubfile.writestr("toc.ncx", tocncx)    
    os.system("rm -rf temp")    

  def __create_contents(self):
    id_counter = 0
    article_counter = 0
    play_order = 1
    spine_items = ""
    manifest_items = ""
    content_html_items = ""

    feed_navpoints_items = ""

    for feed in self.feeds:
        content_html_items = content_html_items + "<h4>{0}</h4>\n".format(feed.name)
        content_html_items = content_html_items + "<ul>\n";
        feed_play_order = play_order
        play_order = inc(play_order)
        article_navpoints_items = ""
        feed_link = "article_{0}.html".format(article_counter)
        for entry in feed.entries:
          data = {'link': "article_{0}.html".format(article_counter),
                  'id': id_counter,
                  "mimetype": "application/xhtml+xml"}

          manifest_items = manifest_items + (manifest_item_tpl % data)
          spine_items = spine_items + (spine_item_tpl % {"id":id_counter})

          content_html_items = content_html_items + \
                        "<li><a href='article_{0}.html'>{1}</a></li>\n" \
                          .format(article_counter, entry.title)

          description = entry.description.replace("&#8230;", "")
          description = description.replace("[", "")
          description = description.replace("]", "")
          description = description.replace("<", "")
          description = description.replace(">", "")
          description = description.replace("&", "")
          description = description.replace("#", "")
          description = description.replace("%", "")
          description = description.replace(";", "")

          article_navpoints_items = article_navpoints_items + \
                        (article_navpoint_tpl % {"article_title":entry.title, \
                                                 "article_link": "article_{0}.html".format(article_counter),
                                                 "order": play_order,
                                                 "description": description,
                                                 "author":entry.author})
          play_order = inc(play_order)
          article_counter = inc(article_counter)
          id_counter = inc(id_counter)

        content_html_items = content_html_items + "</ul>\n";
        feed_navpoints_items = feed_navpoints_items + \
                (feed_nav_point_tpl % {"order":feed_play_order, \
                                       "article_navpoints":article_navpoints_items, \
                                       "title": feed.name, \
                                       "link": feed_link})
                
    for image in self.images:
        mimetype = image[0]
        imgurl = image[1]
        data = {'link': imgurl,
                'id': id_counter,
                "mimetype": mimetype}
        manifest_items = manifest_items + (manifest_item_tpl % data)
        id_counter = inc(id_counter)        

    contenthtml = contents_html_tpl % ({'articles_links':content_html_items})
    contentopf = content_opf % ({"generated_date": get_today(), "items":manifest_items, "itemrefs":spine_items})
    tocncx = toc_ncx_tpl % ({"navpoints": feed_navpoints_items})
    return contenthtml, contentopf, tocncx





if __name__ == "__main__":

  import feedparser
  from feed import feeds
  
  epub = Epub()
  today = datetime.date.today()
  epubfile = "rss2kindle_{0}.epub".format(str(today.year)+str(today.month)+ str(today.day))

  for feed in feeds[0:2]:
    feedname = feed[0]
    url = feed[1]
    f = feedparser.parse(url)
    print "Fetching", feedname

    feedobj = Feed(feedname, url)
    any_content = False
    for entry in f.entries:
      if 'content' in entry:
        print "\t{0}...".format(entry.title[0:80].encode("utf-8"))
        any_content = True
        content = entry.content[0]['value']
       		
        if 'published' in entry:
          publishdate = entry.published
        else:
          publishdate = ""

        if 'description' in entry:
          description = entry.description
        else:
          description = ""

        if 'author' in entry:
          author = entry.author
        else:
          author = "Unknown"

        entryobj = Entry(entry.title, content, author, publishdate, description)
        feedobj.entries.append(entryobj)
    if not any_content:
       print feedname, "has not valid content url:", url
    else:
       epub.feeds.append(feedobj)


  epub.save(epubfile)

  if platform.system() == "Darwin":
      os.system("./amazon/kindlegenmac -c2 {0} ".format(epubfile) )
  if platform.system() == "Linux":
      os.system("./amazon/kindlegen -c2 {0}".format(epubfile))

