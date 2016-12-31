import os 
import sys
im_root = "/home/henry/projects/python/pycaffe/py-faster-rcnn/data/VOCdevkit2007/VOC2007/JPEGImages"
train="/home/henry/projects/python/pycaffe/py-faster-rcnn/data/VOCdevkit2007/VOC2007/ImageSets/Main/"
bus=[]
r2d2=[]
print len(os.listdir("/opt/henry/VOCdevkit2007/VOC2007/JPEGImages"))
traintxt="/opt/henry/VOCdevkit2007/VOC2007/ImageSets/Main/bird_test.txt"
print sum([int(line.strip().split(" ")[-1].strip()) for line in open(traintxt) if line.strip().split(" ")[-1]=='1'])
print len([line for line in open(traintxt)])
for image in os.listdir(im_root):

	if image[0]=='0':
		
		bus.append(image.split(".")[0])
	else:
		r2d2.append(image.split(".")[0])

print len(os.listdir(im_root))
print len(bus)
sys.exit()
with open(train+"bus_train.txt","w") as bt:
	for abus in bus:
		bt.write(abus+"  1")
		bt.write("\n")

	for ar2d2 in r2d2:
		bt.write(ar2d2+" -1")
		if ar2d2!=r2d2[-1]:
			bt.write("\n")
	bt.close()

with open(train+"r2d2_train.txt","w") as bt:
	for abus in bus:
		bt.write(abus+" -1")
		bt.write("\n")

	for ar2d2 in r2d2:
		bt.write(ar2d2+"  1")
		if ar2d2!=r2d2[-1]:
			bt.write("\n")
	bt.close()



with open(train+"trainval.txt","w") as bt:
	for abus in bus:
		bt.write(abus)
		bt.write("\n")

	for ar2d2 in r2d2:
		bt.write(ar2d2)
		if ar2d2!=r2d2[-1]:
			bt.write("\n")
	bt.close()


