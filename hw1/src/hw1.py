from collections import defaultdict 
from itertools import combinations 
from itertools import product 
from itertools import chain 
import time 
import sys 

from util import timeit 
from Apriori import Apriori 

@timeit 
def runApriori(inputFile, outputFile, minSupport): 
    # db = Database() 
    # db.fromFile(path=inputFile) 
    apriori = Apriori(minSupport=minSupport, minConfidence=0) 
    apriori.initDb(path=inputFile) 
    L, C = apriori.generateLargeItemsets() 
    apriori.output(L, C, path=outputFile) 
    return 

@timeit 
def runEclat(inputFile, outputFile, minSupport):
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
    elif args.apriori: 
        runApriori(inputFile=args.inputFile, outputFile=args.output, minSupport=args.minSuport) 
    elif args.eclat: 
        runEclat(inputFile=args.inputFile, outputFile=args.output, minSupport=args.minSuport)




