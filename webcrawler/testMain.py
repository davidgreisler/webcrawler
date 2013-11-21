'''
Created on Nov 19, 2013

@author: prototyp
'''
from Crawler import Crawler
from Indexer import Indexer

if __name__ == '__main__':
    seedURLS = ["http://mysql12.f4.htw-berlin.de/crawl/d01.html","http://mysql12.f4.htw-berlin.de/crawl/d06.html","http://mysql12.f4.htw-berlin.de/crawl/d08.html"]
    crawler = Crawler(seedURLS)
    results = crawler.startCrawling()
    #print '[%s]' % '\n '.join(map(str,results[0]))
    print '[%s]' % '\n '.join(map(str,results[1]))
    stopWords = ['d01', 'd02', 'd03', 'd04', 'd05', 'd06', 'd07', 'd08',  
'a', 'also', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'do'
'for', 'have', 'is', 'in', 'it', 'of', 'or', 'see', 'so',
'that', 'the', 'this', 'to', 'we']
    #indexer = Indexer(results[1],stopWords)
    #indexer.buidlindex()