import os

def build_file_str(template_root,target_root):
	if not os.path.isdir(target_root):
		os.mkdir(target_root)
	for root,dir,files in os.walk(template_root):
		subroot =root.replace(template_root,"")
		for adir in dir:
			if not os.path.isdir("/".join([target_root,subroot,adir])):
			
				os.mkdir("/".join([target_root,subroot,adir]))


if __name__ == '__main__':
	
	template_root="/home/henry/projects/python/pycaffe/py-faster-rcnn/data/VOCdevkit2007"
	target_root="/home/henry/data"

	build_file_str(template_root,target_root)