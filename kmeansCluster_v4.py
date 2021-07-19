'''
kmeansCluster_v4.py
Reads in feature file, removes non-feature columns, applies PCA to reduce to 3 dimensions,
Performs clustering and plots in 3d scatter.

Tom Zimmerman, IBM Research-Almaden, Center for Cellular Construction

V4 7/19/21 Edited for new eye dataset (removed repeated images)
V3 7/15/21 Add cluster number to imageFeatures.csv file and save as new file
V2 7/15/21
This material is based upon work supported by the NSF under Grant No. DBI-1548297.  
Disclaimer:  Any opinions, findings and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the National Science Foundation
'''

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from sklearn import decomposition
from sklearn.cluster import KMeans

inFile=r'C:\Code\A_BlakeRiggs\eyeFeatures_v1.csv'
outFile=r'C:\Code\A_BlakeRiggs\eyeFeaturesCluster_v1.csv'
IM_NUM=0; FIRST_FEATURE=1; MAX_FEATURE=5; 
outHeader='imageNumber,ommatidia_count,follicle_count,socket_shape,ommatidia_merging,depression,class' 


# create array just of 5 features
data=np.loadtxt(inFile,delimiter=',',skiprows=1) # load feature file
print('Loaded data shape',data.shape)

# Cluster
featureArray=data[:,FIRST_FEATURE:FIRST_FEATURE+MAX_FEATURE]
K = KMeans(n_clusters=5, random_state=0).fit(featureArray)
K.fit(featureArray)                           # Compute k-means clustering

# Predict cluster using K-mean on features
predict=K.fit_predict(featureArray)           # Predict the closest cluster each sample in X belongs to.
inertia=K.inertia_
iterations=K.n_iter_
print('Inertia',int(inertia+0.5))
cluster=predict[:] # assign cluster to predicted class

# Add clusters to data file and save as new file
axis=1;     #0=row, 1=column
print('Shape of data before adding cluster column',data.shape)
cluster2D=np.zeros((len(cluster),1))
cluster2D[:,0]=cluster
dataCluster = np.append(data, cluster2D, axis)
print('Shape of dataCluster after adding cluster column',dataCluster.shape)
np.savetxt(outFile,dataCluster,delimiter=',',header=outHeader,fmt='%1.1f')

