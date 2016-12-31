from lxml import etree
import cv2
import os
import sys

def generate_xml(image_path,cls_gt_dic,annotation_root):
	
	
		
	filename = os.path.basename(image_path)
	dataname=image_path.split("/")[-3]
	
	#print image_path
	h,w,d=cv2.imread(image_path).shape

	root=etree.Element("annotation")
	#print root.tag
	
	etree.SubElement(root,"folder").text=dataname
	
	
	etree.SubElement(root,"filename").text=filename
	
	etree.SubElement(root,"source").text=""
	
	etree.SubElement(root,"owner").text=""
	
	
	size=etree.SubElement(root,"size")
	etree.SubElement(size,"width").text=str(w)
	etree.SubElement(size,"height").text=str(h)
	etree.SubElement(size,"depth").text=str(d)
	
	
	etree.SubElement(root,"segmented").text='0'

	for key in cls_gt_dic.keys():
		for gtbox in cls_gt_dic[key]:
			
			name=key

			object=etree.SubElement(root,"object")
			
			etree.SubElement(object,"name").text=name
			etree.SubElement(object,"pose").text="Unspecified"
			etree.SubElement(object,"truncated").text="1"
			etree.SubElement(object,"difficult").text="0"

			bndbox=etree.SubElement(object,"bndbox")
			

			etree.SubElement(bndbox,"xmin").text=str(int(gtbox[0])+1)
			etree.SubElement(bndbox,"ymin").text=str(int(gtbox[1])+1)
			xmax=int(gtbox[0])+int(gtbox[2])-1
			ymax=int(gtbox[1])+int(gtbox[3])-1
			if xmax<=w:

				etree.SubElement(bndbox,"xmax").text=str(xmax)
			else:
				etree.SubElement(bndbox,"xmax").text=str(w)

			if ymax<=h:
				etree.SubElement(bndbox,"ymax").text=str(ymax)

			else:
				etree.SubElement(bndbox,"ymax").text=str(h)


	with open(annotation_root+"/"+os.path.splitext(filename)[0]+".xml","w") as xmlf:
		xmlf.write(etree.tostring(root))
	



def main():
	image_root,gt_root,annotation_root=sys.argv[1:]
	generate_xml(image_root,gt_root,annotation_root)



if __name__ == '__main__':
	main()

#image_root,gt_root,annotation_root=["/home/henry/projects/toBeLable/R2D2/R2D2Image"
#						,
#						"/home/henry/projects/toBeLable/R2D2/R2D2GT",
#						"/home/henry/projects/python/pycaffe/model_generator/data/VOC2007/Annotations"]


#generate_xml(image_root,gt_root,annotation_root)
