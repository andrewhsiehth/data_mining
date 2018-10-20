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