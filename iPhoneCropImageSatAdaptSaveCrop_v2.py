'''
iPhoneCropImageSatAdaptSaveCrop
Find eye and crop image using threshold of saturation
Thresh is set adaptivly by measuring % of on pixels after thresholding altering thresh level to keep % pix on within a range
If more than one object has acceptable area, pick one closest to the center of the image
Save cropped image

Tom Zimmerman, IBM Research-Almaden, Center for Cellular Construction

V1 7/16/21 
This material is based upon work supported by the NSF under Grant No. DBI-1548297.  
Disclaimer:  Any opinions, findings and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the National Science Foundation
'''
import cv2
from os import listdir,rename
from os.path import isfile, join
import numpy as np
from statistics import median
import math

############ PUT YOUR IMAGE DIRECTORY HERE ##################
imageDir=r'C:\Users\ThomasZimmerman\Pictures\CCC_Riggs\iPhone\MRD_A_jpg\\' # image location
saveDir=r'C:\Users\ThomasZimmerman\Pictures\CCC_Riggs\iPhone\Crop2\\'     # directory for saving cropped images
cropPrefix='MRD_Crop_'
badCropPrefix='BAD_MRD_Crop_'

##imageDir=r'C:\Users\ThomasZimmerman\Pictures\CCC_Riggs\iPhone\SV_jpg\\' # image location
##saveDir=r'C:\Users\ThomasZimmerman\Pictures\CCC_Riggs\iPhone\Crop2\\'     # directory for saving cropped images
##cropPrefix='SV_Crop_'
##badCropPrefix='BAD_SV_Crop_'

##imageDir=r'C:\Users\ThomasZimmerman\Pictures\CCC_Riggs\iPhone\OreoWT_jpg\\' # image location
##saveDir=r'C:\Users\ThomasZimmerman\Pictures\CCC_Riggs\iPhone\Crop2\\'     # directory for saving cropped images
##cropPrefix='OreoWT_Crop_'
##badCropPrefix='BAD_OreoWT_Crop_'

##imageDir=r'C:\Users\ThomasZimmerman\Pictures\CCC_Riggs\iPhone\WT_jpg\\' # image location
##saveDir=r'C:\Users\ThomasZimmerman\Pictures\CCC_Riggs\iPhone\Crop2\\'     # directory for saving cropped images
##cropPrefix='WT_Crop_'
##badCropPrefix='BAD_WT_Crop_'

SCALE=(320,240)     # display resolution
#PIX_MAX=0.060       # servo thresh to keep % pix on within this value
#PIX_MIN=0.055       # servo thresh to keep % pix on within this value
PIX_MAX=0.070       # servo thresh to keep % pix on within this value
PIX_MIN=0.065       # servo thresh to keep % pix on within this value
MAX_COUNT=10        # don't iterlate more than this number of times
THRESH_START=160    # starting value for thresh
STEP=2              # thresh increment size per loop
THICK=50            # bounding box line thickness
MIN_AREA=5         # min good obj area (percent * 1000)
MAX_AREA=80         # max good obj area
ksize = (128,128)   # blur kernal 
EXPAND=500          # number of pix to add to crop boundary to capture entire eye
################################ FUNCTIONS #####################################
def doContour(im):
    detectState=0; # assume bad image
    # find eye as object with proper size and near the center of the image
    xx0=0; xx1=0; yy0=0; yy1=0; 
    (yRez,xRez)=im.shape
    imArea=xRez*yRez
    xcIM=xRez/2; ycIM=yRez/2; # find center of image
    dMin=99999.0  # distance of object from center, used if several objects detected, initialize really big so min will be detected
    dummy,contourList, hierarchy = cv2.findContours(im, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) # all countour points, uses more memory
    for objContour in contourList:
        # Get bounding box for ROI
        PO = cv2.boundingRect(objContour)
        x0=PO[0]; y0=PO[1]; x1=x0+PO[2]; y1=y0+PO[3]; xc=x0+(x1-x0)/2; yc=y0+(y1-y0)/2;

        # check if object is good size
        area = int(1000*cv2.contourArea(objContour)/imArea)
        if area>MIN_AREA and area<MAX_AREA:
            detectState=1 # indicate that valid object detected
            #print('good area',area)
            # check to see if close to center, in case more than one object detected
            xc=x0+(x1-x0)/2; yc=y0+(y1-y0)/2 # find center of object
            d=math.sqrt((xcIM-xc)**2 + (ycIM-yc)**2)
            if d<dMin:
                cv2.rectangle(im, (x0,y0), (x1,y1), 128, THICK) # place GRAY rectangle around candidate
                #print('Closer dx:',xcIM-xc,'dy:',ycIM-yc,'dMin',dMin,'d',d)
                dMin=d # update min in case there is another object to evaluate
                xx0=x0; xx1=x1; yy0=y0; yy1=y1;
        else:
            print('Reject area:',area)
    if detectState==1:
        cv2.rectangle(im, (xx0,yy0), (xx1,yy1), 255, THICK) # place WHITE rectangle around good object
    return(im,detectState,xx0,yy0,xx1,yy1)

def expandBox(xRez,yRez,x0,y0,x1,y1):
    x0 = np.clip(x0-EXPAND, 0,xRez-1)
    x1 = np.clip(x1+EXPAND, 0,xRez-1)
    y0 = np.clip(y0-EXPAND, 0,yRez-1)
    y1 = np.clip(y1+EXPAND, 0,yRez-1)
    return(x0,y0,x1,y1)

################################ MAIN ##########################################
                   
# find and process all images in dir
files = [f for f in listdir(imageDir) if isfile(join(imageDir, f))]
thresh=THRESH_START
for fileName in files:
    rawColorIM=cv2.imread(imageDir+fileName)   # read in color image
    rawIM=cv2.cvtColor(rawColorIM, cv2.COLOR_BGR2GRAY) # read in as grayscale image
    cv2.imshow('Original',cv2.resize(rawColorIM,SCALE))

    hsvIM = cv2.cvtColor(rawColorIM, cv2.COLOR_BGR2HSV)
    satIM=hsvIM[:,:,1]
    (yRez,xRez)=satIM.shape
    cv2.imshow('Saturation',cv2.resize(satIM,SCALE))
    blurIM = cv2.blur(satIM, ksize, cv2.BORDER_DEFAULT) 
    
    # servo threshold until a good percentage of pixels are deteected
    count=0;
    while count<MAX_COUNT:
        ret,threshIM= cv2.threshold(blurIM,thresh,255,cv2.THRESH_BINARY)
        pix=round(np.sum(threshIM)/(xRez*yRez*255),3)
        if pix>PIX_MAX:
            thresh+=STEP
        elif pix<PIX_MIN:
            thresh-=STEP
        else:
            break # within range so quit servoing
        if thresh>255 or thresh<0:  # if thresh out of range, reset and quit
            thresh=THRESH_START
            break
        count+=1
    print('thresh',thresh,'loop count',count,'pix',pix)
    
    # find eye as object with proper size and near the center of the image
    (im,detectState,x0,y0,x1,y1)=doContour(threshIM)

    # save cropped image
    if detectState==1: # don't save if detectState is good
        outName=saveDir+cropPrefix+fileName
    else:
        outName=saveDir+badCropPrefix+fileName
    (x0,y0,x1,y1)=expandBox(xRez,yRez,x0,y0,x1,y1)
    cropIM=rawIM[y0:y1,x0:x1]
    cv2.imwrite(outName,cropIM)
    print('saved image',outName)
    cv2.imshow('Save',cv2.resize(cropIM,SCALE))
    cv2.imshow('Detect',cv2.resize(im,SCALE))
    print()

    # read keyboard and quit if 'q'
    key=cv2.waitKey(10) & 0xFF
    if key == ord('q'):
        break
    
cv2.destroyAllWindows()
