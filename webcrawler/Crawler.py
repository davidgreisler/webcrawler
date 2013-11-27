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
    __webGrapg = {}
    __siteContents = []
    ____frontier = None
    __soup = None
    
    baseURL = "http://mysql12.f4.htw-berlin.de/crawl/" # base url erstellen durch urlparse
    
    def __init__(self,seedUrls):
        self.__frontier = Frontier(seedUrls)
        
    def startCrawling(self):
        node = self.__frontier.getNode()
        
        while(node!=""):
            self.__downloadPage(node)
            node = self.__frontier.getNode()
        return (self.__webGrapg,self.__siteContents)
        
  
    # download via urlib2
    """
    Download webpage to given Url via urllib2 and processes it with BeautifulSoup. After text and links will be extracted
    """
    def __downloadPage(self,seedUrl):
        response = urllib2.urlopen(seedUrl)  # TODO catch HTTPError urllib2.HTTPError: HTTP Error 404: Not Found
        #print response.info()
        html = response.read()
        self.__soup = BeautifulSoup(html)                                  #get the html soup
        self.__getLinksFromPage(seedUrl)
        self.__getTextFromPage(seedUrl)
    
        response.close()  # best practice to close the fi
    """
    Extract all URLs from a with BeatifulSoup processed webpage and add them to the webgraph dictionary
    Found links will be added to the frontier
    argument The URL of the page from which the links should be extracted
    """    
    def __getLinksFromPage(self,seedUrl):
        links = []                                               #
        for link in self.__soup.find_all('a'):
            link = self.__validateUrl(seedUrl, link.get('href'))     
            links.append(link)
            self.__frontier.setNode(link)
        self.__webGrapg.update({seedUrl:links})         
        #print '[%s]' % '\n '.join(map(str,links))
    """
    Extract all text from a with BeatifulSoup processed webpage and add them to the siteContent dictionary
    argument The URL of the page from which the links should be extracted
    """   
    def __getTextFromPage(self,seedUrl):
        [s.extract() for s in self.__soup('a')] #extract all <a> link tags
        bodyContent = self.__soup.body.get_text()
        regex = re.compile('[%s]' % re.escape(string.punctuation)) # building regex obj on punctuation
        words = regex.sub(" ",bodyContent).split()                 #replacing punctuation with whitespace and split into single words
        #self.__siteContents.update({seedUrl:words})
        self.__siteContents.append((seedUrl,words))
        #print '[%s]' % '\n '.join(map(str,words))
        
    def __validateUrl(self,seedUrl,url):
        return "http://mysql12.f4.htw-berlin.de/crawl/"+url #TODO extract base url if missing
        