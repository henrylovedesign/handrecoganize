import os
import xml.etree.ElementTree as ET
import sys
sys.path.append("../")
import model_generator.projectroot as prt

proot=prt.project_dir
MORPXdevkit_root = os.path.join(proot,"py-faster-rcnn","data","MORPXdevkit")

def get_imname_gtbox(xml):
	gtboxes={}
	tree = ET.parse(xml)
	root = tree.getroot()
	imname = root.find('filename').text

	for obj in root.findall('object'):
		cls = obj.find('name').text
		
		for bnd in obj.findall("bndbox"):
		
			xmin=bnd.find('xmin').text
			ymin=bnd.find('ymin').text
			xmax=bnd.find('xmax').text
			ymax=bnd.find('ymax').text
			
			w=str(int(xmax)-int(xmin))
			h=str(int(ymax)-int(ymin) )

			try:
				gtboxes[cls].append([xmin,ymin,w,h])
			except KeyError:
				gtboxes[cls]=[]
				gtboxes[cls].append([xmin,ymin,w,h])
	return imname,gtboxes


def mk_dir(dataname):
	try:
		os.mkdir(os.path.join(proot,"MorpxData",dataname))
	except OSError:
		pass

	try:
                os.mkdir(os.path.join(proot,"MorpxData",dataname,"clsImages"))
        except OSError:
                pass

	try:
                os.mkdir(os.path.join(proot,"MorpxData",dataname,"clsGTBox"))
        except OSError:
                pass



def reconstruct(dataname):
	
	mk_dir(dataname)
	xml_root =os.path.join( MORPXdevkit_root,dataname, "Annotations")
	cls_gt_root = os.path.join(proot,"MorpxData",dataname,"clsGTBox")
	
	for xml in os.listdir(xml_root):
		
		xml = os.path.join(xml_root,xml)
		imagename,gtboxes = get_imname_gtbox(xml)
		imagename = os.path.splitext(imagename)[0]
		
		for key in gtboxes.keys():
			if not os.path.isdir(os.path.join(cls_gt_root,key)):
				os.mkdir(os.path.join(cls_gt_root,key))
				
			filename = os.path.join(cls_gt_root,key,imagename+".txt")
			with open(filename,"w") as gf:

				gf.write("\n".join([" ".join(cor) for cor in gtboxes[key]]))

def main(argv=None):
	if argv is None:
		argv=sys.argv

	dataname = argv[1]
	reconstruct(dataname)

if __name__ == '__main__':
	main()
