import cv2
import numpy as np
from PIL import Image, ImageEnhance
import os
#im0= Image.open('/opt/henry/model_generator/MorpxData/classification/hands/rawData/hands/ResultFrame/2016112510716/320.jpg')
#im1=ImageEnhance.Color(im0).enhance(2.0)
#im2=ImageEnhance.Brightness(im1).enhance(0.1)
#im3=ImageEnhance.Contrast(im2).enhance(10.0)
#im3.show() 
def skinCondition(r,g,b):
	if(
			r>80
		and	g>40
		and	b>20

		and	r>g
		and	r>b
		and	max([r,g,b])-min([r,g,b])>5
		and	abs(r-g)>5
				):
		return True

	else:
		return False

def color_trans(img,alpha,beta,save_root=None,condition=None):
	data32=np.asarray(img,dtype="int32")
	h,w = [data32.shape[0],data32.shape[1]]
	for i in xrange(h):
		for j in xrange(w):
			
			if condition!=None:
				r=data32[i,j,2]
				g=data32[i,j,1]
				b=data32[i,j,0]
				
				if condition(r,g,b):
					data32[i,j,::]=data32[i,j,::]*alpha+beta
			
			if condition==None:
					data32[i,j,::]=data32[i,j,::]*alpha+beta

				
			
			if save_root!=None:
				cv2.imwrite(save_root,new_image)
	
	np.clip(data32,0,255,out=data32)
	new_image=data32.astype('uint8')

	return new_image
def main():
	hand_root='/opt/henry/model_generator/MorpxData/classification/hands/rawData/hands'
	root='/opt/henry/model_generator/MorpxData/classification/hands/rawData/hands/ResultFrame' 
	i=0
	for subdir in os.listdir(root):
		for im in os.listdir(os.path.join(root,subdir)):
			im_path = os.path.join(os.path.join(root,subdir,im) )
			img = cv2.imread(im_path)



			data32=np.asarray(img,dtype="int32")
			h,w = [data32.shape[0],data32.shape[1]]
			for i in xrange(h):
				for j in xrange(w):
			
					r=data32[i,j,2]
					g=data32[i,j,1]
					b=data32[i,j,0]
					if not(
						r>80
					and	g>40
					and	b>20

					and	r>g
					and	r>b
					and	max([r,g,b])-min([r,g,b])>5
					and	abs(r-g)>5
				):
						#print "detected"
						data32[i,j]=[0,0,0]
			
			im_name=os.path.splitext(im)[0]+'_trans'+".jpg"
			
			np.clip(data32,0,255,out=data32)

			new_image=data32.astype('uint8')
			#cv2.imshow('test',new_image)
			#key=cv2.waitKey()
			#print new_image==img
			cv2.imwrite(os.path.join(hand_root,'test',str(i)+subdir+im_name),new_image)
		
			i+=1
			#cv2.imshow('origin',img)
			#cv2.imshow('test',new_image)
			#k=cv2.waitKey()
if __name__ == '__main__':
	
#	alpha_beta=[[1,100],
#				[1.2,-70],
#				[1.2,-30],
#				[1.6,-120],
#				[1.6,-30],				[2.0,80]]


#	img=cv2.imread('/opt/henry/model_generator/MorpxData/classification/hands/rawData/hands/ResultFrame/2016112594355/210.jpg')
#	nimage=color_trans(img,1.6,0)
#	cv2.imshow('origin',img)
#	cv2.imshow('test',nimage)
#	key=cv2.waitKey()

	main()	
