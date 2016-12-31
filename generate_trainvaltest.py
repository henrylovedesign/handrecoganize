import os
import sys
sys.path.append("../")
import model_generator.projectroot as pr
MORPXdevkit_path = pr.project_dir+"/py-faster-rcnn/data/MORPXdevkit/"


def triplet_split(file_root,ratios):
	filelist = [os.path.splitext(os.path.splitext(file)[0])[0] for file in os.listdir(file_root)]
	num1 = int(len(filelist)*ratios[0])
	parta = filelist[0:num1]
	b = filelist[num1::]
	num2 = int(len(b)*ratios[1])
	partb = b[:num2]
	partc = b[num2:]

	return parta,partb,partc


def make_dir(dataname):

	try:
		os.mkdir(os.path.join(MORPXdevkit_path,dataname))
	except OSError:
		pass

	for subdir in ['Annotations','ImageSets','JPEGImages']:
		try:
			os.mkdir(os.path.join(MORPXdevkit_path,dataname,subdir))
			if subdir == 'ImageSets':
				try:
					os.mkdir(os.path.join(MORPXdevkit_path,dataname,subdir,"Main"))
				except OSError:
					pass
		except OSError:
			pass

	



def generate_trainvaltest(dataname):
	
	make_dir(dataname)
	cls_gt_root=os.path.join(pr.project_dir,"MorpxData",dataname,"clsGTBox")	

	train = []
	val =[]
	test = []
	for cls in os.listdir(cls_gt_root):
		ctrain,cval,ctest = triplet_split(os.path.join(cls_gt_root,cls),[0.5,0.5])
		train+=ctrain
		val+=cval
		test+=ctest

	train = list(set(train))
	val = list(set(val)-set(train))
	test = list(set(test)-set(val)-set(train))
	
	def sign(imagename,cls):
		if (imagename+".txt") in os.listdir(os.path.join(cls_gt_root,cls)):
			return " 1"
		else:
			return "-1"

	for cls in os.listdir(cls_gt_root):
		traintext = "\n".join([ imagename + " " + sign(imagename,cls) for imagename in train])
		valtext = "\n".join([ imagename + " " + sign(imagename,cls) for imagename in val])
		testtext = "\n".join([ imagename + " " + sign(imagename,cls) for imagename in test])
		
		with open(os.path.join(MORPXdevkit_path,dataname,"ImageSets","Main",cls+"_"+"train.txt"),"w") as t:
			t.write(traintext)
		t.close()
		with open(os.path.join(MORPXdevkit_path,dataname,"ImageSets","Main",cls+"_"+"val.txt"),"w") as t:
			t.write(valtext)
		t.close()

		with open(os.path.join(MORPXdevkit_path,dataname,"ImageSets","Main",cls+"_"+"test.txt"),"w") as t:
			t.write(testtext)
		t.close()

		
		with open(os.path.join(MORPXdevkit_path,dataname,"ImageSets","Main",cls+"_"+"trainval.txt"),"w") as t:
			t.write(traintext+"\n"+valtext)
		t.close()		

		with open(os.path.join(MORPXdevkit_path,dataname,"ImageSets","Main","train.txt"),"w") as t:
			t.write("\n".join(train))
		t.close()

		with open(os.path.join(MORPXdevkit_path,dataname,"ImageSets","Main","test.txt"),"w") as t:
			t.write("\n".join(test))
		t.close()

		with open(os.path.join(MORPXdevkit_path,dataname,"ImageSets","Main","trainval.txt"),"w") as t:
			t.write("\n".join(train+val))

		t.close()

def main(argv=None):
	if argv is None:
		argv = sys.argv

	dataname = argv[1]
	generate_trainvaltest(dataname)


if __name__ == '__main__':
	main()
