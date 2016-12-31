import cv2
import numpy as np

import random             


def horizon_flip(img):
	
		return cv2.flip(img,0)
	



def vertical_flip(img):
	return cv2.flip(img,1)



def mirror(img):
	return cv2.flip(img,-1)



def rotater(img):
	try:
		rows,cols,c = img.shape 
	except ValueError:
		rows,cols = img.shape

	M = cv2.getRotationMatrix2D((cols/2,rows/2),90,1)
	dst = cv2.warpAffine(img,M,(cols,rows))
	return dst
def rotatel(img):
	try:
		rows,cols,c = img.shape
	except ValueError:
		rows,cols = img.shape
        M = cv2.getRotationMatrix2D((cols/2,rows/2),270,1)
        dst = cv2.warpAffine(img,M,(cols,rows))
	return dst



def add_noise(img,amplitude=3):
	h,w,d = img.shape
	shape=(h,w,d)
	data32=np.asarray(img,dtype="int32")
        noise=np.zeros((h,w),dtype="int32")
        for i in xrange(h):
            for j in xrange(w):
                noise[i,j] = noise[i,j]+random.randrange(0,amplitude)
        

        for chan in xrange(3):
        
            data32[:,:,chan]+=noise
        np.clip(data32,0,255,out=data32)
        img=e=data32.astype('uint8')


	return img


def toGray(img):

	gray_img = np.zeros(img.shape,dtype=img.dtype)


	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	for index in xrange(3):
		gray_img[::,::,index]=gray

	return gray_img

def invert(img):
	if len(img.shape)==2:
		return 255-img

	if len(img.shape)==3 and (img.shape[2]==3):
		for index in range(3):
			img[::,::,index]=255-img[::,::,index]

		return img
 


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


def hsv_space_aug(img,h_index,s_index,v_val):
	
	hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype("float32")
	hue,s,v=cv2.split(hsv_image)

	hue = pow(hue,h_index)
	s = pow(s,s_index)
	v = v+v_val

	np.clip(hue,0,180,out=hue)
	np.clip(s,0,255,out=s)
	np.clip(v,0,255,out=v)


	hue = hue.astype("uint8")
	s = s.astype("uint8")
	v = v.astype("uint8")
	



	hsv_image = cv2.merge((hue,s,v))

	new_image = cv2.cvtColor(hsv_image,cv2.COLOR_HSV2BGR)

	return new_image



def rotateImage(image, angle):

	image_center = tuple(np.array(image.shape[0:2])/2)

	rot_mat = cv2.getRotationMatrix2D(image_center,angle,scale=1.0)
	result = cv2.warpAffine(image, rot_mat, (image.shape[1],image.shape[0]),flags=cv2.INTER_LINEAR)
	return result

def guassBlur(image):
    
        kernel=(3,3)
	blur_image = cv2.GaussianBlur(image, kernel,0) 

	return blur_image


def getEdge(image):
	sobelX = cv2.Sobel(image,cv2.CV_64F,1,0)
	sobelY = cv2.Sobel(image,cv2.CV_64F,0,1)

	sobelX = np.uint8(np.absolute(sobelX))
	sobelY = np.uint8(np.absolute(sobelY))
	sobelCombined = cv2.addWeighted(sobelX,0.5,sobelY,0.5,gamma=0.8)

	return sobelCombined




if __name__ == '__main__':

	raw = cv2.resize(cv2.imread("/home/henry/WarmHole/model_generator/MorpxData/rawData/goldenHand/betterhand_positive_crop_0.jpg"),(28,28))
	print raw
	#img = hsv_space_aug(cv2.imread("/home/henry/2850.jpg"),random.uniform(0.9,1.1),random.uniform(0.9,1.1),random.randrange(-20,20))
	img = guassBlur(raw)
        print img.shape
	cv2.imshow("test",cv2.resize(img,(300,300)))
	key=cv2.waitKey()
