import os
import random
import cv2
import transformation as tf
def get_sub_img(image_root,pcondition=None,ncondition=None):
	
	plist=[]
	nlist=[]
	for img in os.listdir(image_root):
		if pcondition is not None:
			if pcondition(img) == True:
				plist.append(os.path.join(image_root,img))

		if ncondition is not None:
			if ncondition(img) == True:
				nlist.append(os.path.join(image_root,img))
	if pcondition!=None and ncondition==None:
		return plist


	if pcondition==None and ncondition!=None:
		return nlist

	if pcondition!=None and ncondition!=None:
		return plist,nlist


def creat_train_test_list(plist,nlist,ratio):
	
	random.shuffle(plist)
	random.shuffle(nlist)

	plen = len(plist)
	nlen = len(nlist)

	plist = [" ".join([image,"1"]) for image in plist]
	nlist = [" ".join([image,"0"]) for image in nlist]
	
	trainlist = plist[0:int(plen*ratio)]+nlist[0:int(nlen*ratio)]
	testlist =  plist[int(plen*ratio):]+nlist[int(nlen*ratio):]
	
	random.shuffle(trainlist)
	random.shuffle(testlist)
	
	return trainlist,testlist



def writeToFile(listarray,filepath,state):
	if state=='w':
		with open(filepath,'w') as f:
			f.write("\n".join(listarray))
	if state=='a':
		with open(filepath,'a') as f:
                        f.write("\n".join(listarray))



def transform(img):


	return tf.horizon_flip(img),tf.vertical_flip(img),tf.mirror(img),tf.rotater(img),tf.rotatel(img),tf.toGray(img)



def main():
	


	def pcondition2(img):

		return True
	def pcondition(img):
		if 'Hand' in img:
			return True

		else:
			return False

	def ncondition(img):

		return img.startswith('00')	 

	def pcondition3(img):
		return not img.startswith('00')

	def ncondition2(img):
		return True
	




	
	pimg_root1="/opt/henry/model_generator/MorpxData/classification/hands/backup/HandImage"
	pimg_root7='/opt/henry/model_generator/MorpxData/classification/hands/sayHiPost' 
	
	

	
	nimg_root1='/opt/henry/model_generator/MorpxData/classification/hands/humanbody/pos32K'
	nimg_root2="/opt/henry/model_generator/MorpxData/classification/hands/background/VOC2007"
	nimg_root3='/opt/henry/gender/GenderData/Combined1And3_old/Male' 
	nimg_root4='/opt/henry/gender/GenderData/Combined1And3_old/Female'
	nimg_root5="/opt/henry/model_generator/MorpxData/classification/hands/background/crowd"

	

	image_db = "/opt/henry/model_generator/MorpxData/classification/hands/train4"
	
	
	plist1= get_sub_img(pimg_root1,pcondition=pcondition2)
	#plist2= get_sub_img(pimg_root2,pcondition=pcondition2)
	#plist3= get_sub_img(pimg_root3,pcondition=pcondition2)	
	#plist4= get_sub_img(pimg_root4,pcondition=pcondition2)
	#plist5= get_sub_img(pimg_root5,pcondition=pcondition2)
	#plist6= get_sub_img(pimg_root6,pcondition=pcondition2)

	plist7= get_sub_img(pimg_root7,pcondition=pcondition2)


	nlist1= get_sub_img(nimg_root1,ncondition=pcondition2)
	nlist2= get_sub_img(nimg_root2,ncondition=pcondition2)
	nlist3= get_sub_img(nimg_root3,ncondition=pcondition2)
	nlist4= get_sub_img(nimg_root4,ncondition=pcondition2)
	nlist5= get_sub_img(nimg_root5,ncondition=pcondition2)


	
	plist=[]
	nlist=[]
	


	for p in [plist7,plist1]:
	

		for pimage in p:
			if os.path.basename(pimage)!='thumb.db':
				rawimg = cv2.imread(pimage)

				try:
					transform(rawimg)

				except AttributeError:
					print pimage
	                	invtimg,hfimg,vfimg,mrimg,rrimg,rlimg = transform(rawimg)
	                	dic={"":rawimg,"hflip":hfimg,"vflip":vfimg,"mr":mrimg,"rr":rrimg,"rl":rlimg}
				if p == plist7:
					copy=12

				if p==plist1:
					copy=1
	                	for key in dic.keys():
					for i in xrange(copy):
	                        		image=cv2.resize(dic[key],(30,30))
	                        		imgPath=os.path.join(image_db,os.path.basename(pimage)+"_"+key+str(i))
	                        		cv2.imwrite( imgPath,image)
	                        		plist.append(imgPath)
	
	cutoff=300000
	
	for n in [nlist5[0:15000],nlist1[0:5000],nlist2[0:5000],nlist3[0:5000],nlist4[0:5000]]:
		random.shuffle(n)	
		for nimage in n:
			if os.path.basename(nimage)!='Thumb.db':
				rawimg = cv2.imread(nimage)
				try:
	                                transform(rawimg)
					#rawimg = tf.toGray(rawimg)


					invtimg,hfimg,vfimg,mrimg,rrimg,rlimg = transform(rawimg)
	                        	dic={"":rawimg,"hflip":hfimg,"vflip":vfimg,"mr":mrimg,"rr":rrimg,"rl":rlimg}
	                        	for key in dic.keys():
	                                	image=cv2.resize(dic[key],(30,30))
	                                	imgPath=os.path.join(image_db,os.path.basename(nimage)+"_"+key)
	                                	
	                                	if len(nlist)<=cutoff:
							cv2.imwrite( imgPath,image)

							nlist.append(imgPath)

				except TypeError:
					print nimage
					pass
		


	
	trainlist,testlist = creat_train_test_list(plist,nlist,0.7)
	print len(trainlist)
	print len(testlist)	

	print len(nlist)
	print len(plist)
	writeToFile(trainlist,"/opt/henry/model_generator/models/hand_classifytor/hand_finetune3_train.data",'w')
	writeToFile(testlist,"/opt/henry/model_generator/models/hand_classifytor/hand_finetune3_test.data",'w')
if __name__ == '__main__':

	main()


