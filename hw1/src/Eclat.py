

class Eclat: 
    class Database: 
        def __init__(self):
            self.transactions = None 
            self.itemIndex = {} 
            self.items = [] 

        def addItem(self, item):
            if item not in self.itemIndex:
                self.itemIndex[item] = len(self.items) 
                self.items.append(item) 
            return  

        def fromFile(self, path, sep=' '): 
            with open(path, mode='r') as f: 
                lines = f.readlines() 
                f.close() 
            for line in lines: 
                transaction = [] 
                for item in line.strip().split(sep): 
                    self.addItem(item) 
                    transaction.append(self.itemIndex[item]) 
                self.transactions.append(transaction) 
            return 
    
    def __init__(self, minSupport, minConfidence): 
        self.minSupport = minSupport 
        self.minConfidence = minConfidence 
        self.db = None 

    def initDb(self, path): 
        self.db = self.Database() 
        self.db.fromFile(path) 
        return 


    def transactions2bitvectors(self): 
        bitvectors = [] 
        for transaction in self.db.transactions: 
            bitvector = 0 
            for item in transaction: 
                bitvector |= (1 << item) 
            bitvectors.append(bitvector) 
        return bitvector 

    

    