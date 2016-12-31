import os
import cv2



def quartercrop(im):
    h,w,c = im.shape

    xmin = w/4
    ymin = h/4
    xmax = 3*w/4
    ymax = 3*h/4

    return im[ymin:ymax,xmin:xmax]

def downcrop(im):

    h,w,c = im.shape

    xmin = w/5
    ymin = 2*h/3
    xmax = 4*w/5
    ymax = h

    return im[ymin:ymax,xmin:xmax]

def sidecrop(im):

    h,w,c = im.shape
    
    xmin = w/8
    ymin = h/3

    xmax = w/2
    ymax = 2*h/3

    return im[ymin:ymax,xmin:xmax]

root = "/home/henry/WarmHole/model_generator/MorpxData/rawData"
imroot="/home/henry/WarmHole/model_generator/MorpxData/rawData/adultFace1"
for imname in os.listdir(imroot):

    im = cv2.imread(os.path.join(imroot,imname  ))
    #cv2.imwrite(os.path.join(root+"/quarterface","quartercrop_"+imname),quartercrop(im))
    #cv2.imwrite(os.path.join(root+"/downface","downcrop_"+imname),downcrop(im))
    cv2.imwrite(os.path.join(root+"/sideface","sidecrop_"+imname),sidecrop(im))







