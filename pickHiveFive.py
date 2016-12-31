import os
import shutil
root="/opt/henry/model_generator/raw_data/hands/hand/HandImage"
new_home='/opt/henry/model_generator/MorpxData/classification/hands/hgfive'

for img in os.listdir(root):
	if img.startswith("Hand"):
		shutil.move(os.path.join(root,img),new_home)
