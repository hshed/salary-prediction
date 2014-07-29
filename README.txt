ASSIGNMENT #2 SUBMITTED BY HRISHIKESH KUMAR (10010817)
============================================================

============================================================
PACKAGES AND LIBRARIES USED 
============================================================
Python v2.7
Numpy, Scipy, and Scikit learn

============================================================
IMPORTANT NOTES
============================================================
# Name the training file Training.csv and test file Test.csv

# Either put all files into your installation directory of 
Python or you must have your PATH set in your environment.

# On 4GB RAM i3 processor, it rakes less than 120 seconds 
in feature extraction and creating sparse matrix.

============================================================
FEATURE EXTRACTION
============================================================
# Run Feature.py to extract features into csv file. You get 
the following csv files:

-> Company.csv : it contains unique company with min, max
and median salaries.

-> LocationAndSalary.csv : it contains unique locations with 
min, max and median salaries

-> IdfList.csv : it contains word list with their idf

-> TimeAndTerm.csv : it contains columns with time and term 
of the job with row number corresponding to respective 
document number. I have assigned 1 to full time job, -1 to 
part time and 0 to jobs with no time given. Similar 
assigning has been done with job term.

-> Source.csv : it contains unique sources. The salaries in 
this file has not been used in the program.

->CategoryAndSalary.csv : it contains unique categories. The
 salaries in this file have not been used in the program.

# Run CreateSparce.py file. It retrieves the dictionary from
Dictionary.py and other different variables required for 
creating sparse matrix. The sparse matrix is created with name
spm.pkl in the src/main folder of your workspace.

=============================================================
TRAINING
=============================================================
# There are two .py files for Training namely SVReg.py and RFReg.py.
SVReg.py uses sklearn svm package to generate traning models 
using SVR. RFReg.py uses sklearn RandomForestRegressor to generate
training models using Random Forest Regession Technique.

# Running SVReg.py will generate models by first splicing the sprase
matrix along row into smaller matrices. The models are saved with 
name 'SV i.pkl' where i is the ith model number. 

NOTE: I have already created the models on the whole document. It
took about 10 hours since SVR technique has almost quadratic 
time complexity.

# Running RFReg.py will generate models by first splicing the sarse
matrix alogn row into smaller matrices. The models are saved with
name 'RF i.pkl' where i is the ith model number.

NOTE: I have already created the models on the whole document. It
took about 2 hours.

============================================================
TESTING
============================================================
# To extract features from Test.csv first run TestFile.py. It
extracts all the necessary features required.

# To create the sparse matrix of Test data, run 
CreateTestSparse.py. The sparse matrix is created with name
testspm.pkl in the src/main folder of your workspace.

# The models are saved in the main directory. For SVR, run 
SVRTest.py. For, Random Forest, run RFTest.py

============================================================
DROPBOX FILES
============================================================
Find the trained models in this link : 
Extract all the models (not the folder) into the same directory as extracted files from moodle.
