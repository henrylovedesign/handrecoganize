import annotation as an
import os
import sys
sys.path.append("../")
import model_generator.projectroot as prt
proot=prt.project_dir
MORPXdevkit_root = os.path.join(proot,"py-faster-rcnn","data","MORPXdevkit")



def make_dir(dataname):

        try:
                os.mkdir(os.path.join(MORPXdevkit_root,dataname))
        except OSError:
                pass

        for subdir in ['Annotations','ImageSets','JPEGImages']:
                try:
                        os.mkdir(os.path.join(MORPXdevkit_root,dataname,subdir))
                        if subdir == 'ImageSets':
                                try:
                                        os.mkdir(os.path.join(MORPXdevkit_root,dataname,subdir,"Main"))
                                except OSError:
                                        pass
                except OSError:
                        pass



def generate_xmls(cls_im_root,cls_gt_root,annotation_root):
	
	for img in os.listdir(cls_im_root):
		cls_gt_dic={}
		for cls in os.listdir(cls_gt_root):
			filename= os.path.join(cls_gt_root,cls , os.path.splitext(img)[0]+".txt")
			filename2= os.path.join(cls_gt_root,cls , img+".txt")
			#print filename
			if os.path.isfile( filename ):
				gtboxes = [line.strip().split(" ") for line in open(filename,"r")]
				cls_gt_dic[cls]=gtboxes
			if os.path.isfile( filename2 ):
                                gtboxes = [line.strip().split(" ") for line in open(filename2,"r")]
                                cls_gt_dic[cls]=gtboxes
		

		image_path = os.path.join(cls_im_root,img)
		an.generate_xml(image_path,cls_gt_dic,annotation_root)		
			


def main(argv=None):
	if argv is None:
		argv = sys.argv

	dataname = argv[1]
	print dataname
	#make_dir(dataname)
	cls_im_root = os.path.join(proot,"MorpxData",dataname,"clsImages")
	cls_gt_root = os.path.join(proot,"MorpxData",dataname,"clsGTBox")
	annotation_root = os.path.join(MORPXdevkit_root,dataname,"Annotations")
	generate_xmls(cls_im_root,cls_gt_root,annotation_root)

if __name__ == '__main__':
	main()
