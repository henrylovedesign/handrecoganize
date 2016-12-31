root = '/opt/henry/model_generator/MorpxData/classification/hands' 
import os
import shutil
for cls in os.listdir(root):
	index=0
	if cls!='train' and (cls!='test') and (cls!='backup'):
		if cls == 'sayHiPost':
			for img in os.listdir(  os.path.join(root,cls)   ):
				shutil.move(os.path.join(root,cls,img),os.path.join(root,cls,'positive'+"_"+cls+str(index)+".jpg"))
				index+=1

		else:
			for img in os.listdir(  os.path.join(root,cls)   ):
                                shutil.move(os.path.join(root,cls,img),os.path.join(root,cls,'negative'+"_"+cls+str(index)+".jpg"))
                                index+=1
				
