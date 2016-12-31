import cv2
import sys
import os
sys.path.append("../")
import model_generator.projectroot as prt
proot = prt.project_dir
import random
import shutil

def readConfig(config):
    sample = [line.strip() for line in open(config,'r')]
    pindex = sample.index('positive')
    nsample = sample[1:pindex]
    psample = sample[pindex+1:]
    testSet=[]
    for s in nsample:
        name = s.split(" ")[0]
        crop_num = int(s.split(" ")[1])
        testSet.append(['negative',name,crop_num])

    for s in psample:
        name = s.split(" ")[0]
        crop_num = int(s.split(" ")[1])
        testSet.append(['positive',name,crop_num])

    return testSet

def readDtConfig(config):
    sample = [line.strip() for line in open(config,'r')]
    return sample




def randomcrop(im):
    h,w,c = im.shape
    while True:
        xmin = random.randrange(0,w-1)
        ymin = random.randrange(0,h-1)

        xmax =xmin+random.randrange(0,w-xmin)
        ymax =ymin+ random.randrange(0,h-ymin)
        #print [xmin,ymin,xmax,ymax]
        if not (xmax==xmin or (ymax==ymin)):
            break
    return im[ymin:ymax,xmin:xmax]

def genTestSet(test_data_root,testSet,testSetRoot):
    nlist=[]
    plist=[]
    save_root = os.path.join(testSetRoot,"Image")
    listmap = {"positive":plist,"negative":nlist}
    rootmap = {"positive":os.path.join(test_data_root,'positive'),"negative":os.path.join(test_data_root,'negative')}
    lablemap={"positive":'1',"negative":'0'}
    for sample in testSet:
            print sample
            im_root = os.path.join(rootmap[sample[0]],sample[1])
            for image in os.listdir(im_root):
            
                name = "_".join([sample[1],image])
                im = cv2.imread(os.path.join(im_root,image))
                cv2.imwrite( os.path.join(save_root,name),cv2.resize(im,(28,28)) )
                listmap[sample[0]].append([os.path.join(save_root,name),lablemap[sample[0]]])
        
                if sample[2]>1:
                    index=0
                    for i in xrange(sample[2]):
                        crop = randomcrop(im)
                        name = os.path.splitext(image)[0]+"_"+str(index)+".jpg"
                        cv2.imwrite(os.path.join(save_root,name),crop)
                        listmap[sample[0]].append([os.path.join(save_root,name),lablemap[sample[0]]])
                        index+=1
    imlist = nlist+plist
    with open(os.path.join(testSetRoot,'testimlist'),"w") as wr:
        wr.write("\n".join([" ".join(indexim) for indexim in imlist ]))
    
    
def dtTestSet(dtTest_data_root,config,testSetRoot):
    samples = readDtConfig(config)
    for sample in samples:

        #for textfile in os.listdir(os.path.join(dtTest_data_root,sample,"GT")):
         #   shutil.copy(os.path.join(dtTest_data_root,sample,"GT",textfile),os.path.join(testSetRoot,"GT") )

        for image in os.listdir(os.path.join(dtTest_data_root,sample)  ):
            shutil.copy(os.path.join(dtTest_data_root,sample,image),os.path.join(testSetRoot,"Image"))



def main(argv=None):
    if argv==None:
        argv=sys.argv

    clsname = argv[1]
    testSetname = argv[2]
    mode = argv[3]
    if mode == "cls":
        test_data_root = os.path.join(proot,"MorpxData","classification",clsname,"ForTest")
        testSetRoot = os.path.join(test_data_root,"TestSet",testSetname)
        config = os.path.join(testSetRoot,"config")

        testSet= readConfig(config)
        genTestSet(test_data_root,testSet,testSetRoot)
    
    if mode == "dt":
        dtTest_data_root = os.path.join(proot,"MorpxData","detection",clsname,"ForTest")
        testSetRoot = os.path.join(dtTest_data_root,"TestSet",testSetname)
        config = os.path.join(dtTest_data_root,"TestSet",testSetname,"config")

        
        dtTestSet(dtTest_data_root,config,testSetRoot)

if __name__ == '__main__':
    main()

    
