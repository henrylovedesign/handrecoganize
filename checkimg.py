import imghdr
root = '/opt/henry/model_generator/MorpxData/classification/hands' 
import os
for cls in os.listdir(root):
	if cls!='test' and (cls!='backup') and (cls!='train') and (cls!='sys'):
		for img in os.listdir(os.path.join( root,cls   )):
			impath = os.path.join(root,cls,img)
			
			if imghdr.what(impath)==None:
				print impath
		
	
			

	
