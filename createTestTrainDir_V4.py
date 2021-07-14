'''
createTestTrainDir_V4
Reads in directory of images. Sorts, shuffles, assigns them numbers, divide and write into train, validate, test directories.
Tom Zimmerman, IBM Research-Almaden, Center for Cellular Construction

V4 July 13, 2021
This material is based upon work supported by the NSF under Grant No. DBI-1548297.  
Disclaimer:  Any opinions, findings and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the National Science Foundation
'''

from pathlib import Path
from os import listdir,rename
from os.path import isfile, join
import random
import cv2

#################### USER DEFINDED VARIABLES ############################
# define directories (for Win PC)
testDir=r'C:\Code\A_BlakeRiggs\testDir\\'
trainDir=r'C:\Code\A_BlakeRiggs\trainDir\\'
verifyDir=r'C:\Code\A_BlakeRiggs\verifyDir\\'
imageDir=r'C:\Users\ThomasZimmerman\Pictures\drosophilaEye\SEM\\'
imageListFileName='imageList.csv'

# define directories (for Mac)
#testDir=r'/Users/TZimmerman/Code/A_BlakeRiggs/testDir/'
#trainDir=r'/Users/Code/A_BlakeRiggs/trainDir/'
#verifyDir=r'/Code/A_BlakeRiggs/verifyDir/'
#imageDir=r'/Users/ThomasZimmerman/Pictures/drosophilaEye/'
#imageListFileName='imageList.csv'

################################### FUNCTIONS ############################
def saveImages(maxCount,outDir,index,f):     
    # save files to directories using interger name
    for i in range(0,maxCount):          
        imageReadFile=imageDir+f[index]
        imageWriteFile=outDir+str(index)+'.tif'
        print('imagePointer',index)
        print('read',imageReadFile)
        print('write',imageWriteFile)
        print()
        im = cv2.imread(imageReadFile)  # load image
        cv2.imwrite(imageWriteFile,im)  # save image
        index+=1
    return(index)

################################### MAIN ############################

# create directories if they don't exist
Path(testDir).mkdir(parents=True, exist_ok=True)
Path(trainDir).mkdir(parents=True, exist_ok=True)
Path(verifyDir).mkdir(parents=True, exist_ok=True)

# create list of all images
files = [f for f in listdir(imageDir) if isfile(join(imageDir, f))]
imageCount=len(files)

# create index for images; 70% 20% 10%
countTrain=int(0.7*imageCount)
countTest=int(0.2*imageCount)
countVerify=int(0.1*imageCount)
countRemain=imageCount-countTrain-countTest-countVerify
countTest+=countRemain
print('Final image train =',countTrain,'verify =',countVerify,'test =',countTest)

# sort and randomize image files, save list
random.seed(46) # seed random number generator
files.sort() # put list in alphabetical order so we know the order
print('imageNameList before shuffle')
print(files[0:3])
random.shuffle(files)
print('imageNameList after shuffle')
print(files[0:3])

# save image number and name
imageNumber=0
with open(imageListFileName, "w") as f:
    f.write('imageNumber,imageName\n')
    for imName in files:
        s=str(imageNumber)+','+imName+'\n'
        f.write(s)
        imageNumber+=1

# save images to folders using imageNumber names
index=0
index=saveImages(countTrain,trainDir,index,files)
index=saveImages(countVerify,verifyDir,index,files)
index=saveImages(countTest,testDir,index,files)

