'''
CosineScore(q)
1 float Scores[N] = 0
2 float Length[N]
3 for each query term t
4 do calculate w t,q and fetch postings list for t
5 for each pair(d,tf t,d) in postings list
6 do Scores[d]+ = w t,d × w t,q
7 Read the array Length
8 for each d
9 do Scores[d] = Scores[d]/Length[d] << hier fehlte noch was?
10 return Top K components of Scores[]

aus Scoring Folie S 27/37

qi = tf-idf Gewicht des Wortes in Query
di = tf-idf Gewicht des Wortes in Dokument

cos = (qi * di) / wurzel(alle qi²) * wurzel(alle di²)

cos ist damit der Abstand des Query-Vektors zu dem des Dokuments

'''
class Scorer:
    
    __indexDf = {}
    __indexTf = {}
    __documentCount = 0
    __scores = []
    __length = []
    
    def __init__(self,indexDf,indexTf,documentCount):
        self.__indexDf = indexDf
        self.__indexTf = indexTf
        self.__documentCount = documentCount
    
    def cosinScore(self,query,postingsList):
        ''' 3 for each query term t '''
        for term in query[terms]:
            ''' Gewichtung holen ??? '''
            for pair in postingsList:
                ''' 6 do Scores[d]+ = w t,d × w t,q '''
                scoresDocument.add(weightTermDocument * weightTermQuery)

                ''' 8 for each d '''
                for document in postingsList:
                    summeQis = 0;
                    for qi in qis:
                        summeQis = summeQis + quadrat(qi)

                        lengthQi = wurzel(summeQis)

                        summeDis = 0;
                        for di in dis:
                            summeDis = summeDis + quadrat(di)

                            lengthDi= wurzel(summeQis * summeDis)

                            score[document] = score[document] / (lengthQi * lengthDi)

                return scoresDocument
     
     def __calcW(self):
         pass
    
         
     def __calcLength(self):         
         pass