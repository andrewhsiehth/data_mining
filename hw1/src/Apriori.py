from collections import defaultdict 
from itertools import combinations 
from itertools import product 
from itertools import chain 

from util import timeit 

# def generateProperNoneEmptySubsets(s):
#     return chain(*map(lambda subsetSize: map(lambda x: frozenset(x), combinations(s, subsetSize)), range(1, len(s)))) 

class Apriori: 
    class Database: 
        def __init__(self): 
            self.transactions = None 

        def fromFile(self, path): 
            self.transactions = [] 
            with open(path, mode='r') as f: 
                lines = f.readlines() 
                f.close() 
            for line in lines: 
                self.transactions.append(frozenset(line.strip().split(' '))) 
            return 

    def __init__(self, minSupport, minConfidence): 
        self.minSupport = minSupport 
        self.minConfidence = minConfidence 
        self.db = self.Database() 

    @timeit 
    def initDb(self, path): 
        self.db.fromFile(path) 
        return 
        
    @timeit
    def generateC1(self): 
        C1 = defaultdict(int) 
        for transaction in self.db.transactions: 
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
    def scanDb(self, Ck): 
        for candidate in Ck: 
            for transaction in self.db.transactions: 
                if candidate <= transaction: 
                    Ck[candidate] += 1 
        return Ck 


    @timeit
    def generateLk(self, Ck): 
        Lk = set() 
        transactionCounts = len(self.db.transactions) 
        for candidate, count in Ck.items():
            support = count / transactionCounts 
            if support >= self.minSupport: 
                Lk.add(candidate) 
        return Lk  

    @timeit 
    def generateLargeItemsets(self): 
        C = [defaultdict(int)]  
        L = [set()]    
        C1 = self.generateC1() 
        L1 = self.generateLk(C1)  
        Ck = C1 
        Lk = L1 
        while Lk:  
            C.append(Ck) 
            L.append(Lk)   
            print('iter: {0} len(C{0}): {1} len(L{0}): {2}'.format(len(L)-1, len(C[-1]), len(L[-1]))) 
            Ck = self.generateCk(L[-1]) 
            Ck = self.scanDb(Ck)  
            Lk = self.generateLk(Ck) 
        return L, C  

    # @timeit 
    # def generateAssociationRules(self, L, C): 
    #     associationRules = []
    #     transactionCounts = len(self.db.transactions)   
    #     for l in chain(*L): 
    #         for s in generateProperNoneEmptySubsets(l): 
    #             diff = l - s  
    #             support = C[len(l)].get(l) / transactionCounts 
    #             confidence = C[len(l)].get(l) / C[len(diff)].get(diff)  
    #             if confidence >= self.minConfidence: 
    #                 associationRules.append((diff, s, support, confidence))  
    #     return associationRules 

    def output(self, L, C, path):  
        with open(path, mode='w') as f: 
            f.writelines(sorted(['{0} ({1})\n'.format(' '.join(sorted(l, key=int)), C[len(l)].get(l)) for l in chain(*L)], key=lambda x: (len(x), x)))
            f.close() 
        return 