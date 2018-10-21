from collections import defaultdict 
from itertools import combinations 
from itertools import product 
from itertools import chain 

from util import timeit 


class Apriori: 
    def __init__(self, minSupport, minConfidence): 
        self.minSupport = minSupport 
        self.minConfidence = minConfidence 
        
    @timeit
    def generateC1(self, db): 
        C1 = defaultdict(int) 
        for transaction in db.transactions: 
            for item in transaction: 
                candidate = frozenset([item])
                C1[candidate] += 1 
        return C1 

    @timeit 
    def generateCk(self, itemsets): 
        Ck = defaultdict(int)  
        for itemsetI, itemsetJ in combinations(itemsets, r=2):
            candidate = itemsetI | itemsetJ 
            if len(candidate) == len(itemsetI)+1: 
                Ck[candidate] = 0  
        return Ck 

    @timeit
    def scanDb(self, Ck, db): 
        for candidate in Ck: 
            for transaction in db.transactions: 
                if candidate <= transaction: 
                    Ck[candidate] += 1 
        return Ck 


    @timeit
    def generateLk(self, Ck, db): 
        Lk = set() 
        transactionCounts = len(db.transactions) 
        for candidate, count in Ck.items():
            support = count / transactionCounts 
            if support >= self.minSupport: 
                Lk.add(candidate) 
        return Lk  

    @timeit 
    def generateLargeItemsets(self, db): 
        C = [defaultdict(int)]  
        L = [set()]    
        C1 = self.generateC1(db) 
        L1 = self.generateLk(C1, db)  
        Ck = C1 
        Lk = L1 
        while Lk:  
            C.append(Ck) 
            L.append(Lk)   
            print('iter: {0} len(C{0}): {1} len(L{0}): {2}'.format(len(L)-1, len(C[-1]), len(L[-1]))) 
            Ck = self.generateCk(L[-1]) 
            Ck = self.scanDb(Ck, db)  
            Lk = self.generateLk(Ck, db)  
        return L, C  

    # @timeit 
    # def generateAssociationRules(self, L, C): 
    #     associationRules = []
    #     transactionCounts = len(db.transactions)   
    #     for l in chain(*L): 
    #         for s in generateProperNoneEmptySubsets(l): 
    #             diff = l - s  
    #             support = C[len(l)].get(l) / transactionCounts 
    #             confidence = C[len(l)].get(l) / C[len(diff)].get(diff)  
    #             if confidence >= self.minConfidence: 
    #                 associationRules.append((diff, s, support, confidence))  
    #     return associationRules 

# def generateProperNoneEmptySubsets(s):
#     return chain(*map(lambda subsetSize: map(lambda x: frozenset(x), combinations(s, subsetSize)), range(1, len(s)))) 
    # def output(self, L, C, path):  
    #     with open(path, mode='w') as f: 
    #         f.writelines(sorted(['{0} ({1})\n'.format(' '.join(sorted(l, key=int)), C[len(l)].get(l)) for l in chain(*L)], key=lambda x: (len(x), x)))
    #         f.close() 
    #     return 