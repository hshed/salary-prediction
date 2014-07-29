import cPickle as pickle
import csv, time, math
class RFTest():
    def __init__(self):
        print 'Loading testspm.pkl ...'
        self.y = self.getY()
        infile = open('testspm.pkl', 'rb')
        _x = pickle.load(infile)   # sparse matrix
        self.X = _x.toarray()
        infile.close()
        print 'Sparse Loaded Successfully.'
        l = []
        for i in range(1,2):
            l.append('RF '+ str(i) + '.pkl')
        pickle.dump(l,open('rffilenames.pkl','wb'),pickle.HIGHEST_PROTOCOL)
        f=open('rffilenames.pkl',"rb")
        l=pickle.load(f)   #this list contains model names
        f.close()
        print 'Predicting Salary'
        predicted_salary=[]
    
        for word in l:
            f=open(word,"rb")
            rf=pickle.load(f)
            f.close()
            predicted_salary.append(rf.predict(self.X))
        
        # mean of all models
        salary=[0 for x in range(0,len(predicted_salary[0]))]
        i=0
        for i in range(0,len(salary)):
            for e in predicted_salary:
                salary[i]+=e[i]
            
        for i in range(0,len(salary)):
            salary[i]=salary[i]/float((len(l)))

        print 'Calculating mean square error'
        
        error=0
        for i in range(0,len(salary)):
            error+=(salary[i]-self.y[i])**2
        error=error/float(len(salary))

        print 'Root Mean square error :', math.sqrt(error)*30000 #30000 is median salary used for normalization
        
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
    rftest = RFTest() 
    print time.time() - start_time, 'seconds'
