'''
scatter_PCA_v4.py
Reads in feature file, removes non-feature columns,
applies PCA to reduce to 3 dimensions and plots in 3d scatter.

Tom Zimmerman, IBM Research-Almaden, Center for Cellular Construction

V4 July 15, 2021 Added comments on removing columns
V3 July 15, 2021
This material is based upon work supported by the NSF under Grant No. DBI-1548297.  
Disclaimer:  Any opinions, findings and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the National Science Foundation
'''

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA
from sklearn import decomposition

# load file (you need to change the path to where you put the imageFeature.csv file!
inFile=r'C:\Code\A_BlakeRiggs\Drosophila Eye Images\imageFeatures.csv'
data=np.loadtxt(inFile,delimiter=',',skiprows=1)
IM_NUM=0; MAG=1; EYE_NUM=2; EYE_HAIR=3; EYE_SOCKET=4; EYE_CELL=5; WILD=6; EYE_DEPRESS=7; 

# create array just of 5 features by removing IM_NUM, MAG and WILD columns
print('First row of data as columns are removed')
print('Data shape',data.shape)
print(data[0,:])
axis=1                          # 0=remove row, 1=means remove column
features=np.delete(data,0,axis) # remove IM_NUM.... np.delete(arrayToProcess,pointer to what to remove, axis=what should I remove (row=0,col=1)
print(features[0,:])            # address array as row,col
features=np.delete(features,0,axis) # remove MAG
print(features[0,:])
features=np.delete(features,4,axis) # remove WILD
print(features[0,:])
print('Features shape',features.shape)
print()
EYE_NUM=0; EYE_HAIR=1; EYE_SOCKET=2; EYE_CELL=3; EYE_DEPRESS=4 # new array columns


# do PCA to reduce 5 dimensions to 3 dimensions
print('Features shape before PCA',features.shape)
pca = decomposition.PCA(n_components=3)
pca.fit(features)
pcaFeatures = pca.transform(features)
print('Features shape after PCA',pcaFeatures.shape)
print('Variance ratios',pca.explained_variance_ratio_)

# 3D plot features
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x=pcaFeatures[:,0]
y=pcaFeatures[:,1]
z=pcaFeatures[:,2]
ax.set_xlabel('PCA 0')
ax.set_ylabel('PCA 1')
ax.set_zlabel('PCA 2')

ax.scatter(x, y, z, c='r', marker='o')
plt.show()
