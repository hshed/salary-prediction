#!/usr/bin/python
# -*- coding: cp1252 -*-
import csv, time, math, string
from scipy.sparse import coo_matrix
from numpy import array
class Dictionary():
    
    def __init__(self, documentLength, isSparse=None):
        print 'Initializing...'
        if isSparse == None:
            self._isSparse = 0
        else: self._isSparse = 1
        self._documentLength = documentLength
        #self.isAsIntended = re.compile(r"\w{3,}").findall
        #self._countInDocumentDict = {}  # e.g. {d1:10, d2:50, ...} for one word
        self._universalWordDict = {}  # e.g. {w1:{d1:10, d2:50, ...}, w2:{d1:20, d2:0, ...}, ...}
        #self._universalWordDict = OrderedDict()
        self._dictOfWordCount = {}  # e.g. {d1:200, d2:300, d3:100, ...}
        self._categoryDict = {}  # e.g. {'teaching job':[1000,15000,...],...}
        self._locationDict = {}  # e.g. {'location':[1000,15000,...],...}
        self._companyDict = {}   # e.g. {'company':[1000,5000,...],...}
        self._sourceDict = {}    #e.g.  {'source':[1000,5000,...],...}
        self._jobTimeTermList = []   #e.g. {1:'[full, permanent]', 2:[None,None], 3:'[part, contact]'}
        self._locationDocs = {}
        self._companyDocs = {}
        self._catDocs = {}
        self._sourceDocs = {}
        self.setDifferentDicts()  # building the dict universalWordDict
        print 'length: ', len(self._universalWordDict)
        print 'Dictionary Created'
        self.writeIDFtoCSV()
        self._wordIdfList = [(v,k) for k,v in self._idfOfWord.items()]
        self._wordIdfList.sort(reverse=True, key = lambda tup: tup[0])
        
    def setDifferentDicts(self):
        with open('Training.csv', mode='r') as infile:
            reader = csv.reader(infile)
            reader.next()  # first row with headings. we have to ignore it
            i = 1
            lower = str.lower
            for row in reader:
                # wordsList = re.findall(r"\w{3,}", ' '.join([row[2].lower(), row[1].lower()])) # list of words greater than size 4
                if self._isSparse == 1:  
                    category = row[7]
                    location = row[3]
                    company = row[6]
                    source = row[8]
                    tempSalary = int(row[9])
                    if self._categoryDict.has_key(category):  # means one instance of category is in the dict
                        self._categoryDict[category].append(tempSalary)
                    else: self._categoryDict[category] = [tempSalary]
                    
                    if self._catDocs.has_key(category):
                        self._catDocs[category].append(i)
                    else: self._catDocs[category] = [i]
                    
                    if self._locationDict.has_key(location):  # means one instance of location is in the dict
                        self._locationDict[location].append(float(tempSalary)/30000.0)
                    else: self._locationDict[location] = [float(tempSalary)/30000.0]
                    
                    if self._locationDocs.has_key(location):
                        self._locationDocs[location].append(i)
                    else: self._locationDocs[location] = [i]
                    
                    self._jobTimeTermList.append(self.checkData(row))
                    
                    if company != '':
                        if self._companyDocs.has_key(company):
                            self._companyDocs[company].append(i)
                        else: self._companyDocs[company] = [i]
                        if self._companyDict.has_key(company):  # means one instance of company is in the dict
                            self._companyDict[company].append(float(tempSalary)/30000.0)
                        else: self._companyDict[company] = [float(tempSalary)/30000.0]
                    
                    if source !='':
                        if self._sourceDocs.has_key(source):
                            self._sourceDocs[source].append(i)
                        else: self._sourceDocs[source] = [i]
                        if self._sourceDict.has_key(source):  # means one instance of source is in the dict
                            self._sourceDict[source].append(tempSalary)
                        else: self._sourceDict[source] = [tempSalary]
                    
                    i += 1
                    if i == self._documentLength + 1:
                        break
                else:
                    s = ' '.join([lower(row[2]), lower(row[1])])
                    s = s.translate(string.maketrans("‘’‚“”„†‡‰‹›!“#$%&‘()™*+,-˜./0123456789:;<=>?@[\]_`{|}~–—¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿Þßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ€¢â—ªïž'","                                                                                                                                "))
                    #wordsList = self.isAsIntended(' '.join([lower(row[2]), lower(row[1])]))
                    wordsList = s.split()
                    for word in wordsList:
                        v = len(word)
                        if v>3 and v<15:
                            if word not in self._universalWordDict:
                                self._universalWordDict[word]={i:1}
                            else:
                                if i not in self._universalWordDict[word]:
                                    self._universalWordDict[word][i]=1
                                else:
                                    self._universalWordDict[word][i]+=1
                        
                    self._dictOfWordCount[i] = len(wordsList)
                    i += 1
                    if i == self._documentLength + 1:
                        break
                    
    
    def checkData(self,row):
        jobTime = row[4]
        jobTerm = row[5]
        w1={'full time':1,'part time':-1,'':0}    #this dictionary corresponds to time feature
        w2={'permanent':0,'contract':1,'':-1}     #this dictionary corresponds to term feature
        
        if jobTime == '' or jobTerm == '':
            s=row[2].lower()          
            s=s.translate(string.maketrans("‘’‚“”„†‡‰‹›!“#$%&‘()™*+,-˜./0123456789:;<=>?@[\]_`{|}~–—¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿Þßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ€¢â—ªïž'","                                                                                                                                "))
            if jobTime=='':
                if ('full time' in s and 'part time' in s) or ('full time' not in s and 'part time' not in s):
                    word1=''
                else:
                    if 'full time' in s:      #searching full time in description
                        word1='full time'
                    else:
                        word1='part time'
            else:
                word1=jobTime.translate(string.maketrans("_"," ")) #removing underscore from time feature value
                
            if jobTerm=='':
                if ('permanent' in s and 'contract' in s) or ('permanent' not in s and 'contract' not in s):
                    word2=''
                else:
                    if 'permanent' in s:      #searching permanent in description
                        word2='permanent'
                    else:
                        word2='contract'
            else: word2=jobTerm.translate(string.maketrans("_"," "))   #removing underscore from term feature value
        
        else:
            word1=jobTime.translate(string.maketrans("_"," "))
            word2=jobTerm.translate(string.maketrans("_"," "))
            
        return [word1,w1[word1],word2,w2[word2]]
   
    
    def tfNew(self, freq, count):
        return freq / float(count)
        
    def idfNew(self, num):
        return math.log10(float(self._documentLength) / (num))
    
    def writeIDFtoCSV(self):
        idfList = []
        self._idfOfWord = {}
        with open('IdfList.csv', mode='w') as outfile:
            writer = csv.writer(outfile, lineterminator='\n')
            for word in self._universalWordDict:
                idfList.append(word)
                num = len(self._universalWordDict[word])
                x = self.idfNew(num)
                idfList.append(x)
                writer.writerow(idfList)
                self._idfOfWord[word] = x
                idfList = []
                
    def tfidfNew(self, freq, count, num):
        return self.tfNew(freq, count) * self.idfNew(num)
    
    def totalidf(self):
        # tempListWord = [None]*(self._documentLength + 1)
        # finalList = []
        c = []
        r = []
        d = []
        i = 0  # 0th word
        #sorted_dict = OrderedDict(sorted(self._universalWordDict.iteritems()))
        for word in self._universalWordDict:
            tempDict = self._universalWordDict[word]
            numOfDocsContaining = len(tempDict)
            for document in tempDict:
                count  = self._dictOfWordCount[document]
                freq = tempDict[document]
                c.append(document - 1)
                r.append(i)
                d.append(self.tfidfNew(freq, count, numOfDocsContaining))
                # tempListWord[document] = self.tfidfNew(freq, document, numOfDocsContaining)
            i += 1
        print len(c)
        print len(r)
        print len(d)
        col = array(c)
        row = array(r)
        data = array(d)
        sparseA = coo_matrix((data, (row, col)), shape=(len(self._universalWordDict), self._documentLength))
        '''del c[:]
        del r[:]
        del d[:]'''
        return sparseA
            # finalList.append(tempListWord)
            # tempListWord = [None]*(self._documentLength + 1)
            
    def tfidfInDict(self):
        theDict = {}
        tDict = self._universalWordDict
        for word in tDict:
            tempDict = tDict[word]
            numOfDocsContaining = len(tempDict)
            for document in tempDict:
                count  = self._dictOfWordCount[document]
                freq = tempDict[document]
                if word not in theDict:
                    theDict[word] = {document:self.tfidfNew(freq, count, numOfDocsContaining)}
                else:
                    theDict[word][document] = self.tfidfNew(freq, count, numOfDocsContaining)
        return theDict
        
if __name__ == "__main__":
    start_time = time.time()
    sal = Dictionary(146860)
    @staticmethod
    def idfList():
        return sal._wordIdfList
    print time.time() - start_time, "seconds"
