#!/usr/bin/python
# -*- coding: cp1252 -*-
import csv, time, string
from Dictionary import Dictionary as diction

class TestFile():
    def __init__(self):
        dictionObj = diction(146860)
        self._prevIdfList = dictionObj._wordIdfList[:10000]
        self._eligibleWordsList = [i[1] for i in self._prevIdfList]
        self._eligibleWords = {}
        for i in self._prevIdfList:
            self._eligibleWords[i[1]] = i[0]
        self._WordDict = {}
        self._testdictOfWordCount = {}
        self._dictOfWordCount = {}
        self._testcategoryDict = {}  # e.g. {'teaching job':[1000,15000,...],...}
        self._testlocationDict = {}  # e.g. {'location':[1000,15000,...],...}
        self._testcompanyDict = {}   # e.g. {'company':[1000,5000,...],...}
        self._testsourceDict = {}    #e.g.  {'source':[1000,5000,...],...}
        self._testjobTimeTermList = []   #e.g. {1:'[full, permanent]', 2:[None,None], 3:'[part, contact]'}
        self._testlocationDocs = {}
        self._testcompanyDocs = {}
        self._testcatDocs = {}
        print 'training features'
        di = diction(146860,1)
        self._ssourceDocs = di._sourceDocs
        self._scatDocs = di._catDocs
        self._scompanyDocs = di._companyDocs
        self._slocDocs = di._locationDocs
        self._testsourceDocs = {}
        print 'dicting...'
        self.setDicts()
        self.retrieveFeatures()
        self.writejobTimetoCSV()
        self.calculateTfIdf()
        
    def setDicts(self):
        with open('Test.csv', mode='r') as infile:
            reader = csv.reader(infile)
            reader.next()
            i = 1
            lower = str.lower
            for row in reader:
                s = ' '.join([lower(row[2]), lower(row[1])])
                s = s.translate(string.maketrans("‘’‚“”„†‡‰‹›!“#$%&‘()™*+,-˜./0123456789:;<=>?@[\]_`{|}~–—¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿Þßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ€¢â—ªïž'", "                                                                                                                                "))
                wordsList = s.split()
                for word in wordsList:
                    v = len(word)
                    if v>3 and v<15:
                        if word in self._eligibleWordsList :
                            if word not in self._WordDict:
                                self._WordDict[word] = {i:1}
                            else:
                                if i not in self._WordDict[word]:
                                    self._WordDict[word][i] = 1
                                else:
                                    self._WordDict[word][i] += 1
                        
                self._dictOfWordCount[i] = len(wordsList)
                i += 1
                #if i == 5000:
                #   break
                
    def tfidf(self, freq, count, word):
        tf = freq / float(count)
        return tf * self._eligibleWords[word]
    
    def calculateTfIdf(self):
        theDict = {}
        tDict = self._WordDict
        for word in tDict:
            tempDict = tDict[word]
            for document in tempDict:
                count = self._dictOfWordCount[document]
                freq = tempDict[document]
                if word not in theDict:
                    theDict[word] = {document:self.tfidf(freq, count, word)}
                else:
                    theDict[word][document] = self.tfidf(freq, count, word)
        return theDict
    
    def writejobTimetoCSV(self):
        with open('TestTimeAndTerm.csv', mode='w') as outfile:
            writer = csv.writer(outfile, lineterminator='\n')
            for timeterm in self._testjobTimeTermList:
                writer.writerow(timeterm)
    
    def retrieveFeatures(self):
        with open('Test.csv', mode='r') as infile:
            reader = csv.reader(infile)
            reader.next()
            i = 1
            for row in reader: 
                    category = row[7]
                    location = row[3]
                    company = row[6]
                    source = row[8]
                    tempSalary = int(row[9])
                    if self._testcategoryDict.has_key(category):  # means one instance of category is in the dict
                        self._testcategoryDict[category].append(tempSalary)
                    else: self._testcategoryDict[category] = [tempSalary]
                    
                    if self._testcatDocs.has_key(category):
                        self._testcatDocs[category].append(i)
                    else: self._testcatDocs[category] = [i]
                    
                    if self._testlocationDict.has_key(location):  # means one instance of location is in the dict
                        self._testlocationDict[location].append(float(tempSalary) / 30000.0)
                    else: self._testlocationDict[location] = [float(tempSalary) / 30000.0]
                    
                    if self._testlocationDocs.has_key(location):
                        self._testlocationDocs[location].append(i)
                    else: self._testlocationDocs[location] = [i]
                    
                    self._testjobTimeTermList.append(self.checkData(row))
                    
                    if company != '':
                        if self._testcompanyDocs.has_key(company):
                            self._testcompanyDocs[company].append(i)
                        else: self._testcompanyDocs[company] = [i]
                        if self._testcompanyDict.has_key(company):  # means one instance of company is in the dict
                            self._testcompanyDict[company].append(float(tempSalary) / 30000.0)
                        else: self._testcompanyDict[company] = [float(tempSalary) / 30000.0]
                    
                    if source != '':
                        if self._testsourceDocs.has_key(source):
                            self._testsourceDocs[source].append(i)
                        else: self._testsourceDocs[source] = [i]
                        if self._testsourceDict.has_key(source):  # means one instance of source is in the dict
                            self._testsourceDict[source].append(tempSalary)
                        else: self._testsourceDict[source] = [tempSalary]
                    
                    i += 1
                    #if i==5000:
                    #    break
                    
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
                

if __name__ == '__main__':
    start_time = time.time()
    testFile = TestFile()
    print time.time() - start_time, 'seconds'
