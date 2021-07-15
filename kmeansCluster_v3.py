'''
kmeansCluster_v3.py
Reads in feature file, removes non-feature columns, applies PCA to reduce to 3 dimensions,
Performs clustering and plots in 3d scatter.

Tom Zimmerman, IBM Research-Almaden, Center for Cellular Construction

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

inFile=r'C:\Code\A_BlakeRiggs\Drosophila Eye Images\imageFeatures.csv'
outFile=r'C:\Code\A_BlakeRiggs\Drosophila Eye Images\imageFeaturesCluster.csv'
IM_NUM=0; MAG=1; EYE_NUM=2; EYE_HAIR=3; EYE_SOCKET=4; EYE_CELL=5; WILD=6; EYE_DEPRESS=7; CLUSTER=8;
outHeader='imageNumber,magnification,numberEyeCells,folliclesPerCell,eyeSocketShape,eyeCellMerging,wildType,depression,Cluster' 	 

# create array just of 5 features by removing IM_NUM, MAG and WILD columns
data=np.loadtxt(inFile,delimiter=',',skiprows=1) # load feature file
print('First row of data as columns are removed')
print('Data shape',data.shape)
print(data[0,:])
features=np.delete(data,0,1) # remove IM_NUM
print(features[0,:])
features=np.delete(features,0,1) # remove MAG
print(features[0,:])
features=np.delete(features,4,1) # remove WILD
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

# Cluster
K = KMeans(n_clusters=5, random_state=0).fit(pcaFeatures)
K.fit(pcaFeatures)                           # Compute k-means clustering

# Predict cluster using K-mean on features
predict=K.fit_predict(pcaFeatures)           # Predict the closest cluster each sample in X belongs to.
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

# Display the cluster of wild types
wildIndex=np.where(data[:,WILD]==10)
print('Clusters of Wild type images',cluster[wildIndex])

# 3D plot features
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
x=pcaFeatures[:,0]
y=pcaFeatures[:,1]
z=pcaFeatures[:,2]
ax.set_xlabel('PCA 0')
ax.set_ylabel('PCA 1')
ax.set_zlabel('PCA 2')
ax.scatter(x, y, z, c=cluster, marker='o')
plt.show()

