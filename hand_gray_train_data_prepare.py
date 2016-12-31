import os
import sys
sys.path.append('../')
import cv2
import handclstor_data_prepare as dt
import randomcrop 
import random
import model_generator.projectroot as prt
import transformation as tf 
proot = prt.project_dir

cls_data_root = os.path.join(proot,"MorpxData","classification")

targetname="hands"

target_cls_data_root = os.path.join(cls_data_root,"hands")

sample_map={

	"positive":	[
			"sayHiPost"
				],
	"negative":	[
			"animal",
			"background",
			"crowd",
			"home",
			"humanbody",
			"interior",
			"Male",
			"stuff",
			"workingplace",
			"cropfromhumanbody"	
				]


}


#crop from human body

print "crop from human body"
#croproot = os.path.join(target_cls_data_root,"cropfromhumanbody")

#if not os.path.isdir(croproot):
#	os.mkdir(croproot)

#size = 4
#sub_train_root = croproot
#hbroot = os.path.join(target_cls_data_root,"humanbody")

#for img in os.listdir(hbroot):
#	n=random.randrange(0,size)
	

	#if n==0:
#		im_path=os.path.join(hbroot,img)
#		
#		randomcrop.randomcrop(im_path,size,sub_train_root)

print "crop finish"

#balance data


print "balancing data"
psample_size=250000

nsample_size=0
for nsample in sample_map['negative']:
	nsample_size+=len(os.listdir(os.path.join(target_cls_data_root,nsample )))

print "total nsample size: "+str(nsample_size)


sample_step = nsample_size*6/psample_size


print "sample_step: "+str(sample_step)

#prepare positive and negative sample

image_db = os.path.join(target_cls_data_root,"train_gray")

plist=[]
nlist=[]

def nsample_condition(img):

	n=random.randrange(0,sample_step)
	if n==0:
		return True
	else:
		return False
def psample_condition(img):
	return True

for key in sample_map.keys():
		
		
	
	for sample in sample_map[key]:
	
		if key=="positive":
	                copy=20
			pimg_root = os.path.join(target_cls_data_root,sample)
        	        sublist = dt.get_sub_img(pimg_root,pcondition=psample_condition)
			print "preparing positive sample with total "+str(len(sublist))
        	if key=="negative":
                	copy=1
			nimg_root = os.path.join(target_cls_data_root,sample)
                	sublist = dt.get_sub_img(nimg_root,ncondition=nsample_condition)
			print "preparing negative sample with total "+str(len(sublist))
		for image in sublist:
			#print image
			imgname= os.path.splitext(os.path.basename(image))[0]
			rawimg =tf.toGray( cv2.imread(image) )
			
			
				
			hfimg,vfimg,mrimg,rrimg,rlimg = dt.transform(rawimg)
	        	transdic={"":rawimg,"hflip":hfimg,"vflip":vfimg,"mr":mrimg,"rr":rrimg,"rl":rlimg}
			for transkey in transdic.keys():
				for i in xrange(copy):
	                        	pretrain_img=cv2.resize(transdic[transkey],(30,30))
	                        	imgPath=os.path.join(image_db,imgname+"_"+key+"_"+transkey+str(i)+".jpg")
	                        	cv2.imwrite( imgPath,pretrain_img)
	                        	if key == "positive":
						plist.append(imgPath)

						if len(plist)%1000==0:
							print str(len(plist))+" finished"
					if key == "negative":
						nlist.append(imgPath)
						if len(nlist)%1000==0:
							print str(len(nlist))+" finished"
trainlist,testlist = dt.creat_train_test_list(plist,nlist,0.7)

print "total positive size: "+str(len(plist))
print "total negative size: "+str(len(nlist))

print "training size: "+str(len(trainlist))
print "testing size: " +str(len(testlist))

dt.writeToFile(trainlist,"/opt/henry/model_generator/models/hand_classifytor/hand_train_gray.data",'w')
dt.writeToFile(testlist,"/opt/henry/model_generator/models/hand_classifytor/hand_test_gray.data",'w')




 
