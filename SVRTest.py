import cPickle as pickle
import csv, time, math
class SVRTest():
    def __init__(self):
        print 'Loading spm.pkl ...'
        self.y = self.getY()   # get the normalized salary. to be used in error calculation
        infile = open('testspm.pkl', 'rb')
        _x = pickle.load(infile)   # sparse matrix
        self.X = _x
        infile.close()
        print 'Sparse Loaded Successfully.'
        l = []
        for i in range(1,2):
            l.append('SV '+ str(i) + '.pkl')
        pickle.dump(l,open('svrfilenames.pkl','wb'),pickle.HIGHEST_PROTOCOL)
        f=open('svrfilenames.pkl',"rb")
        l=pickle.load(f)   #list containing model names
        f.close()
        print 'Predicting Salary...'
        predicted_salary=[]
    
        for word in l:
            f=open(word,"rb")
            rf=pickle.load(f)
            f.close()
            predicted_salary.append(rf.predict(self.X))
        print len(predicted_salary[0])
        #getting mean of all models
        salary=[0 for x in range(0,len(predicted_salary[0]))]
        i=0
        for i in range(0,len(salary)):
            for e in predicted_salary:
                salary[i]+=e[i]
            
        for i in range(0,len(salary)):
            salary[i]=salary[i]/float((len(l)))

        print 'Calculating mean square error'

        meanSqE=0
        for i in range(0,len(salary)):
            meanSqE+=(salary[i]-self.y[i])**2
        meanSqE=meanSqE/float(len(salary))

        print 'Root Mean square error is :', math.sqrt(meanSqE)*30000 #30000 is median salary used for normalization
        
    def getY(self):
        Y = []
        with open('Test.csv', mode='r') as infile:
            reader = csv.reader(infile)
            reader.next()
            for row in reader:
                Y.append(eval(row[9])/30000.0)
        return Y

if __name__ == '__main__':
    start_time = time.time()
    rftest = SVRTest() 
    print time.time() - start_time, 'seconds'
