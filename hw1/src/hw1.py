from collections import defaultdict 
from itertools import combinations 
from itertools import product 
from itertools import chain 
import time 


def timeit(func): 
    def timed(*args, **kwargs): 
        startTime = time.time() 
        funcReturn = func(*args, **kwargs) 
        endTime = time.time() 
        executionTime = endTime - startTime 
        print('[{0}] execution time: {1}'.format(func.__name__, executionTime))  
        return funcReturn 
    return timed 

def generateProperNoneEmptySubsets(s):
    return chain(*map(lambda subsetSize: map(lambda x: frozenset(x), combinations(s, subsetSize)), range(1, len(s)))) 

class Database: 
    def __init__(self): 
        self.transactions = []

    def fromFile(self, path):
        with open(path, mode='r') as f: 
            lines = f.readlines() 
            f.close() 
        for line in lines: 
            self.transactions.append(frozenset(line.strip().split(' '))) 
        return 


class Apriori: 
    def __init__(self, minSupport, minConfidence): 
        self.minSupport = minSupport 
        self.minConfidence = minConfidence 
        self.itemsets = {} 

    @timeit
    def generateC1(self, db): 
        C1 = defaultdict(int) 
        for transaction in db.transactions: 
            for item in transaction: 
                candidate = frozenset([item])
                C1[self.itemsets.setdefault(candidate, candidate)] += 1 
        return C1 

    @timeit 
    def generateCk(self, itemsets): 
        Ck = defaultdict(int)  
        for itemsetI, itemsetJ in combinations(itemsets, r=2):
            candidate = itemsetI | itemsetJ 
            if len(candidate) == len(itemsetI)+1: 
                Ck[self.itemsets.setdefault(candidate, candidate)] = 0  
        return Ck 

    @timeit
    def scan(self, Ck, db): 
        for candidate in Ck: 
            for transaction in db.transactions: 
                if candidate <= transaction: 
                    Ck[candidate] += 1 
                    assert candidate is self.itemsets.get(candidate) 
        return Ck 


    # @timeit
    # def __generateCk(self, Lk_minus1, db): 
    #     Ck = defaultdict(int) 
    #     for itemsetI, itemsetJ in combinations(Lk_minus1, r=2): 
    #         candidate = itemsetI | itemsetJ
    #         if len(candidate) == len(itemsetI)+1: 
    #             if candidate not in Ck: 
    #                 for transaction in db.transactions: 
    #                     if candidate <= transaction: 
    #                         Ck[candidate] += 1 
    #     return Ck 


    @timeit
    def generateLk(self, Ck, db): 
        Lk = set() 
        transactionCounts = len(db.transactions) 
        for candidate, count in Ck.items():
            support = count / transactionCounts 
            if support >= self.minSupport: 
                Lk.add(candidate) 
                assert candidate is self.itemsets.get(candidate) 
        return Lk  

    @timeit 
    def generateAssociationRules(self, L, C, db): 
        associationRules = []
        transactionCounts = len(db.transactions)   
        for l in chain(*L): 
            for s in generateProperNoneEmptySubsets(l): 
                diff = l - s  
                support = C[len(l)].get(l) / transactionCounts 
                confidence = C[len(l)].get(l) / C[len(diff)].get(diff)  
                if confidence >= self.minConfidence: 
                    associationRules.append((diff, s, support, confidence))  
        return associationRules 


    @timeit 
    def generateLargeItemsets(self, db): 
        self.itemsets = {}
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
            Ck = self.scan(Ck, db)  
            Lk = self.generateLk(Ck, db) 
        return L, C  


    def output(self, L, C): 
        for l in sorted(chain(*L), key=lambda l: C[len(l)].get(l)):
            print('{0} ({1})'.format(' '.join(sorted(l)), C[len(l)].get(l)))
