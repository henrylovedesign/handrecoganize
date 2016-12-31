import os
import sys
import cv2
import time
# set up Python environment: numpy for numerical routines, and matplotlib for plotting
import numpy as np
import matplotlib.pyplot as plt
# display plots in this notebook
#%matplotlib inline

# set display defaults

rownum = 16
colnum = 10


def vis_square(data):
    pad = 5
    width = data.shape[2]*rownum+(rownum+1)*pad
    height = data.shape[1]*colnum+(colnum+1)*pad

    planar = np.zeros((height,width,3),dtype="uint8")
    print data.shape
    for i in xrange(data.shape[0]):
        row = i%colnum
        col = i/colnum
        #cv2.imshow('test',data[i])
        #cv2.waitKey()
        for rowindex in xrange(90):
            for colindex in xrange(90):
               y= row*(pad+data.shape[1]) +pad + rowindex
               x= col*(pad+data.shape[2]) +pad + colindex
               planar[y,x,:] = data[i,rowindex,colindex,:]

    cv2.imshow("blackboard",planar)
    key = cv2.waitKey()
    return key


def main(argv=None):
    if argv==None:
        argv = sys.argv
    
    if os.path.isfile(argv[1]):
    
        imlist = [path.strip().split(" ")[0] for path in open(argv[1],"r")]
        
    

    if os.path.isdir(argv[1]):
        imlist = [os.path.join(argv[1],imname) for imname in os.listdir(argv[1])]

    
    
    batch = rownum * colnum

    
    
    cur_index=0

    
    key = cv2.waitKey()
    while(key!=27):
        print 'test'
        batchlist = imlist[cur_index:cur_index+batch]
        
        batch_show = np.empty((colnum*rownum,90,90,3),dtype="uint8")
        for i in xrange(len(batchlist)):
            batch_show[i,:,:,:]=cv2.resize(cv2.imread( os.path.join(batchlist[i])   ),(90,90) )


        key=vis_square(batch_show)
        if key==ord('n'):
            cv2.destroyAllWindows
            cur_index+=batch
            key=vis_square(batch_show)
        

if __name__ == '__main__':
    main()




