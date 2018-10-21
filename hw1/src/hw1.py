from collections import defaultdict 
from itertools import combinations 
from itertools import product 
from itertools import chain 
import time 
import sys 

from util import timeit 
from Apriori import Apriori 
from Database import Database 
from Eclat import Eclat 

@timeit 
def runApriori(inputFile, outputFile, minSupport): 
    def output(L, C, db, path):  
        with open(path, mode='w') as f: 
            # f.writelines(sorted(['{0} ({1})\n'.format(' '.join(sorted(l, key=int)), C[len(l)].get(l)) for l in chain(*L)], key=lambda x: (len(x), x)))
            f.writelines(sorted(['{0} ({1})\n'.format(' '.join(sorted(map(lambda x: db.itemList[x], l), key=int)), C[len(l)].get(l)) for l in chain(*L)], key=lambda x: (len(x), x)))
            f.close() 
        return 
    db = Database() 
    db.fromFile(path=inputFile)
    apriori = Apriori(minSupport=minSupport, minConfidence=0) 
    L, C = apriori.generateLargeItemsets(db) 
    output(L, C, db, path=outputFile) 
    return 

@timeit 
def runEclat(inputFile, outputFile, minSupport): 
    def output(L, db, path): 
        with open(path, mode='w') as f: 
            f.writelines(sorted(['{0} ({1})\n'.format(' '.join(sorted(map(lambda x: db.itemList[x], l), key=int)), count) for l, count in L.items()], key=lambda x: (len(x), x))) 
            f.close()
        return 
    db = Database() 
    db.fromFile(path=inputFile) 
    eclat = Eclat(minSupport=minSupport, minConfidence=0) 
    L = eclat.generateLargeItemsets(db) 
    output(L, db, path=outputFile) 
    return 


        
if __name__ == '__main__': 
    import os 
    import pickle 
    import argparse 
    parser = argparse.ArgumentParser() 
    parser.add_argument('-i', '--inputFile', required=True) 
    parser.add_argument('-o', '--output', required=True) 
    parser.add_argument('-s', '--minSuport', default=0)  
    parser.add_argument('-d', '--debugFolder', default=None) 
    parser.add_argument('-a', '--apriori', default=False, action='store_true')
    parser.add_argument('-e', '--eclat', default=False, action='store_true')
    args = parser.parse_args() 

    if args.debugFolder: 
        # apriori experiments 
        aMinSupport = [0.35, 0.3, 0.25, 0.2] 
        aExecutionTime = []
        for support in aMinSupport:         
            startTime = time.time() 
            runApriori(
                inputFile=args.inputFile, 
                outputFile=os.path.join(args.output, 'A{0:.2f}.log'.format(support)),  
                minSupport=support 
            ) 
            endTime = time.time() 
            executionTime = endTime - startTime 
            aExecutionTime.append(executionTime) 
        with open(os.path.join(args.debugFolder, 'apriori.log'), mode='w') as f: 
            f.write('minSupport,executionTime\n') 
            for s, e in zip(aMinSupport, aExecutionTime): 
                f.write('{0:.2f},{1:.6f}\n'.format(s, e)) 
            f.close() 

        # eclat experiments
        eMinSupport = [0.35, 0.3, 0.25, 0.2, 0.15, 0.1, 0.05] 
        eExecutionTime = [] 
        for support in eMinSupport: 
            startTime = time.time() 
            runEclat(
                inputFile=args.inputFile, 
                outputFile=os.path.join(args.output, 'E{0:.2f}.log'.format(support)),  
                minSupport=support 
            ) 
            endTime = time.time() 
            executionTime = endTime - startTime 
            eExecutionTime.append(executionTime) 
        with open(os.path.join(args.debugFolder, 'eclat.log'), mode='w') as f: 
            f.write('minSupport,executionTime\n') 
            for s, e in zip(eMinSupport, eExecutionTime): 
                f.write('{0:.2f},{1:.6f}\n'.format(s, e)) 
            f.close() 

    elif args.apriori: 
        runApriori(inputFile=args.inputFile, outputFile=args.output, minSupport=args.minSuport) 
    elif args.eclat: 
        runEclat(inputFile=args.inputFile, outputFile=args.output, minSupport=args.minSuport)




