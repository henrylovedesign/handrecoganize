import cv2
import os
import transformation

def toGray(img_root,spath):
	for img in os.listdir(img_root):
		gimg = transformation.toGray(cv2.imread(   os.path.join(img_root,img)        ))
		invgimg = transformation.invert(gimg)
		gimg = cv2.resize(gimg,(30,30))
		invgimg = cv2.resize(invgimg,(30,30))
		cv2.imwrite(os.path.join(spath,img ),gimg)
		cv2.imwrite(os.path.join(spath,img.split(".")[0]+"_invert.jpg"),invgimg )

if __name__ == '__main__':

	img_root='/opt/henry/model_generator/MorpxData/classification/testImage/' 
	spath = '/opt/henry/model_generator/MorpxData/classification/hands/test'

	toGray(img_root,spath) 

