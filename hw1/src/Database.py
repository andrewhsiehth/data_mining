class Database: 
        def __init__(self):
            self.transactions = None 
            self.itemIndex = {} 
            self.itemList = [] 

        def addItem(self, item):
            if item not in self.itemIndex:
                self.itemIndex[item] = len(self.itemList) 
                self.itemList.append(item) 
            return  

        def fromFile(self, path, sep=' '): 
            self.transactions = [] 
            with open(path, mode='r') as f: 
                lines = f.readlines() 
                f.close() 
            for line in lines: 
                transaction = [] 
                for item in line.strip().split(sep): 
                    self.addItem(item) 
                    transaction.append(self.itemIndex[item]) 
                self.transactions.append(frozenset(transaction)) 
            return 
