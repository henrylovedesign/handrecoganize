from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import argparse
#import utils
import cv2



def kmeans_quantize(image,n_clusters):


	h,w = image.shape[0:2]
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


	image_reshape = image.reshape((image.shape[0] * image.shape[1], 3))


	clt = KMeans(n_clusters = n_clusters)
	clt.fit(image_reshape)

	cluster_centers_=clt.cluster_centers_.astype("uint8")
	for i in xrange(w):
		for j in xrange(h):
			
			
			cluster_belong = clt.predict([image[j,i,0],image[j,i,1],image[j,i,2]])
			image[j,i,0] = cluster_centers_[cluster_belong][0][0]
			image[j,i,1] = cluster_centers_[cluster_belong][0][1]
			image[j,i,2] = cluster_centers_[cluster_belong][0][1]


	image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

	return image





if __name__ == '__main__':
	image_path="/opt/henry/model_generator/MorpxData/classification/hands/rawData/hands/ResultFrame/201611251088/180.jpg"
	n_clusters=64
	image = cv2.imread(image_path)
	image = kmeans_quantize(image,n_clusters)
	cv2.imshow('test',image)
	key = cv2.waitKey()

