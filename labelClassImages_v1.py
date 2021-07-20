'''
labelClassImages
Reads in feature file with classes, loads each image, adds class prefix to image name, saves in new directors
For example if image 23 is class 2, the original image "23.tif" is copied to the new file as "2_23.tif"

Tom Zimmerman, IBM Research-Almaden, Center for Cellular Construction

v1 7/20/21
This material is based upon work supported by the NSF under Grant No. DBI-1548297.  
Disclaimer:  Any opinions, findings and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the National Science Foundation
'''

from pathlib import Path
from os import listdir,rename
from os.path import isfile, join
import random
import cv2

# define directories (for Win PC)
inDir=r'C:\Code\A_BlakeRiggs\images\\'          # where orininal images are stored
outDir=r'C:\Code\A_BlakeRiggs\classImages\\'    # where to put class labeled images
classFile=r'C:\Code\A_BlakeRiggs\eyeFeaturesCluster_v1.csv'
IMAGE_NUMBER=0; CLASS=6; # index into class table

# open class file
f = open(classFile, "r")
skipHeader=1 # flag to skip header
# for every image, add class prefix and save in outDir
for line in f:
    if skipHeader:
        skipHeader=0
    else:
        a=line.split(',')
        imageNumber=a[IMAGE_NUMBER][:-2]  # get rid of decimal point
        imageClass=a[CLASS][:-3] # get rid of decimal point and carrage return
        print(imageNumber,imageClass)
        imageReadName=inDir+imageNumber+'.tif'
        imageWriteName=outDir+imageClass+'_'+imageNumber+'.tif'
        im = cv2.imread(imageReadName)  # load image
        cv2.imwrite(imageWriteName,im)  # save image
f.close()
