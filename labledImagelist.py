import os

def get_image_list(image_root,gt_root,file):
	
	with open(file,"w") as imagelist:
		imlist = os.listdir(image_root)

		for imgname in imlist:

			try:
				label=open(gt_root+"/"+imgname+".txt").read().strip().split(" ")[0]
				label= str(int(2*(int(label)-0.5)))
				imagelist.write(imgname+" "+label)
				if(imgname!=imlist[-1]):
					imagelist.write("\n")

			except IOError:
				pass

image_root,gt_root,file=["/home/henry/projects/toBeLable/R2D2/R2D2Image",
						
						"/home/henry/projects/toBeLable/R2D2/R2D2GT",
						"/home/henry/projects/toBeLable/R2D2/image_label.list"]

get_image_list(image_root,gt_root,file)