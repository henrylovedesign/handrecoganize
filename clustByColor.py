import numpy as np
from sklearn.cluster import KMeans
import os
import cv2
def meanRGB(img):
    meanR=np.mean(img[:,:,2])
    meanG=np.mean(img[:,:,1])
    meanB=np.mean(img[:,:,0])

    return np.array([meanR,meanG,meanB])



def kmeans(clustnum,points):
    return KMeans(n_clusters=clustnum,random_state=0).fit(points)


def main():
    root = "/home/henry/WarmHole/model_generator/MorpxData/classification/hands/ForTrain/TrainingSet/BCam2"
    #name = ["betterhand_positive_crop", "hands_positive_crop","myhand2nd_positive_crop", "myhand_positive_crop"]
    name=["Image"]
    points=[]
    imlist=[]
    for sample in name:
        print sample
        imroot=os.path.join(root,sample)
        for im in os.listdir(imroot)[0:3000]:
            imlist.append(os.path.join(imroot,im))
            imarray = cv2.imread(os.path.join(imroot,im))
            h,w,c = imarray.shape
            centerx = int(w/2)
            centery = int(h/2)
            xmin = centerx-w/4
            ymin = centery-h/4
            xmax = centerx+w/4
            ymax = centery+h/4

            fpoint = meanRGB(imarray[ymin:ymax,xmin:xmax])
            #print fpoint
            points.append(fpoint)
    #print points       
    points=np.array(points)
    model = kmeans(9,points)
    print "model"
    
    lables = list(set(model.labels_))
    cluster={}
    for lable in lables:
        cluster[str(lable)]=[]
    for im in imlist:
    
        lable = str(model.predict([meanRGB(cv2.imread(im))])[0])
    
        cluster[lable].append(im)
    
    #print cluster
    for key in cluster.keys():
        with open("/home/henry/WarmHole/model_generator/MorpxData/handcluster/"+key+"_.txt","w") as clt:
            clt.write( "\n".join(cluster[key])  )
        clt.close()

if __name__ == '__main__':
    main()
