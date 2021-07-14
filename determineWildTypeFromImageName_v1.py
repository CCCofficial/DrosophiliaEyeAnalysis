''' Determine if image is wild or mutated based on analyzing terms in file name
Tom Zimmerman, IBM Research-Almaden, Center for Cellular Construction

V1 July 14, 2021
This material is based upon work supported by the NSF under Grant No. DBI-1548297.  
Disclaimer:  Any opinions, findings and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the National Science Foundation
'''

# define directories
inFile=r'C:\Code\A_BlakeRiggs\imageMag.csv' # format imageNumber,imageName,imageMagnification

# open file
f = open(inFile, "r")
data = f.readlines()

# look for terms in spreadsheet
wildImage=[]    # list of wild image numbers
mutImage=[]     #list of mutated image numbers
for i in range(1,len(data)):
    a=data[i].split(',')
    imageNumber=a[0]
    imageName=a[1]
    imageMag=a[2]
    terms=a[1].split('_')
    if 'Wild' in terms and not 'KD' in terms and not 'Knock' in terms:
        wildImage.append(imageNumber)
        #print(imageNumber,'wild',terms)    # print for debugging
    else:
        mutImage.append(imageNumber)               
        #print('          mod',terms)       # print for debugging 
print('Image number of wild-type images (no mutations)')
print(wildImage)

