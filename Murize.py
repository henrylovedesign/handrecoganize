import os
import cv2
import numpy as np
def colorbin(step,val):
    n = (255+1)/step
    bindex = val/step
    bincolor = (bindex*step+bindex*(step+1))/2

    return bincolor

def binarize(im,step):

    data32 = np.asarray(im,dtype = "int32")
    
    h,w,c = data32.shape

    for i in xrange(h):
        for j in xrange(w):
            for k in xrange(c):
                data32[i,j,k]=colorbin(step,data32[i,j,k])

    
    np.clip(data32,0,255,out=data32)
    new_image=data32.astype('uint8')

    return new_image

def main():
    im = cv2.imread("/home/henry/2850.jpg")
    im = binarize(im,2)
    cv2.imshow("test",cv2.resize(cv2.resize(im,(56,36)),(480,300)))
    cv2.waitKey()

if __name__ == '__main__':
    main()
