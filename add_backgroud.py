import random
import numpy as np
import os
import cv2
def add_background(mask,background):
    mask_h,mask_w = mask.shape[0:2]

    xmin = random.randrange(0,background.shape[1]-mask_w)
    ymin = random.randrange(0,background.shape[0]-mask_h)


    for i in xrange(mask_h):
        for j in xrange(mask_w):
            if mask[i,j,0]<20 and (mask[i,j,1]<40) and (mask[i,j,2]<80):
                mask[i,j]=background[ymin+i-1,xmin+j-1]

    return mask



def main():
    background_root = "/opt/henry/model_generator/MorpxData/classification/hands/ForTest/negative/background"
    background_list = os.listdir(background_root)
    background_num = len(background_list)
    mask_root = "/opt/henry/model_generator/MorpxData/classification/hands/ForTrain/positive/blackground_positive_crop"
    with_background_root = "/opt/henry/model_generator/MorpxData/classification/hands/ForTrain/positive/HWB_positive_crop"
    

    for imname in os.listdir(mask_root):
        mask = cv2.imread(os.path.join(mask_root,imname))
        
        while True:
            index = random.randrange(0,background_num)
            background = cv2.imread(os.path.join(background_root,background_list[index]))
            if background.shape[0]>mask.shape[0] and (background.shape[1]>mask.shape[1]):
                break
        print mask.shape,background.shape
        new_image = add_background(mask,background)

        cv2.imwrite(os.path.join(with_background_root,imname),new_image)

if __name__ == '__main__':
    main()
