'''
Created on Nov 21, 2013

@author: prototyp
'''
from docutils.nodes import document
from pprint import pprint

class Indexer(object):
    '''
    classdocs
    '''
    __siteContents = {}
    __indexDf = {} #{u"term":documentFrequency,...}
    __indexTf = {} #{u"term":[(u"document",termFrequency),(u"document",termFrequency),...}
    __stopWords = []

    def __init__(self,siteContents,stopWords):
        self.__siteContents = siteContents
        self.__stopWords = stopWords

    """
    adds all term of a given document to the index
    if a term is the index the document frequency will be increased in member __indexDf and the document and term frequency will be added to __indexTf 
    if the term is not in the index a new entry will be made
    arguments: document (u'd01', [(u'term', termFrequency), (u'term', termFrequency)], ...)
    """
    def __addDoctoIndex(self,document):
        #print "Document %s"% (document,)
        #pprint (self.__indexDf)
        #pprint (self.__indexTf)
        
        for wordTfCount in document[1]:
            #print "word %s"  %(word,)   
            
            if wordTfCount[0] in self.__indexDf:
                self.__indexDf[wordTfCount[0]] = self.__indexDf[wordTfCount[0]] +1
                self.__indexTf[wordTfCount[0]].append((document[0],wordTfCount[1]))
                #print "gefunden " + wordTfCount[0] 
            else:
                #print "nicht gefunden "+ wordTfCount[0]
                self.__indexDf.update({wordTfCount[0]:1})
                self.__indexTf.update({wordTfCount[0]:[(document[0],wordTfCount[1])]})
    
    """
    builds up the indexes for documents frequency and the index for the documents and term frequency of all terms 
    """
    def buidlindex(self):        
        self.__siteContents = map(self.__nomalizeDocument,self.__siteContents)
        self.__siteContents = map(self.__groupDocumentWords,self.__siteContents)
        #print '[%s]' % '\n '.join(map(str,self.__siteContents))
        map(self.__addDoctoIndex,self.__siteContents)
        return (self.__indexDf,self.__indexTf)

        
    """
    Group all similiar words and counts them
    arguments: the document
    """
    def __groupDocumentWords(self,document): #mapReduce impl
        shrinkedDoc = []
        analysedWords = [] 
        word = ()
        for word in document[1]:
            if (word not in analysedWords and word not in self.__stopWords):
                shrinkedDoc.append((word,document[1].count(word))) 
                analysedWords.append(word)        
        return (document[0],shrinkedDoc)
        
       
    """
    Nomalises all words of a given document
    Normalisation: make each term of the document to lower case
    arguments: the document
    """    
    def __nomalizeDocument(self,document):
        return (document[0],map(unicode.lower,document[1]))
            
        