# -*- coding: utf-8 -*-
__author__ = "Eduardo Lopes"
__email__ = "eduardocl@gmail.com"

from bs4 import BeautifulSoup

import os
import xml.etree.ElementTree as ET

feeds = [
        ("Weekend Nerd",        "http://weekendnerd.wordpress.com/feed/"),
        ('Code Geeks',          'http://feeds.feedburner.com/JavaCodeGeeks'),
        ("Le Gorafi",           "http://www.legorafi.fr/feed"),
        ("Reinaldo Azevedo",    "http://veja.abril.com.br/blog/reinaldo/feed/"),
        ("Notalatina",          "http://notalatina.blogspot.com/feeds/posts/default"),
        ("Felipe Moura Brasil", "http://veja.abril.com.br/blog/felipe-moura-brasil/feed/"),
        ("Rodrigo Constantino", "http://veja.abril.com.br/blog/rodrigo-constantino/feed/"),
        ("Ordem Livre",         "http://ordemlivre.org/feed"),
        ("Reaçonaria",          "http://reaconaria.org/feed/"),
        ("Implicante",          "http://www.implicante.org/feed/"),
        ("The Daily WTF",       "http://syndication.thedailywtf.com/TheDailyWtf"),
		("rfi",					"http://www.rfi.fr/radiofr/podcast/rss_apprendre_francais.xml"),
        ("Daily Galaxy",        "http://www.dailygalaxy.com/my_weblog/rss.xml"),
        ("Zero Hora",           "http://zerohora.clicrbs.com.br/rs/rss/"),
		("Akita on Rails",      "http://feeds.feedburner.com/AkitaOnRails")]




class Feed:
    def __init__(self, xmlfile):
        self.feeds = []
        if os.path.isfile(xmlfile):
            self.xmlfile = ET.parse(xmlfile)
            root = self.xmlfile.getroot()
            for children in root:
                name = children[0].text
                url = children[1].text
                self.feeds.append((name,url))

    def get_feeds(self):
        return self.feeds

    def add_feeds(self, name, url):
        pass

    def save_feeds(self):
        pass

    def print_feeds(self):
        for i,feed in enumerate(self.feeds):
            print i, feed[0]

if __name__ == "__main__":
    feed = Feed("feeds.xml")
    print feed.get_feeds()
    feed.print_feeds()
