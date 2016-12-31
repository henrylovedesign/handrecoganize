import numpy as np
import cv2
from sklearn.decomposition import PCA
import os
def meanBGR(im):
    meanB=int(np.mean(im[:,:,0]))
    meanG=int(np.mean(im[:,:,1]))
    meanR=int(np.mean(im[:,:,2]))

    return meanB,meanG,meanR

def meanInten(im):
    return np.mean(im)


def substract_mean(im):
    meanB,meanG,meanR = meanBGR(im)
    data32=np.asarray(im,dtype="int32")

    #meanB = np.mean(im)
    #meanG= meanB
    #meanR= meanB
    
    #print meanB,meanG,meanR
    data32[:,:,0]=data32[:,:,0]-meanB
    data32[:,:,1]=data32[:,:,1]-meanG
    data32[:,:,2]=data32[:,:,2]-meanR

    np.clip(data32,0,255,out=data32)
    im=data32.astype('uint8')

    return im

def rgbPCA(imbatch):
    bgr=[]
    for im in imbatch:
        h,w,c=im.shape
        for i in xrange(h):
            for j in xrange(w):
                bgr.append([im[i,j,0],im[i,j,1],im[i,j,2]])
    
    np.array(bgr)

    pca = PCA(n_components=3).fit(bgr)

    return pca.components_,pca.explained_variance_


def perturbation(imbatch):
    
    comp,eigenv = rgbPCA(imbatch)
    pert_batch=[]
    for im in imbatch:
        
        h,w,c = im.shape

        aph1,aph2,aph3 = np.random.normal(0, 0.001, 3)
        #print aph1,aph2,aph3
        p1 = comp[0]
        p2 = comp[1]
        p3 = comp[2]
        pert = p1*aph1*eigenv[0] + p2*aph2*eigenv[1] + p3*aph3*eigenv[2]
        #print pert
        data32 = np.asarray(im,dtype="int32")
        for i in xrange(h):
            for j in xrange(w):
                #print data32[i,j]
                data32[i,j,0]=data32[i,j,0]+int(pert[0])
                data32[i,j,1]=data32[i,j,0]+int(pert[1])
                data32[i,j,2]=data32[i,j,2]+int(pert[2])
                #print data32[i,j]
        np.clip(data32,0,255,out=data32)
        im=data32.astype('uint8')
        pert_batch.append(im)
    return pert_batch 

def main():
    test_impath= "/home/henry/2850.jpg"
    im=cv2.imread(test_impath)
    
    imroot = "/home/henry/WarmHole/model_generator/MorpxData/classification/hands/ForTest/negative/animal"
    imroot2= "/home/henry/WarmHole/model_generator/MorpxData/classification/hands/ForTest/negative/pert_animal"
 
    
    imbatch=[]
    for im in os.listdir(imroot):
        im = cv2.imread(os.path.join(imroot,im))
        new_im=substract_mean(im)
        imbatch.append(new_im)
    
    
    imbatch=np.array(imbatch)
    #print imbatch.shape
    pert_imbatch=perturbation(imbatch)
    pert_im = pert_imbatch
    name=0
    for im in pert_im:
        print im.shape
        cv2.imwrite(os.path.join(imroot2,str(name)+".jpg"),im)
        name+=1
    #print components,eigenvalue



if __name__ == '__main__':
    main()

