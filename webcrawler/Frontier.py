'''
Created on Nov 8, 2013

@author: prototyp
'''


class Frontier:
    '''
    classdocs
    '''

# Kontrolle auf zugriff der listen synchronized
# Static oder singleton
    toVisitNodes=[]
    visitedNodes=[""]
    
    def __init__(self,seeds):
        self.toVisitNodes=seeds
        self.visitedNodes=[]

    #adds a new node which should be visited. check if the node already has been visited
    def setNode(self,newNode):
        if (newNode not in self.visitedNodes and newNode not in self.toVisitNodes):
            #print "Node added        " + newNode
            self.toVisitNodes.append(newNode)
        else:
            pass
            #print "Node already visited"
            
            
    def getNode(self):
        if self.getLenToVisit() != 0:
            node = self.toVisitNodes[0]
            self.visitedNodes.append(node)
            del self.toVisitNodes[0]
            return node
        else:
            #print "All Nodes visited"
            return ""
        
    def getLenToVisit(self):
        return len(self.toVisitNodes)
    
    def getLenVisitedNotes(self):
        return len(self.visitedNodes)