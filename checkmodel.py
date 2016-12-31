import sys
caffe_root="/opt/henry/model_generator/py-faster-rcnn/caffe-fast-rcnn/"
sys.path.insert(0,caffe_root+"python")
import os
import caffe
caffe.set_mode_gpu()
caffe.set_device(0)

import numpy as np
import cv2
import shutil
import transformation as tf
import random
import math
def load_model(net_definition,weights):

	return caffe.Net(net_definition,weights,caffe.TEST)

def score(net,test_image_batch):

	 transformer = caffe.io.Transformer({'data':net.blobs['data'].data.shape})
         transformer.set_transpose('data',(2,0,1))

         size = test_image_batch.shape[0]

         for i in xrange(size):
         
            net.blobs['data'].data[i]=transformer.preprocess('data',test_image_batch[i])

         output = net.forward()

         #t['ip1']
         #print imname+": "+str(np.argmax(output['ip1']))
         score=[]
         for prob in output['ip1']:
            try:
                score.append(float(math.exp(prob[1]))/(math.exp(prob[0])+math.exp(prob[1])))
            except OverFlowError:
                print "overflow"
                score.append(float(1))
         
	 return score
        
	

def predict_image(net,test_image_batch):

	if type(test_image_batch) == str:
	        imlist = [line.strip() for line in open(test_image_batch,"r")]	
                
                test_image_batch = np.asarry([cv2.imread(impath) for impath in imlist ])
    
		
        
        size = test_image_batch.shape[0]
        transformer = caffe.io.Transformer({'data':net.blobs['data'].data.shape})
	transformer.set_transpose('data',(2,0,1))
        
        for i in xrange(size):
	    
            
            transformed_image = transformer.preprocess('data',test_image_batch[i] )

            net.blobs['data'].data[i]=transformed_image

	output = net.forward()
	
		#t['ip1']
		#print imname+": "+str(np.argmax(output['ip1']))
	index = output['ip1']
        #print 'number of test image:' + str(len(test_image_batch))
        #print 'number of index:' +str(len(index))
        return [np.argmax(prob) for prob in  output['ip1']]




def main():
	

        fp=[]
	net_definition = "/opt/henry/model_generator/models/hand_classifytor/deploy/refineExtCamOnly.prototxt"
	#weights = "/opt/henry/model_generator/base_models/face_owner16/snapshot/finetune2/hand_iter_10000.caffemodel"
	weights='/opt/henry/model_generator/models/hand_classifytor/snapshot_ExtCamOnly/hand__iter_100000.caffemodel'


	hand_lenet = load_model(net_definition,weights)

	#test_img_root = '/opt/henry/model_generator/MorpxData/classification/hands/ForTest/croptempTest'
	#test_img_root = '/opt/henry/model_generator/MorpxData/classification/hands/backup/HandImage/'
	test_img_root='/opt/henry/model_generator/MorpxData/classification/hands/ForTest/positive/camera_palm'
	#test_img_root='/opt/henry/model_generator/MorpxData/classification/hands/ForTest/std_pos/train'




	count = 0
	ncount = 0
	pcount = 0
	tp=0
	tn=0
	train_root='/opt/henry/model_generator/MorpxData/classification/hands'
	#train_sub_root = os.path.join(train_root,os.path.basename(test_img_root))
	train_sub_root = '/opt/henry/model_generator/MorpxData/classification/hands/exp' 
	if not os.path.isdir( train_sub_root+"_p"  ):
		os.mkdir(   train_sub_root+"_p"      )

	if not os.path.isdir(train_sub_root+"_n"):
		os.mkdir(train_sub_root+"_n")
	
	for img in os.listdir(test_img_root):
		index = predict_image(hand_lenet,os.path.join(test_img_root,img))
		if img.startswith('R2D2'):
			pcount+=1
		else:
			ncount+=1
		
		if index==1:
			if img.startswith('R2D2'):
				count+=1
				tp+=1
			shutil.copy(  os.path.join(test_img_root, img),train_sub_root+"_p"  )
		if index==0:
			if not img.startswith('R2D2'):
				count+=1
			
				tn+=1
			shutil.copy(  os.path.join(test_img_root, img),train_sub_root+"_n"  )

	print len(os.listdir(test_img_root ))
	
	print "accuracy: "+ str( float(count)/len(os.listdir(test_img_root)) )
	print "true positive rate: "+str(  float(tp)/pcount )
	print "true negative rate: "+str( float(tn)/ncount )

if __name__ == '__main__':
	main()

	
