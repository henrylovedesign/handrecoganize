import sys
import os
sys.path.append('../')
import model_generator.projectroot as prt
proot=prt.project_dir
def recategory(cat_mapping,dataname,new_dataname):
	

	try:
		os.mkdir(os.path.join(proot,"MorpxData",new_dataname))


	except OSError:
                pass    

	try:
		os.mkdir(os.path.join(proot,"MorpxData",new_dataname,"clsGTBox"))

	except OSError:
		pass

	try:
		os.mkdir(os.path.join(proot,"MorpxData",new_dataname,"clsImages"))
	except OSError:

		pass


        for key in cat_mapping.keys():
                
                try:
                        os.mkdir(os.path.join(proot,"MorpxData",new_dataname,"clsGTBox",key))
                except OSError:
                        pass

                image_list=[]
                for cls in cat_mapping[key]:
                        gt_root=os.path.join(cls_gt_root,cls)
                        image_list+= [os.path.splitext(os.path.splitext(filename)[0])[0]+".jpg" for filename in  os.listdir(gt_root)]



                image_list = list(set(image_list))

                for image in image_list:
                        text=[]
                        for cls in cat_mapping[key]:
                                
				if image.replace(".jpg",".txt") in os.listdir(os.path.join(cls_gt_root,cls)):
					text.append(open( os.path.join(cls_gt_root,cls,image.replace(".jpg",".txt")),'r').read())
				
				if image+".txt" in os.listdir(os.path.join(cls_gt_root,cls)):
					text.append(open(os.path.join(cls_gt_root,cls,image+".txt"),'r').read() )


                        with open((os.path.join(proot,"MorpxData",new_dataname,"clsGTBox",key,image.replace(".jpg",".txt"))),'w') as t:
                                t.write("\n".join(text))
                        t.close()

if __name__ == '__main__':
        cls_gt_root = os.path.join(proot,"MorpxData","VOC2007plus",'clsGTBox')
        cat_mapping={
                        "hand":[],
                        "others":[]
                        }

        for cls in os.listdir(cls_gt_root):
                if cls!='hand':
                        cat_mapping["others"].append(cls)

                if cls=='hand':
                        cat_mapping['hand'].append(cls)
        dataname='VOC2007plus'
        new_dataname='hand_others'
        recategory(cat_mapping,dataname,new_dataname)


