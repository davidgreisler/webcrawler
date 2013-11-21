'''
Created on Nov 19, 2013

@author: prototyp
'''

import urllib2
import string
import re
from bs4  import BeautifulSoup
from Frontier import *


class Crawler:
    '''
    classdocs
    '''
    seedUrls =[""]
    webGrapg = []
    siteContents = []
    frontier = None
    soup = None
    
    baseURL = "http://mysql12.f4.htw-berlin.de/crawl/" # base url erstellen durch urlparse
    
    def __init__(self,seedUrls):
        self.frontier = Frontier(seedUrls)
        
    def startCrawling(self):
        node = self.frontier.getNode()
        
        while(node!=""):
            self.__downloadPage(node)
            node = self.frontier.getNode()
        return (self.webGrapg,self.siteContents)
        
  
    # download via urlib2
    def __downloadPage(self,seedUrl):
        response = urllib2.urlopen(seedUrl)  # TODO catch HTTPError urllib2.HTTPError: HTTP Error 404: Not Found
        #print response.info()
        html = response.read()
        self.soup = BeautifulSoup(html)                                  #get the html soup
        self.__getLinksFromPage(seedUrl)
        self.__getTextFromPage(seedUrl)
    
        response.close()  # best practice to close the fi
        
    def __getLinksFromPage(self,seedUrl):
        links = []
        #print seedUrl                                                  #
        for link in self.soup.find_all('a'):
            link = self.__validateUrl(seedUrl, link.get('href'))     
            links.append(link)
            self.frontier.setNode(link)
        self.webGrapg.append((seedUrl,links))
        
        #print '[%s]' % '\n '.join(map(str,links))
        
    def __getTextFromPage(self,seedUrl):
        [s.extract() for s in self.soup('a')] #extract all <a> link tags
        bodyContent = self.soup.body.get_text()
        regex = re.compile('[%s]' % re.escape(string.punctuation)) # building regex obj on punctuation
        words = regex.sub(" ",bodyContent).split()                 #replacing punctuation with whitespace and split into single words
        words = map(unicode.lower,words)
        self.siteContents.append((seedUrl,words))
        #print '[%s]' % '\n '.join(map(str,words))
        
    def __validateUrl(self,seedUrl,url):
        return "http://mysql12.f4.htw-berlin.de/crawl/"+url #TODO extract base url if missing
        