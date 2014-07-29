import csv, time, cPickle
from numpy import median, array
from scipy.sparse import coo_matrix
from TestFile import TestFile as test
class TestSparse():
    def __init__(self):
        dictionObj = test()
        self._wordDict = dictionObj._WordDict
        self._dictOfWordCount = dictionObj._dictOfWordCount
        self._timeDict = {1:[], -1:[]} #1=> full time, -1=> part time
        self._termDict = {1:[], -1:[]} #1=> permanent, -1=> part time
        self.timeTermDict()
        self.idfList = dictionObj._prevIdfList
        self.tfIdfDict = dictionObj.calculateTfIdf()
        self._tempLocDict = dictionObj._testlocationDict
        self._locDict = {}
        self._locDocs = dictionObj._testlocationDocs   # each location in which which docs
        self._tempCompanyDict = dictionObj._testcompanyDict
        self._companyDict = {}
        self._companyDocs = dictionObj._testcompanyDocs # each company in which which docs
        self.locationSalary() # # e.g. _locDict = {'loc1':[1000, 5000,2000],...}
        self.companySalary()  # e.g. _companyDict = {'comp1':[1000, 5000,2000],...}
        self._catDocs = dictionObj._testcatDocs #e.g. {'cat1':[1,5,8,...],...}
        self._sourceDocs = dictionObj._testsourceDocs # e.g. similar to category
        self._totalSourceDocs = dictionObj._ssourceDocs
        print 'Categories and companies and locations'
        #print self._totalSourceDocs
        self._totalCatDocs = dictionObj._scatDocs
        #print self._totalCatDocs
        self._totalCompDocs = dictionObj._scompanyDocs
        self._totalLocDocs = dictionObj._slocDocs
        print 'here'
        
    def createSparseMatrix(self):
        c = []
        r = []
        d = []
        #i = 0  # 0th word
        print 'sparsing...'
        appendR = r.append
        appendC = c.append
        appendD = d.append
        count = 0  # column count
        wordStopper = 0
        
        for time in self._timeDict:
            td = self._timeDict[time]
            for document in td:
                appendC(count)
                appendR(document - 1)
                appendD(time)
        count+=1
        
        for term in self._termDict:
            td = self._termDict[term]
            for document in td:
                appendC(count)
                appendR(document - 1)
                appendD(term)
        count+=1
        
        for location in self._locDocs:
            td = self._locDocs[location] #list
            for document in td:
                for b in xrange(0,3):
                    appendC(count + b)
                    appendR(document-1)
                    appendD(self._locDict[location][b])
        count +=3
        
        for company in self._companyDocs:
            td = self._companyDocs[company] #list
            for document in td:
                for b in xrange(0,3):
                    appendC(count + b)
                    appendR(document-1)
                    appendD(self._companyDict[company][b])
        count +=3
        
        for category in self._totalCatDocs:
            if self._catDocs.has_key(category):
                td = self._catDocs[category] #
                for document in td:
                    appendC(count)
                    appendR(document - 1)
                    appendD(1)
            count +=1
        
        for source in self._totalSourceDocs:
            if self._sourceDocs.has_key(source):
                td = self._sourceDocs[source]
                for document in td:
                    appendC(count)
                    appendR(document - 1)
                    appendD(1)
            count +=1
        for word in self.idfList:
            wordStopper +=1
            count +=1
            if wordStopper>10000:
                break 
        col = array(c)
        print max(c)
        row = array(r)
        print len(r)
        data = array(d)
        print len(data)
        print 'sparse'
        sparseA = coo_matrix((data, (row, col)), shape=(112, count))
        print 'writing sparse in testspm.pkl'
        f = open('testspm.pkl', 'wb')
        cPickle.dump(sparseA, f, cPickle.HIGHEST_PROTOCOL)
        f.close()
        ''''l = []
        for i in range(1,40):
            l.append('RF '+ str(i) + '.pkl')
        cPickle.dump(l,open('rffilenames.pkl','wb'),cPickle.HIGHEST_PROTOCOL)'''
        return sparseA
    
    def timeTermDict(self):
        # e.g. {'full time':[1,5,10,..],'part time':[5,15,20,...]}
        # e.g. {'permanent':[1,4,9,...],'contract':[2,6,8,..,]}
        print 'Please Wait...'
        try :
            with open('TestTimeAndTerm.csv', mode='r') as infile:
                reader = csv.reader(infile)
                i = 1 #document #1
                for row in reader:
                    if row[0] == 'full time':
                        self._timeDict[1].append(i)
                    if row[0] == 'part time':
                        self._timeDict[-1].append(i)
                    if row[2] == 'permanent':
                        self._termDict[1].append(i)
                    if row[2] == 'contract':
                        self._termDict[-1].append(i)
                    i+=1
        except IOError:
            print 'Is TestTimeAndTerm.csv open? If not, then run TestFile.py first!'
     
    
    def locationSalary(self):
        # e.g. {'loc1':[1000, 5000,2000],...}
        tempSalList = []
        tempDict = self._tempLocDict
        tmpDic = {}
        for location in tempDict:
            tempSalaryList = tempDict[location]
            minSal = min(tempSalaryList)
            tempSalList.append(minSal)
            maxSal = max(tempSalaryList)
            tempSalList.append(maxSal)
            medianSal = median(tempSalaryList)
            tempSalList.append(medianSal)
            tmpDic[location] = tempSalList
            tempSalList = []
        self._locDict = tmpDic
        
    def companySalary(self):
        # e.g. {'comp1':[1000, 5000,2000],...}
        tempCompList = []
        tempDict = self._tempCompanyDict
        tmpDic = {}
        for company in tempDict:
            tempSalaryList = tempDict[company]
            minSal = min(tempSalaryList)
            tempCompList.append(minSal)
            maxSal = max(tempSalaryList)
            tempCompList.append(maxSal)
            medianSal = median(tempSalaryList)
            tempCompList.append(medianSal)
            tmpDic[company] = tempCompList
            tempCompList = []
        self._companyDict = tmpDic
        
if __name__ == '__main__':
    start_time = time.time()
    cre = TestSparse()
    print time.time() - start_time, 'seconds'
    print cre.createSparseMatrix()
    print time.time() - start_time, 'seconds'
