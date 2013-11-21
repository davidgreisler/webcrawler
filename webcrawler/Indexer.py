'''
Created on Nov 21, 2013

@author: prototyp
'''
from docutils.nodes import document

class Indexer(object):
    '''
    classdocs
    '''
    __siteContents = []
    __index = {}
    __stopWords = []

    def __init__(self,siteContents,stopWords):
        self.__siteContents = siteContents
        self.__stopWords = stopWords
        self.__index = {(u"hund",1) :[(u"d01",5)],
                        (u"katze",3):[(u"d03",2),(u"d04",2),(u"d02",10)],
                        (u"baer",2) :[(u"d01",2),(u"d03",5)]         
                        }
        
    #normalize words
    #remove stopwords
    
    def __checkDoc(self,document):
        for word in document[1]:
            indexKey = self.__findKey(word)
            if indexKey != None:
                print "gefunden "
                newIndexKey = (indexKey[0],indexKey[1]+1)
                newIndexValue = self.__index.pop(indexKey).append()
                pass
            else:
                print "nicht gefunden"
                #New index key Value anlegen
                pass
    
    def __findKey(self,searchKey):
        for key in self.__index:
            if key[0] == searchKey:
                return key
        return None    
        
    def buidlindex(self):
        testDoc = [(u"d01",[u"Bla",u"hund"]),
                   (u"d03",[u"blub",u"Bla",u"Katze"])]
        
        #print self.__siteContents
        #map(self.__checkDoc,testDoc)
        self.__siteContents = map(self.__nomalizeDocument,self.__siteContents)
        self.__siteContents = map(self.__groupDocumentWords,self.__siteContents)
        
        print '[%s]' % '\n '.join(map(str,self.__siteContents))
    
    def __groupDocumentWords(self,document):
        shrinkedDoc = []
        analysedWords = [] 
        word = ()
        for word in document[1]:
            if (word not in analysedWords and word not in self.__stopWords):
                shrinkedDoc.append((word,document[1].count(word))) 
                analysedWords.append(word)        
        return (document[0],shrinkedDoc)
        
        
        
    def __nomalizeDocument(self,document):
        print document[1]
        return (document[0],map(unicode.lower,document[1]))
            
        