'''
imageViewThreshEdgeHSV
Loads one image, display edge, HSV, RGB and several threshold methods of image
Uses keyboard to dynamically change method parameters

Tom Zimmerman, IBM Research-Almaden, Center for Cellular Construction

V1 7/15/21 
This material is based upon work supported by the NSF under Grant No. DBI-1548297.  
Disclaimer:  Any opinions, findings and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the National Science Foundation
'''
import cv2
import numpy as np

############ PUT YOUR IMAGE HERE ##################
image1=r'C:\Users\ThomasZimmerman\Pictures\CCC_Riggs\iPhone\OreoWT_jpeg\IMG_4818.jpg' # image location

SCALE=(320,240)     # display resolution

# keyboard variable setup and initial values
keyState=0;
key=0;
keyBuf=np.zeros((256),dtype=int)
keyBuf[ord('t')]=90     # quantization threshold
keyBuf[ord('e')]=5      # canny low thresh
keyBuf[ord('E')]=30     # canny high thresh
keyBuf[ord('k')]=10     # kernal size (*2 + 1)   
keyBuf[ord('T')]=2      # threshold for adaptive 

############# Funcions #################
def processKey(key):
    global keyState;

    if key==ord('='):
        keyBuf[keyState]+=1
    elif key==ord('+'):
        keyBuf[keyState]+=10
    elif key==ord('-'):
        if keyBuf[keyState]>0:
            keyBuf[keyState]-=1
    elif key==ord('_'):
        if keyBuf[keyState]>10:
            keyBuf[keyState]-=10
    else:
        keyState=key
    print (chr(keyState),'=',keyBuf[keyState])
    return

def title():
    print('Keyboard Controls')
    print('Click on any image to direct key activity to program')
    print('Press key to select parameter')
    print('Push + and - keys to change value')
    print('Hold shift while pressing + or - to change value by increments of 10')
    print()
    print('Key Parameter')
    print('=== =========')
    print('t quantization threshold')
    print('e Canny low threshold')
    print('E Canny high threshold')
    print('k kernal size')    
    print('T threshold for adaptive')
    print('q to quit program')
    
################################ MAIN ##########################################
title()                         # display instructions
rawColorIM=cv2.imread(image1)   # read in color image
rawIM=cv2.cvtColor(rawColorIM, cv2.COLOR_BGR2GRAY) # read in as grayscale image
(x,y)=rawIM.shape
run=1
while(run):

    # read keyboard and update variables
    key=cv2.waitKey(10) & 0xFF
    if key == ord('q'):
        run=0
    if key!=255:
        processKey(key)
    thresh=keyBuf[ord('t')]
    eLow=keyBuf[ord('e')]
    eHigh=eLow+keyBuf[ord('E')]
    kernalSize=2*keyBuf[ord('k')]+1
    threshAdapt=keyBuf[ord('T')]
    
    edgeIM = cv2.Canny(rawIM,eLow,eHigh)
    cv2.imshow('edge',cv2.resize(edgeIM,SCALE))
    
    ret,th1= cv2.threshold(rawIM,thresh,255,cv2.THRESH_BINARY_INV)
    cv2.imshow('THRESH_BINARY_INV',cv2.resize(th1,SCALE))

    ret,th2 = cv2.threshold(rawIM,thresh,255,cv2.THRESH_TRUNC)
    cv2.imshow('THRESH_TRUNC',cv2.resize(th2,SCALE))

    ret,th3 = cv2.threshold(rawIM,thresh,255,cv2.THRESH_TOZERO_INV)
    cv2.imshow('THRESH_TOZERO_INV',cv2.resize(th3,SCALE))

    th4 = cv2.adaptiveThreshold(rawIM,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,kernalSize,threshAdapt)
    cv2.imshow('ADAPTIVE_THRESH_MEAN',cv2.resize(th4,SCALE))

    th5 = cv2.adaptiveThreshold(rawIM,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,kernalSize,threshAdapt)
    cv2.imshow('ADAPTIVE_THRESH_GAUSSIAN',cv2.resize(th5,SCALE))

    cv2.imshow('Original Color',cv2.resize(rawColorIM,SCALE))
    cv2.imshow('Original Gray',cv2.resize(rawIM,SCALE))

    cv2.imshow('Red',cv2.resize(rawColorIM[:,:,2],SCALE))
    cv2.imshow('Green',cv2.resize(rawColorIM[:,:,1],SCALE))
    cv2.imshow('Blue',cv2.resize(rawColorIM[:,:,0],SCALE))
	
    hsvIM = cv2.cvtColor(rawColorIM, cv2.COLOR_BGR2HSV)
    cv2.imshow('Hue',cv2.resize(hsvIM[:,:,0],SCALE))
    cv2.imshow('Saturation',cv2.resize(hsvIM[:,:,1],SCALE))
    cv2.imshow('Value',cv2.resize(hsvIM[:,:,2],SCALE))

cv2.destroyAllWindows()
