import os
import cv2
import random

def randomcropones(im):

        h,w = im.shape[0::2]

        xmin = int(random.uniform(0,int(0.75*w)))
        ymin = int(random.uniform(0, int(0.75*h) ) )

        cw = int(random.uniform(1,w-xmin))
        ch = int(random.uniform(1,h-ymin))


        size = min(cw,ch)

        crop=im[ymin:ymin+size,xmin:xmin+size]
	cor = [xmin,ymin,xmin+size,ymin+size]

        return crop,cor



def randomcrop(im_path,num,sub_train_root):

	image = cv2.imread(im_path)

	h,w,d = image.shape
	#print h
	for i in xrange(num):
		xmin = int(random.uniform(0,int(0.75*w)))

		ymin = int(random.uniform(0, int(0.75*h) ) )

		cw = int(random.uniform(1,w-xmin))

		ch = int(random.uniform(1,h-ymin))
		
		#size = min(h-ymin,w-xmin)	
		size = min(cw,ch)	
		#print size
		crop=image[ymin:ymin+size,xmin:xmin+size]
		#print crop	
		cropname = os.path.splitext( os.path.basename(im_path) )[0]+"_"+str(i)+".jpg"

		croppath = os.path.join(sub_train_root,cropname)
		
		cv2.imwrite(croppath,crop)

		#print "save"

def main():

	im_root = '/opt/henry/model_generator/MorpxData/classification/hands/ForTrain/negative/rawVOC'
	for im in os.listdir(im_root):
		#if im.startswith('00'):			
			im_path = os.path.join( im_root,im  )
			#print im
			#num = random.randrange(1,20)
			num=4

			sub_train_root = '/opt/henry/model_generator/MorpxData/classification/hands/ForTrain/negative/rcropVOC' 
			#sub_train_root = im_root
			randomcrop(im_path,num,sub_train_root)


if __name__ == '__main__':
	main()
		
