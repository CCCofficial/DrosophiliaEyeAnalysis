from pathlib import Path
from os import listdir,rename
from os.path import isfile, join
import random
import cv2

# define directories
testDir=r'C:\Code\A_BlakeRiggs\testDir\\'
trainDir=r'C:\Code\A_BlakeRiggs\trainDir\\'
verifyDir=r'C:\Code\A_BlakeRiggs\verifyDir\\'
imageDir=r'C:\Users\ThomasZimmerman\Pictures\drosophilaEye\\'
imageListFileName='imageList.csv'

# create directories if they don't exist
Path(testDir).mkdir(parents=True, exist_ok=True)
Path(trainDir).mkdir(parents=True, exist_ok=True)
Path(verifyDir).mkdir(parents=True, exist_ok=True)

# create list of all images
imageNameList=[]
files = [f for f in listdir(imageDir) if isfile(join(imageDir, f))]
imageCount=len(files)
print('Image Count =',imageCount)
for i in range(len(files)):
    fileName=files[i]
    imageNameList.append(fileName)

# create index for images; 70% 20% 10%
count70=int(0.7*imageCount)
count20=int(0.2*imageCount)
count10=int(0.1*imageCount)
countRemain=imageCount-count70-count20-count10
print('Initial count70 =',count70,'count20 =',count20,'count10 =',count10,'remain =',countRemain)
count20+=countRemain
print('Final count70 =',count70,'count20 =',count20,'count10 =',count10)

# sort and randomize image files, save list
random.seed(46) # seed random number generator
imageNameList.sort() # put list in alphabetical order so we know the order
print('imageNameList before shuffle')
print(imageNameList[0:3])
random.shuffle(imageNameList)
print('imageNameList after shuffle')
print(imageNameList[0:3])
imageListFileName
# save image number and name
imageNumber=0
with open(imageListFileName, "w") as f:
    f.write('imageNumber,imageName\n')
    for imName in imageNameList:
        s=str(imageNumber)+','+imName+'\n'
        f.write(s)
        imageNumber+=1
        
# save files to directories using interger name
# train images
imagePointer=0
for i in range(0,count70):          
    imageReadFile=imageDir+imageNameList[imagePointer]
    imageWriteFile=trainDir+str(imagePointer)+'.tif'
    print('imagePointer',imagePointer)
    print('read',imageReadFile)
    print('write',imageWriteFile)
    print()
    im = cv2.imread(imageReadFile)  # load image
    cv2.imwrite(imageWriteFile,im)  # save image
    imagePointer+=1
    
# verify images
for i in range(0,count10):          
    imageReadFile=imageDir+imageNameList[imagePointer]
    imageWriteFile=verifyDir+str(imagePointer)+'.tif'
    print('imagePointer',imagePointer)
    print('read',imageReadFile)
    print('write',imageWriteFile)
    print()
    im = cv2.imread(imageReadFile)  # load image
    cv2.imwrite(imageWriteFile,im)  # save image
    imagePointer+=1
    
# test images
for i in range(0,count20):          
    imageReadFile=imageDir+imageNameList[imagePointer]
    imageWriteFile=testDir+str(imagePointer)+'.tif'
    print('imagePointer',imagePointer)
    print('read',imageReadFile)
    print('write',imageWriteFile)
    print()
    im = cv2.imread(imageReadFile)  # load image
    cv2.imwrite(imageWriteFile,im)  # save image
    imagePointer+=1
    
