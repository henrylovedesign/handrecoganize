import os
import sys
import cv2



voc_root = '/opt/henry/model_generator/MorpxData/rawData/VOC2007'
box_root = os.path.join(voc_root,"clsGTBox")
image_root = os.path.join(voc_root,"clsImages")
save_root = '/opt/henry/model_generator/MorpxData/classification/hands/ForTrain/negative/voc2007'


for cls in os.listdir(box_root):
    for boxfile in os.listdir(os.path.join(box_root,cls)):
        path = os.path.join(box_root,cls,boxfile)
        detcor =[ [ int(cor) for cor in line.strip().split(" ")] for line in open(path)]
        name = os.path.splitext(boxfile)[0]
        im_path = os.path.join(image_root,name+".jpg")
        image = cv2.imread(im_path)
        index =0
        for box in detcor:
            xmin = box[0]
            ymin = box[1]
            xmax = box[0]+box[2]
            ymax = box[1]+box[3]
            imname  = cls+str(index)+name+".jpg"
            cv2.imwrite( os.path.join(save_root,imname) ,image[ymin:ymax,xmin:xmax])
            index+=1
