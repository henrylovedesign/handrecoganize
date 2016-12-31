import random

def dataAugmentationWithshift(imsize,cor):

	imw,imh = imsize


	xmin = cor[0]
	ymin = cor[1]
	xmax = cor[0]+cor[2]
	ymax = cor[1]+cor[3]

	w = cor[2]
	h = cor[3]

	xcenter = xmin + w/2
	ycenter = ymin + h/2





	inter_vectors = [[0,0],[w/2,0],[w/2,h/2],[0,h/2],[w/4,h/4],[w/4,h/2],[w/2,h/4],[w/4,0],[0,h/4],[3*w/4,3*h/4],[3*w/4,0],[0,3*h/4],[w/2,3*h/4],[3*w/4,h/2]]
	outer_vectors =	[
					[w,0],
					[0,h],
					[w,h],
					[-1*w,0],
					[0,-1*h],
					[-1*w,-1*h],
					[-1*w,h],
					[w,-1*h],
					[w/2,0],
					[0,h/2],
					[w/2,h/2],
					[-1*w/2,0],
					[0,-1*h/2],
					[-1*w/2,-1*h/2],
					[-1*w/2,h/2],
					[w/2,-1*h/2]
					]
	
	negative_crop=[]
	positive_crop=[]


	for vector in inter_vectors:
		negative_crop.append([xmin+vector[0],ymin+vector[1],xcenter+vector[0],ycenter+vector[1]])

	for vector in outer_vectors:
		#if ymax+vector[1] <=0 :
			#print vector
			#print ymin
			#print ymax
			#print h
		wcrop = min(xmax+vector[0],imw) - max(xmin+vector[0],0)
		hcrop = min(ymax+vector[1],imh) - max(ymin+vector[1],0)
		if wcrop<=1 or hcrop<=1:
			
			continue

		if (hcrop*2 > wcrop) and ( wcrop *2 > hcrop ) :

			negative_crop.append(  		[max(xmin+vector[0],0),max(ymin+vector[1],0),min(xmax+vector[0],imw),min(ymax+vector[1],imh)]        )


	for i in range(len(inter_vectors)+len(outer_vectors)):
		shift_vectors =[random.randrange(-10,10),random.randrange(-10,10)]
		positive_crop.append([max(xmin+shift_vectors[0],1), max(ymin+shift_vectors[0],1), min(xmax+shift_vectors[1],imw-1),min(ymax+shift_vectors[1],imh-1)  ])


	





	return positive_crop,negative_crop
