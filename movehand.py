root = '/opt/henry/model_generator/MorpxData/hand_others/clsImages'

import os
import shutil


for img in os.listdir(root):

	if not img.startswith('00'):
		shutil.copy( os.path.join(root,img),'/opt/henry/model_generator/MorpxData/hand_detect/clsImages'   )
