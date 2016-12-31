import cv2
import transformation as trf
import os
root = "/opt/henry/model_generator/MorpxData/rawData/goldenHand"
for im in os.listdir(root):
    img= cv2.imread(os.path.join(root,im))
    img = trf.guassBlur(img)
    cv2.imwrite("/opt/henry/model_generator/MorpxData/rawData/blurGoldenHand/"+im,img)


