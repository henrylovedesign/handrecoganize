import os
import sys
sys.path.append('../')
import cv2
import handclstor_data_prepare as dt
import randomcrop 
import random
import model_generator.projectroot as prt
import transformation as trf
import multiprocessing as mp
from functools import partial
proot = prt.project_dir
import time
import numpy as np
import rename as rn
import gc
import lmdb
import set_caffe_path
import caffe
#cls_data_root = os.path.join(proot,"MorpxData","classification")

#targetname="hands"

#target_cls_data_root = os.path.join(cls_data_root,"hands","ForTrain")


sample_step=1
augmentation_map={"blur":trf.guassBlur,"Hflip":trf.horizon_flip,"Vflip":trf.vertical_flip,"rR":trf.rotater,"lR":trf.rotatel,"saltnoise":trf.add_noise}

def nsample_condition(img):
	if sample_step>0:
		n=random.randrange(0,sample_step)
		if n==0:
			return True
		else:
			return False
	else:
		return True
def psample_condition(img):
	return True

def alpha():
	return random.uniform(0.8,1.5)

def beta():
	return random.randrange(-50,50)


def genh():
	return random.uniform(0.96,1.06)

def gens():
	return random.uniform(0.96,1.06)

def genv():
	return random.randrange(-20,20)

def angle():
	return random.randrange(-20,20)


def name_normalize(sample_map):
    for key in sample_map.keys():
        for imroot in sample_map[key]:
            print imroot
            rn.rename(imroot)


def PNlist(sample_map,training_imroot,pauglist,nauglist):
    srcplist=[]
    srcnlist=[]
    
    
    srclistmap={"positive":srcplist,"negative":srcnlist}
    listnummap={"positive":0,"negative":0}
    augmap={"positive":pauglist,"negative":nauglist}
    
    for key in sample_map.keys():
        imroots = sample_map[key]
        print key
        for imroot in imroots:
            print imroot
            for imname in os.listdir(imroot):
                srcimpath = os.path.join(imroot,imname)
                
                srclistmap[key].append(srcimpath)
                
                
        mult=len(augmap[key])+1
                
        listnummap[key]=mult*len(srclistmap[key])
                
    pnum = listnummap['positive']
    nnum = listnummap['negative']
    return srcplist,srcnlist,pnum,nnum





def gen_TTL(plist,nlist,trainlistFile,testlistFile,positivelistFile,negativelistFile):



    trainlist,testlist = dt.creat_train_test_list(plist,nlist,0.90)

    print "total positive size: "+str(len(plist))
    print "total negative size: "+str(len(nlist))

    print "training size: "+str(len(trainlist))
    print "testing size: " +str(len(testlist))

    dt.writeToFile(trainlist,trainlistFile,'w')
    dt.writeToFile(testlist,testlistFile,'w')
    dt.writeToFile(plist,positivelistFile,'w')
    dt.writeToFile(nlist,negativelistFile,'w')

def get_trainPNlist(training_imroot,sample_map):
    
    listmap={}
    for key in sample_map.keys():
        listmap[key]=[]
    
    for imroot in os.listdir(training_imroot):
        for key in sample_map.keys():
            if imroot.split("_")[0]==key:
                plist+=[os.path.join(training_imroot,imroot,n) for n in os.listdir(os.path.join(training_imroot,imroot))] 
    gen_TTL(plist,nlist,trainlistFile,testlistFile,positivelistFile,negativelistFile)
   

def augmentation(image,auglist):
    h,w,c = image.shape
    transdic={}
    transdic['raw']=image
    for aug in auglist:
        transdic[aug] =augmentation_map[aug](image)

    return transdic


def gentargetmap(imlist):
    imnum = len(imlist)
    map={}
    for i in xrange(imnum):
        map[imlist[i]]=random.randrange(0,10)

    return map


def pSample_prepare(impath,auglist,training_imroot,targetmap):
    
    
    part=targetmap[impath]
    part_root = os.path.join(training_imroot,"positive_part_"+str(part) )
    if not os.path.isdir(part_root):
        print "make dir"
        try:
            os.mkdir(part_root)

        except:
            pass

    image = cv2.resize(cv2.imread(impath),(28,28))
    
    transdic = augmentation(image,auglist)
    
    

    imname = os.path.splitext( os.path.basename(impath) )[0]
    
    #dirname = impath.split("/")
    #print dirname
    #dirname = dirname[-2]

    for transkey in transdic.keys():
        pretrain_img=transdic[transkey]
        imgPath=os.path.join(part_root,imname+transkey+".jpg")
        cv2.imwrite( imgPath,pretrain_img)
        #del pretrain_img
        #del transdic[transkey]
        #gc.collect()           


def nSample_prepare(impath,auglist,training_imroot,targetmap):
    
    part=targetmap[impath]
    part_root = os.path.join(training_imroot,"negative_part_"+str(part) )
    if not os.path.isdir(part_root ):
        try:
            os.mkdir(part_root )
        except:
            pass
  
    try:
        image =cv2.resize(cv2.imread(impath),(28,28))
        
        transdic = augmentation(image,auglist)
        
        
        
        imname = os.path.splitext( os.path.basename(impath) )[0]
        #dirname = impath.split("/")
        #dirname = dirname[-2]

     
        for transkey in transdic.keys():
            pretrain_img=transdic[transkey]
            imgPath=os.path.join(part_root,imname+transkey+".jpg")
            cv2.imwrite( imgPath,pretrain_img)
            #del pretrain_img
            #del transdic[transkey]
            #gc.collect()
    except:
        print impath

def parrelize(f,inputs):
    pool=mp.Pool(processes=24)
    
        
    pool.map(f,inputs)
    
    pool.close()
    pool.join()
    



def main(argv=None):
    if argv==None:
        argv=sys.argv
    
    
    clsname=argv[1]
    trainingSet=argv[2]

    mode = argv[3]

    print "Setting..."   

    #classification data root   
    cls_data_root = os.path.join(proot,"MorpxData","TrainingSet",clsname)
    
    #database root for training
    target_cls_data_root = os.path.join(proot,"MorpxData","rawData")
    
    #training directory for training classification model
    trainingRoot = os.path.join(cls_data_root,trainingSet)
    
    #image root for training
    training_imroot = os.path.join(trainingRoot,"Image")
    
    #train,test,positive,negative sample list
    trainlistFile = os.path.join(trainingRoot,trainingSet+"_train.data")
    testlistFile = os.path.join(trainingRoot,trainingSet+"_test.data")
    positivelistFile = os.path.join(trainingRoot,trainingSet+"_train_positive.data")
    negativelistFile = os.path.join(trainingRoot,trainingSet+"_train_negative.data")
    
    #positive,negative combination setting configure file
    configfile = os.path.join(trainingRoot,"config")

    config = [line.strip() for line in open(configfile,'r')]
    pindex=config.index('positive')
    nindex=config.index('negative')

    sample_map={'positive':[],'negative':[]}
    for sample in config[pindex+1:nindex]:
        sample_path = os.path.join(target_cls_data_root,sample)
        sample_map['positive'].append(sample_path)

    for sample in config[nindex+1::]:
        sample_path = os.path.join(target_cls_data_root,sample)
        sample_map['negative'].append(sample_path)
    
    #augmentation setting
    augfile = os.path.join(trainingRoot,"aug")
    
    aug = [line.strip().split(" ") for line in open(augfile,'r')]
    print aug
    pauglist = aug[0][1].split(",")
    nauglist = aug[1][1].split(",")
    
    


    #name_normalize(sample_map)
    print "preparing positive negative list"
    srcplist,srcnlist,pnum,nnum = PNlist(sample_map,training_imroot,pauglist,nauglist)
    
    print "total positive sample: "+str(pnum)
    print "total negative sample: "+str(nnum)

    ptargetmap=gentargetmap(srcplist)
    ntargetmap=gentargetmap(srcnlist)
    
    rn = raw_input("continue[Y/n]")
    if rn =="n":
        sys.exit()
    if rn =="Y":
        if mode=="f":
            if os.path.isdir(training_imroot):
                os.system("sudo rm -r "+training_imroot)
            os.mkdir(training_imroot)
            #Training Testing list
            print "generate train test list"
            


            wrap_getP =partial(pSample_prepare,auglist = pauglist,training_imroot=training_imroot,targetmap=ptargetmap)
            wrap_getN =partial(nSample_prepare,auglist = nauglist,training_imroot=training_imroot,targetmap=ntargetmap)
            
            print "preparing data"
            
            for key in sample_map.keys():
                    samples = sample_map[key]

                    if key=='positive':
                        print "preparing positive data"
                        parrelize(wrap_getP,srcplist)
                        gc.collect()

                    if key=='negative':
                        print "preparing negative data"
                        parrelize(wrap_getN,srcnlist)           
                        gc.collect()
            
            plist=[]
            nlist=[]
            
            for imroot in os.listdir(training_imroot):
                if imroot.split("_")[0]=="positive":
                    plist+=[os.path.join(training_imroot,imroot,n) for n in os.listdir(os.path.join(training_imroot,imroot))] 
                if imroot.split("_")[0]=="negative":
                    nlist+=[os.path.join(training_imroot,imroot,n) for n in os.listdir(os.path.join(training_imroot,imroot))]
            gen_TTL(plist,nlist,trainlistFile,testlistFile,positivelistFile,negativelistFile)

        if mode=="b":
            
            batch_size = len(srcplist)+len(srcnlist)
            batch = np.empty((batch_size,3,28,28),dtype=np.uint8)
            label = np.empty(batch_size,dtype=np.int64)
            
            for i in xrange(batch_size):
                
                im=cv2.imread(srcplist[i])
                batch[i,0,:,:]=im[:,:,2]
                batch[i,1,:,:]=im[:,:,1]
                batch[i,2,:,:]=im[:,:,0]
                if i<=pnum-1:
                    label[i]=1
                else:
                    label[i]=0

            map_size = batch.nbytes * 10

            env = lmdb.open('mylmdb', map_size=map_size)

            with env.begin(write=True) as txn:
            # txn is a Transaction object
                for i in range(batch_size):
                    datum = caffe.proto.caffe_pb2.Datum()
                    datum.channels = X.shape[1]
                    datum.height = X.shape[2]
                    datum.width = X.shape[3]
                    datum.data = X[i].tobytes()  # or .tostring() if numpy < 1.9
                    datum.label = int(y[i])
                    str_id = '{:08}'.format(i)
                            
                


if __name__=='__main__':
    main()
