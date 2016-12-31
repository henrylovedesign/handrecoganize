import os


root='/opt/henry/model_generator/models/hand_classifytor/snapshot_gray/'
for img in os.listdir(root):
	os.system('chmod 777 '+os.path.join(root,img))
