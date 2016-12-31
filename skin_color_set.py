import numpy as np
import random
import cv2
def skinCondition(r,g,b):
	if(
			r>80
		and	g>40
		and	b>20

		and	r>g
		and	r>b
		and	max([r,g,b])-min([r,g,b])>5
		and	abs(r-g)>5
				):
		return True

	else:
		return False

def main():
    image = np.zeros((60,60,3),dtype="uint8")
    r=random.randrange(0,255)
    g=random.randrange(0,255)
    b=random.randrange(0,255)

    while not skinCondition(r,g,b):
	
	r=random.randrange(0,255)
	g=random.randrange(0,255)
	b=random.randrange(0,255)
	print r,g,b

    for i in xrange(60):
	for j in xrange(60):
		

		image[i,j] = [b,g,r]

    cv2.imshow('skin',image)
    cv2.waitKey()
