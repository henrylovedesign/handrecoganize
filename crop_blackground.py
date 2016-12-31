import cv2
import os
import augmentation as aug
import skin_color_set
root="/opt/henry/model_generator/MorpxData/classification/hands/rawData/hands/test"
rawroot="/opt/henry/model_generator/MorpxData/classification/hands/rawData/hands/ResultFrame"
boxroot="/opt/henry/model_generator/MorpxData/classification/hands/rawData/hands/RawFrame"

positive_crop_root = "/opt/henry/model_generator/MorpxData/classification/hands/ForTrain/positive/blackground_positive_crop"
negative_crop_root = "/opt/henry/model_generator/MorpxData/classification/hands/ForTrain/negative/blackground_negative_crop"

dirs = [positive_crop_root,negative_crop_root]
foldernames = os.listdir(rawroot)
print set(os.listdir(rawroot)) - set(os.listdir(boxroot))
count=1

skincondition = skin_color_set.skinCondition

def refineREC(rec,skincondition):
    h,w = rec.shape[0:2]
    up=h
    left=w
    down = 0
    right =0
    
    for i in xrange(h):
        for j in xrange(w):
            r=rec[i,j,2]
            g=rec[i,j,1]
            b=rec[i,j,0]
            if skincondition(r,g,b):
                print i,j
                if i <= up:
                    up=i
                if j<= left:
                    left=j
                if i>=down:
                    down=i
                if j>=right:
                    right=j
    xmin = left
    ymin = up
    xmax = right
    ymax = down
    print xmin,ymin,xmax,ymax
    return [xmin,ymin,right-left,down-up]



def savecrop(im,name,croplist,saveroot):
	index=0
	for crop in croplist:
		x=crop[0]
		y=crop[1]
		xmax=crop[2]
		ymax=crop[3]

		cv2.imwrite(os.path.join(saveroot,name+str(index)+".jpg"),im[y:ymax,x:xmax])
		index+=1
cnt=0
for im in os.listdir(root):
	image = cv2.imread(os.path.join(root,im))
	imname = os.path.basename(im).replace("_trans","")[3::]
	#print imname
	for foldername in foldernames:
		if foldername in imname:
			index = imname.replace(foldername,"").replace(".jpg","")
			#print imname.replace(foldername,""),imname,foldername
			boxfile = os.path.join(boxroot,foldername,index+".txt")
			boxcor = [[int(cor) for cor in line.strip().split(" ")] for line in open(boxfile,"r")][0]


			x=boxcor[0]
			y=boxcor[1]
			w=boxcor[2]
			h=boxcor[3]
			xmax=min(x+w,image.shape[1])
			ymax=min(y+h,image.shape[0])
		    
		
                        newcor = refineREC(image[y:ymax,x:xmax],skincondition)

                        cor = [x+newcor[0],y+newcor[1],newcor[2],newcor[3]]
		
			positive_crop,negative_crop=aug.dataAugmentationWithshift( [image.shape[1],image.shape[0]] , cor )
			for d in dirs:
				if not os.path.isdir(d):
					os.mkdir(d)
				if os.path.basename(d).split("_")[1]=="positive":
					croplist=positive_crop
				if os.path.basename(d).split("_")[1]=="negative":
					croplist=negative_crop
					
				name="hand"+str(cnt)+"_"
				savecrop(image,name,croplist,d)
	cnt+=1
	
		




print count
