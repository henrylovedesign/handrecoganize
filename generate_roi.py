import selectivesearch
import os
import sys
sys.path.append("../")
#import model_generator.projectroot as prt
import model_generator.projectroot as prt
proot = prt.project_dir
import random
import cv2

def randomCrop(im,num):

	candidates=[]	

	h,w = im.shape[0:2]

	while(len(candidates)<num):

		#print len(candidates)
		#print w/4
		xmin = random.randrange( w/20, int(0.9*w) ) 
		ymin = random.randrange( h/20, int(0.9*h) ) 

		cw = random.randrange((w-xmin)/10 ,w-xmin)
		ch = random.randrange((h-ymin)/10 ,h-ymin)


		size = min(cw,ch)

		#crop=im[ymin:ymin+size,xmin:xmin+size]
		cor = [xmin,ymin,xmin+size,ymin+size]
		if size < min(h,w)/5:	
			continue
		#print cor
		candidates.append(cor)

	return candidates

	






def withSelectiveSearch(im):

	img_lbl, regions = selectivesearch.selective_search(im, scale=500, sigma=0.1, min_size=10)

	candidates=[]
	
	size_threshold = im.shape[0]*im.shape[1]/64
		
	for r in regions:
		
		if list(r['rect']) in candidates:
			continue

		if r['size'] < size_threshold:
			continue


		x,y,w,h = r['rect']


		if 4*h<w or 4*w <h:
			continue


		candidates.append(list(r['rect']))

	return candidates
		


def main():

	name=['wood']
	for cat in name:
		imroot = os.path.join(proot,"MorpxData","classification","hands","ForTrain","negative",cat)
		print 'sampling for '+cat 
		for img in os.listdir(imroot):
			#print img
			num = random.randrange(50,100)
			im = cv2.imread(os.path.join(imroot,img))
			
			
			candidates = randomCrop(im,num)
			
			if not os.path.isdir(os.path.join(proot,"MorpxData","classification","hands","ForTrain","negative","crop_"+cat)):
				os.mkdir( os.path.join(proot,"MorpxData","classification","hands","ForTrain","negative","crop_"+cat) )

			index=0
			for cor in candidates:
				#print cor
				crop = im[ cor[1]:cor[3],cor[0]:cor[2] ]
				#print crop
				#print crop.shape
				#print img
				im_path = os.path.join(proot,"MorpxData","classification","hands","ForTrain","negative","crop_"+cat,str(index)+img)
				try:		
					cv2.imwrite(im_path , im)
				except TypeError:
					print img
				index+=1
if __name__ == '__main__':
	main()
