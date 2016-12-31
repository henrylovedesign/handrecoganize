import os
from random import shuffle
import cv2

def resize(imroot):
    for im in os.listdir(imroot):
        cv2.imwrite(os.path.join(imroot,im) , cv2.resize(cv2.imread(os.path.join(imroot,im)),(29,29))  )

def train_test_split(imroot,trainlist,testlist):
    imnames = os.listdir(imroot)
    
    shuffle(imnames)
    train = imnames[0:1000]

    test = imnames[1000::]

    with open(trainlist,"w") as trf:
        trf.write("\n".join([ " ".join([os.path.join(imroot,imname),"1"]) for imname in train ] )  )

    with open(testlist,"w") as ttf:
        ttf.write("\n".join( [ " ".join( [ os.path.join(imroot,imname),"1"]) for imname in test    ]  ))


imroot = "/home/henry/WarmHole/model_generator/MorpxData/rawData/Mu/train"
trainlist = "/home/henry/WarmHole/model_generator/MorpxData/rawData/Mu/train.data"
testlist = "/home/henry/WarmHole/model_generator/MorpxData/rawData/Mu/test.data"
resize(imroot)
train_test_split(imroot,trainlist,testlist)   
