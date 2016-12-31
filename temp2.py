import os
import shutil
root="/home/henry/projects/python/pycaffe/py-faster-rcnn/data/VOCdevkit2007/VOC2007/Annotations"
for xml in os.listdir(root):
	
	try:
		shutil.copy(root+"/"+xml,root+"/"+xml.replace(".jpg",""))
		os.remove(root+"/"+xml)
	except shutil.Error:
		pass