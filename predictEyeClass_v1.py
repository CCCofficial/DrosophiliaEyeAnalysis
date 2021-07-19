'''
predictEyeClass_v1.py
Reads in feature and class file, divide dataset into training and testing, run several ML algorithms

Tom Zimmerman, IBM Research-Almaden, Center for Cellular Construction

V4 7/19/21 Edited for new eye dataset (removed repeated images)
V3 7/15/21 Add cluster number to imageFeatures.csv file and save as new file
V2 7/15/21
This material is based upon work supported by the NSF under Grant No. DBI-1548297.  
Disclaimer:  Any opinions, findings and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the National Science Foundation
'''

import numpy as np
from sklearn.model_selection import train_test_split
from scipy import stats
from sklearn import preprocessing, neighbors
from sklearn.model_selection import cross_validate
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score, log_loss
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.preprocessing import scale
from sklearn.preprocessing import StandardScaler
#import warnings                        # turn off warnings if you are tired of seeing them
#warnings.filterwarnings("ignore")

inFile=r'C:\Code\A_BlakeRiggs\eyeFeaturesCluster_v1.csv'
IM_NUM=0; FIRST_FEATURE=1; MAX_FEATURE=5; CLASS=5;

# create array just of 5 features
data=np.loadtxt(inFile,delimiter=',',skiprows=1)    # load feature file
print('Loaded data shape',data.shape)
X=data[:,FIRST_FEATURE:FIRST_FEATURE+MAX_FEATURE]   # features
y=data[:,CLASS]                                     # class

# Create train/test 80%/20%
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# create train/test 80%/20%
X = StandardScaler().fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print('trainCount',len(X_train),'testCount',len(X_test))
print('X train shape',X_train.shape,'X test shape',X_test.shape)

# Classify
classifiers = [
    KNeighborsClassifier(10),
    DecisionTreeClassifier(),
    RandomForestClassifier(),
    GaussianNB(),
    LinearDiscriminantAnalysis(),
    QuadraticDiscriminantAnalysis()]

for clf in classifiers:
    try:
        clf.fit(X_train[:,1:], y_train)
        name = clf.__class__.__name__
        train_predictions = clf.predict(X_test[:,1:])
        acc = accuracy_score(y_test, train_predictions)
        print(name,"Accuracy: {:.1%}".format(acc))
    except:
        print('fail',clf)
    
   
          
