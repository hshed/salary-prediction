#!/usr/bin/env python
from sklearn.svm import SVR
import csv, time
import cPickle as pickle
import multiprocessing

def getY():
    Y = []
    i = 0
    with open('Training-original.csv', mode='r') as infile:
        reader = csv.reader(infile)
        reader.next()
        for row in reader:
            Y.append(eval(row[9])/30000.0)
            i += 1
            if i == 5000:
                break

def rclf(a,b,clf2):
    clf2.fit(a,b)
    f = clf2.predict(a)
    return f

def clf(a,b):
    print 'Initializing SVR'
    clf1 = SVR(C=1e3, epsilon=0.2, kernel='linear')
    print 'Starting fitting'
    #clf1.fit(a, b)
    #return clf1.predict(a)
    rclf(a, b, clf1)
    
result_list = []
def log_result(result):
    # This is called whenever foo_pool(i) returns a result.
    # result_list is modified only by the main process, not the pool workers.
    result_list.append(result)

if __name__ == '__main__':
    start_time = time.time()
    print 'Loading spm.pkl'
    infile = open('spm.pkl', 'rb')
    X = pickle.load(infile)   # sparse matrix
    
    infile.close()
    print 'Sparse Loaded Successfully'
    y = getY()
    pool = multiprocessing.Pool(processes=1)
    pool.apply_async(clf, args=[X,y], callback = log_result)
    pool.close()
    pool.join()
    print result_list
    ''''p = multiprocessing.Process(target=clf, args=(X,y))
    p.start()
    p.join()'''
    
    print time.time() - start_time, 'seconds'

