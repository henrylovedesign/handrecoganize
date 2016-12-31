import os
import cv2

sub_train_root = "/opt/henry/model_generator/MorpxData/classification/hands/handdetection"

def crop(gtbox_root,img_root):

	for filename in os.listdir(gtbox_root):
		
		im_name =os.path.splitext( os.path.splitext(filename)[0] )[0]

		im_path = os.path.join(img_root,im_name+".jpg")
		im = cv2.imread(  im_path  )

		gtboxes = [line.strip().split(" ") for line in open( os.path.join( gtbox_root,filename ) ,'r')]	
		index=0
		for box in gtboxes:

			xmin =int( box[0])
			ymin =int( box[1])
			xmax =int( box[2])+xmin
			ymax =int( box[3])+ymin
			hand = im[ymin:ymax,xmin:xmax]

			hand_name = im_name+"_"+str(index)+".jpg"

			hand_path = os.path.join(sub_train_root,hand_name)	

			cv2.imwrite(hand_path,hand)



def main():
	gtbox_root = '/opt/henry/model_generator/MorpxData/VOC2007plus/clsGTBox/hand'

	img_root = '/opt/henry/model_generator/MorpxData/VOC2007plus/clsImages'


	crop(gtbox_root,img_root)


if __name__ == '__main__':
	main()
