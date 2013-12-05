"""
    main.py
    
    A simple search engine, developed within the scope of a course work for AKTINF2.
    
    Authors: David Greisler (s0531301), Paul Kitt (s0528516), Marc Lehmann(s0524790)
    
"""

from SearchEngine import SearchEngine

seedURLs = [ "http://mysql12.f4.htw-berlin.de/crawl/d01.html",
             "http://mysql12.f4.htw-berlin.de/crawl/d06.html",
             "http://mysql12.f4.htw-berlin.de/crawl/d08.html" ]

stopWords = [ 'd01', 'd02', 'd03', 'd04', 'd05', 'd06', 'd07', 'd08',  
              'a', 'also', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'do',
              'for', 'have', 'is', 'in', 'it', 'of', 'or', 'see', 'so',
              'that', 'the', 'this', 'to', 'we' ]

search = SearchEngine(stopwords = stopWords, seed_urls = seedURLs)

exit_string = "/quit"

print "Enter " + exit_string + " to end the program."
print

query = ""
while 1 == 1:
    query = raw_input("Search query: ");
    
    if query == exit_string:
        break;
    
    search.query(query);
    print
