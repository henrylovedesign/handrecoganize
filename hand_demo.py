import cv2

import sys
import os
import checkmodel as cm
import random
import numpy as np
import time

deplot_root="/opt/henry/model_generator/models/hand_classifytor/deploy"
caffemodel_root="/opt/henry/model_generator/models/hand_classifytor/caffemodels"
demo_root = "/opt/henry/model_generator/models/hand_classifytor/demo_result/"

def generate_window(num,imsize):
	win=[]
	for i in xrange(num):
		xmin = random.randrange(0,imsize[0]/2)
		ymin = random.randrange(0,imsize[1]/2)
		
		w = random.randrange(50,imsize[0]-xmin)

		ratio = random.uniform(0.9,1)
		h= int(ratio*w)
		xmax = xmin+w
		ymax = ymin+h
		win.append([xmin,ymin,xmax,ymax])

	return win

def main(argv=None):
        if argv==None:
            argv=sys.argv
        caffemodelname = argv[1]
          
        camera = cv2.VideoCapture(0)

        grabbed, image = camera.read()

        imsize=image.shape[0:2]
        winnum=4000
        windows = generate_window(winnum,imsize)
        os.system("rm "+demo_root+"*")

	net_definition =os.path.join(deplot_root,"22cnet.prototxt")
	weights=os.path.join(caffemodel_root,caffemodelname)


	model = cm.load_model(net_definition,weights)

        capindex=0
        
        test_batch =  np.empty((winnum,30, 30, 3))

	while True:
                
		grabbed, image = camera.read()

                start = time.time()               
                for i in xrange(winnum):
                    cor = windows[i]
                    test_batch[i,:,:,:] = cv2.resize(image[cor[1]:cor[3],cor[0]:cor[2]],(30,30))
                print test_batch.shape
                print time.time()-start
                
                start=time.time()
                score = cm.score(model,test_batch)
                print time.time() - start
                maxscore=max(score)
                if maxscore>0.991:
                    maxindex = score.index(maxscore)
                    win = windows[maxindex ]
                    
                    cv2.imwrite(os.path.join(demo_root,"capture"+str(capindex)+"_"+str(maxscore)+".jpg"),image[win[1]:win[3],win[0]:win[2]])
                    cv2.rectangle(image, (win[0], win[1]), (win[2], win[3]), (255, 255, 255), 2)
                    cv2.putText(image,"Hello Hand: "+str(maxscore), (win[0],win[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255))
                    capindex+=1
                cv2.imshow("detect hand",image)
                                
		key =  cv2.waitKey(30)
            
		if key==27:
			cv2.destroyAllWindows()
			camera.release()
			break
                

if __name__ == '__main__':
	main()
