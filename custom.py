# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")  

import feedparser
import urllib2

from rss2kindle import *


def parse_midia_sem_mascara(url):
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	response = opener.open(url)
	content = response.read()
	html = BeautifulSoup(content)
	article_content = html.find("div", id="content_container")
	#print article_content
	ptags = BeautifulSoup(str(article_content))
	c = ptags.find_all('p')
	print c
	#print article_content	


feeds = [("MSM", "http://feeds.feedburner.com/midiasemmascara", parse_midia_sem_mascara)]



def create_kindle_periodical(feeds):
  ''' Cria um arquivo epub e mobi para cada feed fornecido '''
  if feeds:
    epub = Epub()
    today = datetime.date.today()
    epubfile = "rss2kindle-custom_{0}.epub".format(str(today.year)+str(today.month)+ str(today.day))
  
    for feed in feeds:
      feedname = feed[0]
      url = feed[1]
      f = feedparser.parse(url)
      print "Fetching", feedname
      feedobj = Feed(feedname, url)
      for entry in f.entries:
		  try:	
			print entry.id
			opener = urllib2.build_opener()
			opener.addheaders = [('User-agent', 'Mozilla/5.0')]
			response = opener.open(entry.link)
			content = response.read()
			description = entry.summary_detail['value']
			publishdate = entry.published
			author = "Unknown"
			entryobj = Entry(entry.title, content, author, publishdate, description)
			feedobj.entries.append(entryobj)
		  except Exception, e:
			print "{0} could not be downloaded".format(entry.title)
			print e
      epub.feeds.append(feedobj)	
    
    epub.save(epubfile)

    if platform.system() == "Darwin":
      os.system("./amazon/kindlegenmac -c2 {0} ".format(epubfile) )
    if platform.system() == "Linux":
      os.system("./amazon/kindlegen -c2 {0}".format(epubfile))
      
#create_kindle_periodical(feeds)      
parse_midia_sem_mascara()
