import cv2

testimg='/opt/henry/model_generator/raw_data/hands/hand/HandImage/Hand00003181.jpg'

img = cv2.imread(testimg)

cv2.imshow('test',img)
cv2.waitKey()
