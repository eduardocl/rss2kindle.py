### rss2kindle.py

rss2kindle.py is a kindle periodical format generator from rss or atom feeds.

The feeds are downloaded and parsed using the greate library feedparser (https://pythonhosted.org/feedparser/) and for html manipulation, the Beautiful Soap library (http://www.crummy.com/software/BeautifulSoup/bs4/doc/). These two libs save me a huge amount of time.   


Before using:
  Download kindlegen from http://www.amazon.com/gp/feature.html?docId=1000765211
  and copy the executables for linux and mac to directory "amazon". Rename the
  kindlegen for mac to kindlegenmac.


In order to run type:

python rss2kindle.py

If you want to add a new feed edit the file feed.py adding the name and the feed link.
