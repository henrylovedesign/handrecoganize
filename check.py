import cv2
import os
root='/opt/henry/model_generator/MorpxData/classification/hand'
wid=[]
for image in os.listdir(root):
	h,w,d = cv2.imread(os.path.join(root,image)).shape

	if w!=320:
		wid.append(w)
		print h,w,d
		print image
print len(list(set(wid)))
print set(wid)
