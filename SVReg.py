from sklearn.svm import SVR
import csv, time
import cPickle as pickle

class SVReg():
    def __init__(self):
        print 'Loading spm.pkl ...'
        self.y = self.getY()
        infile = open('spm.pkl', 'rb')
        _x = pickle.load(infile)   # sparse matrix
        self.X = _x.tocsr()
        infile.close()
        print 'Sparse Loaded Successfully.'
        print 'Slicing the sparse...'
        self.slicing()
        self.regressor()
        
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
    
    def slicing(self):
        self.t = {}
        self.u = {}
        k = 0
        self._noOfSVR = 0
        s = self._sizeOfTraining
        print s
        for i in range(1,41):
            self._noOfSVR += 1
            if s > 2500:
                self.t[i] = self.X[k:k+2500]
                self.u[i] = self.y[k:k+2500]
                k = k + 2500
                s = s - 2500
            else:
                self.t[i] = self.X[k:]
                self.u[i] = self.y[k:]
                break
    
    def regressor(self):
        sv = [0 for m in range(0,41)]
        for n in range(1,self._noOfSVR + 1):
            print 'Initializing SVR...'
            sv[n] = SVR(C=1e1, epsilon=0.2, kernel='linear')
            print 'Fitting...'
            a = self.t[n]
            sv[n].fit(a, self.u[n])
            print 'saving model...'
            f = open('SV ' + str(n) + '.pkl', "wb")
            pickle.dump(sv[n], f, pickle.HIGHEST_PROTOCOL)
            f.close()

if __name__ == '__main__':
    start_time = time.time()
    sv = SVReg()
    print time.time() - start_time, 'seconds'
