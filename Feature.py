#!/usr/bin/python
# -*- coding: cp1252 -*-
import time, csv, numpy
from Dictionary import Dictionary as sp

class CategoryFeature():
    def __init__(self):
        '''collect the category dict from Sparse Class'''
        sparseObj = sp(190, 1)
        self._categoryDict = sparseObj._categoryDict
        self._locationDict = sparseObj._locationDict
        self._jobTimeTermList = sparseObj._jobTimeTermList
        self._companyDict = sparseObj._companyDict
        self._sourceDict = sparseObj._sourceDict
        self.writeCatToCSV()
        self.writeLocToCSV()
        self.writejobTimetoCSV()
        self.writeCompanytoCSV()
        self.writeSourcetoCSV()
   
    def writeCatToCSV(self):
        with open('CategoryAndSalary.csv', mode='w') as outfile:
            writer = csv.writer(outfile, lineterminator='\n')
            headings = ['Job Category', 'Min Salary', 'Max Salary', 'Median Salary']
            writer.writerow(headings)
            tempCatList = []
            for category in self._categoryDict:
                tempSalaryList = self._categoryDict[category]
                tempCatList.append(category)
                minSal = min(tempSalaryList)
                tempCatList.append(minSal)
                maxSal = max(tempSalaryList)
                tempCatList.append(maxSal)
                medianSal = numpy.median(tempSalaryList)
                tempCatList.append(medianSal)
                writer.writerow(tempCatList)
                tempCatList = []
    
    def writeLocToCSV(self):
        with open('LocationAndSalary.csv', mode='w') as outfile:
            writer = csv.writer(outfile, lineterminator='\n')
            headings = ['Location', 'Min Salary', 'Max Salary', 'Median Salary']
            writer.writerow(headings)
            tempLocList = []
            for location in self._locationDict:
                tempSalaryList = self._locationDict[location]
                tempLocList.append(location)
                minSal = min(tempSalaryList)
                tempLocList.append(minSal)
                maxSal = max(tempSalaryList)
                tempLocList.append(maxSal)
                medianSal = numpy.median(tempSalaryList)
                tempLocList.append(medianSal)
                writer.writerow(tempLocList)
                tempLocList = []
    
    def writejobTimetoCSV(self):
        with open('TimeAndTerm.csv', mode='w') as outfile:
            writer = csv.writer(outfile, lineterminator='\n')
            for timeterm in self._jobTimeTermList:
                writer.writerow(timeterm)
    
    def writeCompanytoCSV(self):
        with open('Company.csv', mode='w') as outfile:
            writer = csv.writer(outfile, lineterminator='\n')
            rowList = []                
            for company in self._companyDict:
                tempSalaryList = self._companyDict[company]
                rowList.append(company)
                minSal = min(tempSalaryList)
                rowList.append(minSal)
                maxSal = max(tempSalaryList)
                rowList.append(maxSal)
                medianSal = numpy.median(tempSalaryList)
                rowList.append(medianSal)
                writer.writerow(rowList)
                rowList = []
                
    def writeSourcetoCSV(self):
        with open('Source.csv', mode='w') as outfile:
            writer = csv.writer(outfile, lineterminator='\n')
            rowList = []
            for source in self._sourceDict:
                tempSalaryList = self._sourceDict[source]
                rowList.append(source)
                minSal = min(tempSalaryList)
                rowList.append(minSal)
                maxSal = max(tempSalaryList)
                rowList.append(maxSal)
                medianSal = numpy.median(tempSalaryList)
                rowList.append(medianSal)
                writer.writerow(rowList)
                rowList = []
        
if __name__ == "__main__":
    start_time = time.time()
    feat = CategoryFeature()
    print time.time() - start_time, "seconds"
