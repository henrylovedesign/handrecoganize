import numpy as np
import cv2

image = cv2.imread("//opt/henry/model_generator/MorpxData/classification/hands/rawData/hands/ResultFrame/2016112595126/200.jpg")
image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
cv2.imshow("Original",image)
cv2.waitKey()

#lap = cv2.Laplacian(image,cv2.CV_64F)
#lap = np.uint8(np.absolute(lap))
#cv2.imshow("Laplacian",lap)
#acv2.waitKey()


sobelX = cv2.Sobel(image,cv2.CV_64F,1,0)
sobelY = cv2.Sobel(image,cv2.CV_64F,0,1)

sobelX = np.uint8(np.absolute(sobelX))
sobelY = np.uint8(np.absolute(sobelY))
sobelCombined = cv2.bitwise_or(sobelX,sobelY)
cv2.imshow("Sobel X", sobelX)
cv2.waitKey()
cv2.imshow("Sobel Y", sobelY)
cv2.waitKey()
cv2.imshow("Sobel Combined", sobelCombined)
cv2.waitKey() 
