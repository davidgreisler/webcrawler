"""
    PageRank.py
    
    This module contains a Computer class that computes page ranks for every website in a given
    webgraph.
    
"""

class Computer(object):
    """
    The page rank computer takes a webgraph and computes the page rank for every website in the 
    graph.
    
    The page ranks of the websites in a given webgraph are calculated as follows:
    
        1. Assume a page rank of 1 / number of websites in the webgraph for all websites.
        
        2. For every website W in the webgraph, do:
            2.1. For every backlink B (a website that has a link to W), divide the
                 page rank of B through the number of outlinks of B. The sum of 
                 the results is the "backlink part".
            2.2. For every dangling website D (a website with no outlinks), divide the page rank
                 of D through the number of websites in the webgraph. The sum of the results is the 
                 "dangling websites part". 
            2.3. Calculate the page rank using the formula:
                 
                     new rank = dampening factor * (backlink part + dangling websites part) +
                                teleportation rate / number of websites in the webgraph
           
           After new page ranks are calculated for every website, replace the old page ranks with 
           the new page ranks.                
        
        3. Repeat step 2 until the sum of the differences between the old and new page ranks 
           is lower than the termination threshold.
           
    The dampening factor is the probability that an imaginary user surfing the webgraph will switch
    to another website by clicking on a link. The teleportation rate is the probability that he/she
    will switch to a random website (e.g. through a bookmark or by entering an URL in the 
    address bar of his/her browser). The teleportation rate is the result of subtracting the 
    dampening factor from 1.
    
    The default dampening factor is 0.9.
    
    Usage example:
    
        computer = PageRank.Computer({ 'A' : [ 'B', 'C' ], 'B' : [], 'C': [ 'A', 'B' ] })
        computer.compute()
        print computer.page_ranks
    
    """
    
    # The webgraph is a dictionary mapping websites to a list of outlinks (websites linked to by
    # that website).  
    _webgraph = {}
    
    # A dictionary mapping websites to a list of backlinks (websites that link to that website).
    _backlinks = {}
    
    # A dictionary mapping websites to computed page ranks.
    _pageranks = {}
    
    # The probability that an imaginary user surfing the webgraph will switch to another website by
    # clicking on a link.
    _dampening_factor = 0.9
    
    def __init__(self, webgraph = None):
        """
        Creates a new page rank computer using the given webgraph or an empty webgraph if none
        is given.
        
        Args:
            webgraph: The webgraph to use.
        
        """
        if webgraph is None:
            webgraph = {}
        
        self.webgraph = webgraph
    
    @property
    def dampening_factor(self):
        """
        Returns the currently used dampening factor.
        
        """
        return self._dampening_factor
    
    @dampening_factor.setter
    def dampening_factor(self, new_dampening_factor):
        """
        Sets the new dampening factor to the given one.
        
        Args:
            new_dampening_factor: The new dampening factor, must be 0 <= dampening factor <= 1.
        
        """
        
        if new_dampening_factor < 0 or new_dampening_factor > 1:
            raise "Dampening factor must be >= 0 and <= 1."
        
        self._dampening_factor = new_dampening_factor
    
    @property
    def webgraph(self):
        """
        Returns the currently used webgraph.
        
        """
        return self._webgraph
    
    @webgraph.setter
    def webgraph(self, new_webgraph):
        """
        Sets the webgraph to the given one and resets pageranks.
        
        Args:
            new_webgraph: The new webgraph.
        
        """
        self._webgraph = new_webgraph
        self._backlinks = {}
        self._pageranks = {}
        missing_urls = []
        
        # Populate backlinks dictionary.
        
        for website, outlinks in self._webgraph.iteritems():
            if website not in self._backlinks:
                self._backlinks[website] = []
            
            for outlink in outlinks:
                self._backlinks.setdefault(outlink, []).append(website)
                
                if outlink not in self._webgraph:
                    missing_urls.append(outlink)
        
        # Add missing URLs to webgraph.
        
        for url in missing_urls:
            self._webgraph[url] = []
            self._backlinks[url] = []
        
    
    @property
    def page_ranks(self):
        """
        Returns a mapping from URL to page rank.
        
        Returns:
            A dictionary mapping websites to page ranks.
        
        """
        return self._pageranks
    
    def compute(self, termination_threshold = 0.1):
        """
        Computes the page rank for every website in the webgraph.
        
        The calculation is done in multiple steps in which the page ranks are calculated using the
        page ranks from the previous step (beginning with 1 / number of websites in the webgraph for
        all websites). The calculation is finished when the difference between the calculated page
        ranks and the page ranks from the previous step is smaller than the termination threshold.
        
        The result of this computation can be retrieved using the page_ranks attribute.
        
        Args:
            termination_threshold: The calculation finishes when the difference between the
                                   calculated page ranks and those from the previous step is below
                                   this threshold (default 0.1).
        
        """
        self._pageranks = {}
        
        # At the beginning, every website gets the pagerank 1 / number of websites.
        
        for website in self._webgraph.keys():
            self._pageranks[website] = 1.0 / len(self._webgraph)
            
        while True:
            # Compute new page ranks.
            
            new_page_ranks = self._compute_step()
            
            # Are they good enough?
            
            terminate = self._is_termination_threshold_met(new_page_ranks, termination_threshold)
            
            # Save them.
            
            self._pageranks = new_page_ranks
            
            if terminate:
                break
        
    def _compute_step(self):
        """
        Computes and returns the page rank for every website in the webgraph.
        
        The page ranks dictionary (self._pageranks) must be initialized before calling this method!
        
        Returns:
            A dictionary mapping websites to page ranks.
        
        """
        new_pageranks = {}
        teleportation_rate = 1.0 - self._dampening_factor
        
        # Compute "dangling websites part" of the page rank. It is computed only once per step
        # because it is equal for all websites in the webgraph.
        
        dangling_websites_part = self._compute_dangling_websites_part()
        
        # Calculate page rank for every website in the webgraph.

        for website in self._webgraph.keys():
            backlink_part = self._compute_backlink_part(website)
            
            pagerank = self._dampening_factor * (backlink_part + dangling_websites_part) 
            pagerank += (teleportation_rate / len(self._webgraph))

            new_pageranks[website] = pagerank
            
        return new_pageranks
    
    def _compute_backlink_part(self, website):
        """
        Computes the backlink part of the page rank for the given website.
        
        For every backlink B to the given website, the page rank of B is divided through the number
        of outlinks of B. The sum of the results is the backlink part of the page rank for the 
        website.

        Args:
            website: The website for which the backlink part should be computed.

        Returns:
            The backlink part of the page rank for the given website.
        
        """
        backlink_part = 0
            
        for backlink in self._backlinks[website]:
            backlink_part += self._pageranks[backlink] / len(self._webgraph[backlink])
        
        return backlink_part
    
    def _compute_dangling_websites_part(self):
        """
        Computes and returns the dangling websites part of the page rank.
        
        For every dangling website D, the page rank of D is divided through the number of websites
        in the webgraph. The sum of the results is returned.
        
        Returns:
            The dangling websites part of the page rank.
        
        """
        dangling_websites_part = 0
        for website, outlinks in self._webgraph.iteritems():
            if len(outlinks) == 0:
                dangling_websites_part += self._pageranks[website] / len(self._webgraph)
        
        return dangling_websites_part

    def _is_termination_threshold_met(self, new_page_ranks, termination_threshold):
        """
        Calculates the difference between the new page ranks and the previous ones and checks
        whether the difference is smaller than the termination threshold.
        
        Args:
            new_page_ranks: The new page ranks (dictionary mapping websites to page ranks).
            termination_threshold: Threshold for terminating the page rank computation.
        
        Returns:
            When the difference is lower than the termination threshold True, otherwise False.
        
        """
        difference_sum = 0
        
        for website in self._webgraph.keys():
            difference_sum += abs(self._pageranks[website] - new_page_ranks[website])
        
        return difference_sum <= termination_threshold

