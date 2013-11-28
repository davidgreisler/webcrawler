"""
    SearchEngine.py
    
    Defines a class SearchEngine which contains the main search logic for the search engine
    program.
    
"""

from Crawler import Crawler
from Indexer import Indexer
from PageRank import Computer

class SearchEngine(object):
    """
    Manages crawler, indexer and page rank computer and provides a convenient method for querying
    the search index.
    
    The class is initialized with a set of seed URLs for the crawler and a list of stop words for
    the indexer. It will then run the crawler, indexer and page rank computer and provides a ready-
    to-use search index which can be queried using query().
    
    """

    # Words that are filtered out before term/document frequency calculation.
    _stopwords = []
    
    # Seed URLs for the web crawler, these are the URLs which the web crawler uses to start 
    # crawling.
    _seed_urls = []
    
    # The web crawler, starts with the seed URLs and build up the web graph and extracts terms from
    # the web sites.
    _crawler = None
    
    # Computes the page ranks for every website using the web graph.
    _page_rank_computer = None
    
    # The indexer that creates the term frequency and document frequency indexes.
    _indexer = None
    
    # The webgraph is a dictionary mapping websites to a list of outlinks (websites linked to by
    # that website).
    _webgraph = {}
    
    # A dictionary mapping websites to extracted terms.
    _extracted_terms = {}
    
    # A dictionary mapping websites to computed page ranks.
    _page_ranks = {}
    
    # A dictionary mapping terms to the number of documents they occur in.
    _document_frequency = {}
    
    # A dictionary mapping terms to a list of tuples of documents and the number of times the term
    # occurs in that document, e.g. { 'term' : [('document', 123), ('anotherdocument', 1234)] }
    _term_frequency = {}
    
    def __init__(self, seed_urls, stopwords = None):
        """
        Initializes the search engine with the given seed urls and the given stop words and does the
        crawling, computes page ranks and builds up the index. 
        
        Args:
            seed_urls: The seed urls for the crawler.
            stopwords: The stop words for the indexer.
        
        """
        if stopwords is not None:
            self._stopwords = stopwords
        self._seed_urls = seed_urls
        
        self._do_crawling()
        self._compute_page_ranks()
        self._build_index()
        
    def query(self, query):
        """
        Searches the index for every term (separated by whitespace) and prints a list of documents
        in which all terms occur.
        
        Args:
            query: The search query, terms separated by whitespace (all terms will be converted to
                   lowercase).
        
        """
        terms = query.lower().split()
        
        if not terms:
            print "No search terms entered."
            return
        
        documents = []
        
        for term in terms:
            new_document_list = []
            term_documents = []
            
            if term in self._term_frequency:
                for document_and_count in self._term_frequency[term]:
                    term_documents.append(document_and_count[0])
            
            if not documents:
                # First search term, fill list with all documents the term occurs in or break if
                # the term isn't found (we are looking for a document that contains all terms).
                if not term_documents:
                    break
                else:
                    new_document_list = term_documents
            else:
                # Another search term, only keep those documents that contain both the former terms
                # and the current one.
                for document in documents:
                    if document in term_documents:
                        new_document_list.append(document)
            
            documents = new_document_list
        
        print 
        
        if not documents:
            print "No documents match your search terms (\"" + str(terms) + "\")."
            return
        
        print "Results:"
        for document in sorted(documents, key = lambda url : self._page_ranks[url], reverse = True):
            print "  - " + document + " (PageRank: " + str(self._page_ranks[document]) + ")"
    
    def _do_crawling(self):
        """
        Initializes the crawler with the seed urls and starts crawling, then stores the resulting
        webgraph and the extracted terms in the attributes.
        
        """
        
        print "Starting crawler ..."
        print "  Seed URLs: "
        
        for url in self._seed_urls:
            print "   - " + url
        
        self._crawler = Crawler(self._seed_urls)
        results = self._crawler.startCrawling()
        
        self._webgraph = results[0]
        self._extracted_terms = results[1]
        
        #print "  Web graph: "
        #for url in self._webgraph.keys():
        #    print "   - " + url
        #    for outlink in self._webgraph[url]:
        #        print "     -> " + outlink
        
        #print "  Extracted terms: "
        #for website in self._extracted_terms:
        #    print "   - " + website[0] + ": "
        #    print ', '.join(str(token) for token in website[1])
        
        print "Crawler finished."
        print
        
    def _compute_page_ranks(self):
        """
        Initializes the page rank computer with the webgraph and computes the page ranks.
        
        """
        print "Computing page ranks ..."

        self._page_rank_computer = Computer(self._webgraph)
        self._page_rank_computer.compute()
        self._page_ranks = self._page_rank_computer.page_ranks
        
        print "  Page ranks:"
        
        result_sum = 0
        for website in sorted(self._page_ranks.keys()):
            result_sum += self._page_ranks[website]
            
            print "   - " + website + ": " + str(self._page_ranks[website])
        
        #print
        #print "  Sum: " + str(result_sum)
        
        print "Page ranks computed."
        print
        
    def _build_index(self):
        """
        Takes the extracted terms and stop words and builds up the term frequency index and the 
        document frequency index.
        
        """
        print "Building index ..."
    
        self._indexer = Indexer(self._extracted_terms, self._stopwords)
        index = self._indexer.buidlindex()
        
        self._document_frequency = index[0]
        self._term_frequency = index[1]
        
        #print "  Document index:"
        #for term in sorted(self._document_frequency):
        #    print "   - " + term + ": " + str(self._document_frequency[term]) + " times"
        
        #print
        #print "  Term frequency:"
        #for term in sorted(self._term_frequency):
        #    print "   - " + term + ":"
        #    for document_and_count in self._term_frequency[term]:
        #        print "      - " + document_and_count[0] + ": " + str(document_and_count[1]) + " times"
        
        print "Index build up."
        