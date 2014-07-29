import time,csv
import cPickle as pickle
from sklearn.ensemble import RandomForestRegressor as RFR

class RFReg():
    def __init__(self):
        print 'Random Forest Regression'
        self.y = self.getY()
        infile = open('spm.pkl', 'rb')
        _x = pickle.load(infile)   # sparse matrix
        self.X = _x.tocsr()
        infile.close()
        print 'Sparse Loaded Successfully'
        print 'Slicing the sparse'
        self.slicing()
        self.regressor()
        
    def slicing(self):
        self.t = {}
        self.u = {}
        k = 0
        self._noOfRF = 0
        s = self._sizeOfTraining
        for i in range(1,29):
            self._noOfRF += 1
            if s>5000:
                self.t[i] = self.X[k:k+5000]
                self.u[i] = self.y[k:k+5000]
                k = k + 5000
                s = s - 5000
            else:
                self.t[i] = self.X[k:]
                self.u[i] = self.y[k:]
                break

    def getY(self):
        Y = []
        self._sizeOfTraining = 0
        with open('Training.csv', mode='r') as infile:
            reader = csv.reader(infile)
            reader.next()
            for row in reader:
                Y.append(eval(row[9])/30000.0)
                self._sizeOfTraining += 1
        return Y
    
    def regressor(self):
        rf = [0 for m in range(0,29)]
        for n in range(1,self._noOfRF + 1):
            rf[n] = RFR(n_estimators=20, min_samples_split = 30,n_jobs = 1, random_state = 3465343, verbose=2)
            print 'fitting...'
            a = self.t[n].toarray()
            rf[n].fit(a,self.u[n])
            print 'saving model...'
            f = open('RF ' + str(n) + '.pkl', "wb")
            pickle.dump(rf[n], f, pickle.HIGHEST_PROTOCOL)
            f.close()

if __name__ == '__main__':
    start_time = time.time()
    rf = RFReg()
    
    print time.time() - start_time, 'seconds'