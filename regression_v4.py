'''
regressopm
A regression returns a continuous value (phenotype severity) predicted by features (image features)
Procedure: Reads in dataset (features and phenotype),split into 80/20 train/test, train regression model, do regression, evaluate performance
Phenotype is scored as follows; 0=Normal,1=Moderate,2=Severe,3=Eyeless. These are continuos values so fractions are allowed.

Tom Zimmerman, IBM Research-Almaden, Center for Cellular Construction

V1 7/21/21 
This material is based upon work supported by the NSF under Grant No. DBI-1548297.  
Disclaimer:  Any opinions, findings and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the National Science Foundation
'''

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import SGDRegressor
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import BayesianRidge
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score
from sklearn.model_selection import train_test_split
from sklearn import linear_model

#y= b0 + b1x    one feature regression 
#y= b0 + b1x + b2x + b3x + b4x   four feature regression (our data)

####################### FILES #########################
# dataset file with image number, features and phenotype
inFile=r'C:\Code\A_BlakeRiggs\imageFeaturePhenotype_v1.csv'
#imageNumber,ommatidia_count,follicle_count,socket_shape,ommatidia_merging ,Phenotype
IM_NUM=0; FIRST_FEATURE=1; MAX_FEATURE=4; PHENOTYPE=5 # index into dataset file

####################### FUNCTIONS ########################
def doReg(name,reg,X_train,y_train,X_test,y_test):
    print('='*10)
    print(name)
    reg.fit(X_train,y_train) # fitting the training data
    y_prediction = reg.predict(X_test)
    score=r2_score(y_test,y_prediction) # predicting the accuracy score
    print('r2 score',round(score,2)) # percent of variation in independen variable accounted for by independent variable
    #print('mean_sqrd_error',round(mean_squared_error(y_test,y_prediction),2))
    #print('root_mean_squared error',round(np.sqrt(mean_squared_error(y_test,y_prediction)),2))
    print('Coefficients',reg.coef_)

######################### MAIN ##########################
# create feature array X and phenotype array y
data=np.loadtxt(inFile,delimiter=',',skiprows=1) # load feature file
print('Loaded data shape',data.shape)
X=data[:,FIRST_FEATURE:FIRST_FEATURE+MAX_FEATURE] # features
#X=data[:,FIRST_FEATURE:FIRST_FEATURE+1] # features
y=data[:,PHENOTYPE] # phenotype

# Create train/test 80%/20%
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print('trainCount',len(X_train),'testCount',len(X_test))
print('X train shape',X_train.shape,'X test shape',X_test.shape)

# Linear Regression
reg = LinearRegression() # creating an object of LinearRegression class
doReg('Linear Regression',reg,X_train,y_train,X_test,y_test)

# Lasso
reg = linear_model.Lasso(alpha=0.1)
doReg('Lasso',reg,X_train,y_train,X_test,y_test)

# Bayesian Ridge Regression
reg = linear_model.BayesianRidge()
doReg('Bayesian Ridge Regression',reg,X_train,y_train,X_test,y_test)
