from collections import defaultdict 
from itertools import combinations 

from util import timeit 

class Eclat:  
    def __init__(self, minSupport, minConfidence): 
        self.minSupport = minSupport 
        self.minConfidence = minConfidence 

    @timeit 
    def generateBitvectors(self, db): 
        bitvectors = defaultdict(int) 
        for tIdx, transaction in enumerate(db.transactions):  
            for itemIdx in transaction: 
                bitvectors[frozenset([itemIdx])] |= (1 << tIdx) 
        return bitvectors 

    @timeit 
    def prune(self, bitvectors, db):  
        pruned = defaultdict(int) 
        transactionCounts = len(db.transactions) 
        for itemset, bitvector in bitvectors.items(): 
            count = bin(bitvector).count('1') 
            if count / transactionCounts >= self.minSupport: 
                pruned[itemset] = count  
        return pruned 

    @timeit 
    def mining(self, bitvectors, db): 
        largeItemsets = defaultdict(int) 
        pruned = self.prune(bitvectors, db)   
        if not pruned: 
            return largeItemsets 
        largeItemsets.update(pruned) 
        itemsets = list(pruned.keys())
        for i, itemsetI in enumerate(itemsets): 
            candidates = defaultdict(int) 
            for j, itemsetJ in enumerate(itemsets[i+1:]):
                candidate = itemsetI | itemsetJ 
                candidates[candidate] = bitvectors.get(itemsetI) & bitvectors.get(itemsetJ) 
            largeItemsets.update(self.mining(candidates, db)) 
        return largeItemsets  

    @timeit 
    def generateLargeItemsets(self, db):
        bitvectors = self.generateBitvectors(db) 
        largeItemsets = self.mining(bitvectors, db) 
        return largeItemsets 
