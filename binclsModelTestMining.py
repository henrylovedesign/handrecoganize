import cv2
import set_caffe_path
import caffe
import checkmodel as cm
import randomcrop
import os
import sys
import numpy as np
sys.path.append('../')
import model_generator.projectroot as prt
proot = prt.project_dir
import multiprocessing as mp
maxbatchsize=2000
import random
from functools import partial

class database(object):

    def __init__(self,imlist):
        self._cur_index=0
        self._imlist = imlist

    def next_batch(self,batchsize):
        cur_index = self._cur_index
        self._cur_index+=batchsize
        
        return self._imlist[cur_index:cur_index+batchsize]


    def batch_num(self):
        return len(self._imlist)/batchsize+1


#test by different cagtegory
def testModel(dataname,modelname,deploy,weights,config='config',mode='classification',cropmethod='random'):

	data_root = os.path.join(proot,"MorpxData",mode,dataname)
	test_root = os.path.join(data_root,'ForTest')

	sample = [line.strip() for line in open(os.path.join(test_root,config),'r')]
	pindex = sample.index('positive')
	nsample = sample[1:pindex]
	psample = sample[pindex+1:]
	testSet={'negative':{},'positive':{}}
	for s in nsample:
		name = s.split(" ")[0]
		crop_num = int(s.split(" ")[1])
		testSet['negative'][name]=crop_num

	for s in psample:
		name = s.split(" ")[0]
		crop_num = int(s.split(" ")[1])
		testSet['positive'][name]=crop_num



	net_definition = os.path.join(proot,'models', modelname,"deploy",deploy)
	weights = os.path.join(proot,'models',modelname,'caffemodels',weights)


	net = cm.load_model(net_definition,weights)



	win_num=0

	total_im=0
	for key in testSet.keys():
		
		another_key =list(set(testSet.keys())-set([key]))[0]

		if key=='negative':
			tag=1
		if key=='positive':
			tag=0

		toi=[]
		cnt=0
		cntpc_map={}

		for samplename in testSet[key].keys():
				
			print 'calulating false '+another_key+ ' for '+samplename
			pccnt=0
			#pcfpn=0
			crop_num = testSet[key][samplename]
			im_root = os.path.join(data_root,'ForTest',key,samplename)

                        #im_base = database(os.listdir(im_root))


			im_num=len(os.listdir(im_root))
			total_im+=im_num
                        imlist = [os.path.join(im_root,im) for im in os.listdir(im_root)]
                        samplebase = database(imlist )

                        test_batch = np.empty((maxbatchsize,30,30,3))
                        
                        if crop_num==1:
                            for j in xrange(im_num/maxbatchsize+1):
                                batch=samplebase.next_batch(maxbatchsize)
                                print "batchsize: "+str(len(batch))
                                
                                for i in xrange(len(batch)):
                                    test_batch[i]=cv2.resize(cv2.imread(batch[i]),(30,30))
                                                       
                                index = cm.predict_image(net,test_batch)[0:len(batch)]
                                #print len(index),len(test_batch)
                                toi+=[[ os.path.join(im_root,os.path.basename(batch[i]) ) ] for i in range(len(index)) if index[i]==tag   ]
                                cnt+=index.count(tag)
                                pccnt+=index.count(tag)
                                #print len(index),index.count(tag)
                        if crop_num!=1:


			    #win_num+=crop_num*len(os.listdir(im_root))
			    for img in os.listdir(im_root):
                                print img
                                cropcors=[]
	            		im = cv2.imread(os.path.join(im_root,img   ))
                                
                                step = (crop_num+1)/maxbatchsize+1
                                
                                test_batch =  np.empty((crop_num+1,30, 30, 3))


	            		


                                for i in xrange(crop_num):
                                        if cropmethod == 'random':

                                                crop,cor = randomcrop.randomcropones(im)
                                                test_batch[i]=cv2.resize(crop,(30,30) )  
                                                cropcors.append(cor)    		

                                        if cropmethod == 'ssearch':
                                                crop,cor = randomcrop.selective_search(im)

                                        
                                test_batch[-1]=cv2.resize(im,(30,30))
                                
                                for s in xrange(step):
                                    index = cm.predict_image(net,test_batch[s*maxbatchsize:min((s+1)*maxbatchsize,crop_num)])
                                    print len(index)
                                    toi+=[[ os.path.join(im_root,img),cropcors[i][0],cropcors[i][1],cropcors[i][2],cropcors[i][3] ] for i in range( len(index) ) if index[i]==tag   ] 
                                    

                                    cnt+=index.count(tag)
                                    pccnt+=index.count(tag)

				    #print cnt,pccnt,float(pccnt)/len(index)



			rate = float(pccnt)/(im_num)
			print 'false '+another_key +' rate: '+str(rate)
			cntpc_map[samplename] = float(pccnt)/(im_num)


		indoi_rate = float(cnt)/total_im
		
	
				
		filename=os.path.join(data_root,'false'+another_key+".txt")

		print "writo to file"
		with open(filename,'w') as f:
	        	f.write(   "\n".join( [" ".join( [str(cor) for cor in infor]    ) for infor in toi  ] ))

		print 'average false '+another_key+' rate per class per image'
		for key in cntpc_map.keys():

	        	print ":".join([key,str(cntpc_map[key])])  



		print 'average false '+another_key+' rate'
		print indoi_rate

#combine testing
def testModel2(testimlist,net,weights):
    fp=0
    tp=0
    imlist =[line.strip().split(" ") for line in  open(testimlist,"r")]
    batch=4000
    test_batch = np.empty((batch,30,30,3))
    cur_index=0
    step=len(imlist)/batch+1

    model = cm.load_model(net,weights)
    scorelist=[]
    for s in xrange(step):
        truelables=[]
        sublist = imlist[cur_index:cur_index+batch]
        print sublist
        for i in xrange(len(sublist)):
            indeximpath = sublist[i]
            impath = indeximpath[0]
            
            #truelable = indeximpath[1]
            #truelables.append(truelable)
            
            im = cv2.imread(impath)
            test_batch[i]=cv2.resize(im,(30,30))
        
        predict = np.array([p for p in cm.predict_image(model,test_batch)])
        
        print predict
        score = cm.score(model,test_batch)[0:len(sublist)+1]
        scorelist+=zip([item[0] for item in sublist],score)
        
        print scorelist
        #truelables = np.array(truelables)
        #for i in xrange(len(predict)):
            
         #   if (int(predict[i])-int(truelables[i]))==1:
          #      fp += 1
         #   if int(predict[i])*int(truelables[i])==1:
          #     tp += 1

        cur_index = cur_index+batch

        print "cur batch: "+str(cur_index)
    with open(os.path.join( "/".join(testimlist.split("/")[:-1]),'result'   ),"w") as wr:
        wr.write("\n".join( [" ".join( [ scresult[0],str(scresult[1]) ]  ) for scresult in scorelist  ]  )   )

    try:
        totalP = sum([int(indexim[1]) for indexim in imlist])
        totalN = len([indexim[1] for indexim in imlist if indexim[1]=='0'])
        print float(fp)/totalN,float(tp)/totalP
    except IndexError:
        pass


#window testing

def genRanWin(num):
    win=[]
    while True:
        xmin = random.uniform(0.1,1)
        ymin = random.uniform(0.1,1)
        #xmax = random.uniform(0.1,1)
        #ymax = random.uniform(0.1,1)
        w = random.uniform(0.1,1)
    
        win.append([xmin,ymin,w])
        if len(win)>=num:
            break
    return win

def dtTest(impath,wins,model,dtRoot):
    im = cv2.imread(impath)
    try:
        h,w,c = im.shape
    except AttributeError:
        print impath
        
        return 0
    batch = len(wins)+1
    imname= os.path.basename(impath)
    imname= os.path.splitext(imname)[0]

    winbatch=np.empty((batch,30,30,3))   
    crops=[]
    
    for i in xrange(len(wins)):
        win=wins[i]
        xmin = int(w*win[0])
        ymin = int(h*win[1])
        maxsize = min(w-xmin,h-ymin)
        size = int(maxsize*win[2])
        
        xmax = xmin+size
        ymax = ymin+size
        
        if xmax-xmin<9:
            xmax=xmin+min(9,(w-xmin))
        if ymax-ymin<9:
            ymax=ymin+min(9,(h-ymin))

        winbatch[i]=cv2.resize( im[ymin:ymax,xmin:xmax],(30,30) )
        crops.append(" ".join([str(xmin),str(ymin),str(xmax-xmin),str(ymax-ymin) ]))
    winbatch[3999]=cv2.resize(im,(30,30))
    crops.append(" ".join(['0','0',str(w),str(h)]))
    score = [s for s in cm.score(model,winbatch)]
    selnum=20

    
    scoreCrop=sorted(zip(score,crops),reverse=True)[0:selnum]

    subscoreCrop=[]
        
    save_root = os.path.join("/".join(dtRoot.split("/")[:-1]),"Image")
    if not os.path.isdir(save_root ):
        os.mkdir( save_root  )
    index=0
    for scorecrop in scoreCrop:
        score = scorecrop[0]
        if scorecrop[0]>0:
            crop=scorecrop[1].split(" ")
            xmin = int(crop[0])
            ymin = int(crop[1])
            xmax = int(crop[2])+xmin
            ymax = int(crop[3])+ymin
            cropim = im[ymin:ymax,xmin:xmax]
            h,w,c = cropim.shape
            if h==w and h>=5:
                cv2.imwrite( os.path.join(save_root,imname+"crop_"+str(score)+"_"+str(index)+".jpg"),im[ymin:ymax,xmin:xmax])
                index+=1
                subscoreCrop.append([score," ".join([str(xmin),str(ymin),str(w),str(h)]) ])
                break

    with open(os.path.join(dtRoot,imname+".txt"),"w") as dt:
        dt.write("\n".join([" ".join([str(sc[0]),sc[1]]) for sc in subscoreCrop] ))
    

def testWithWindow(testSetRoot,net,weights):
    weightsname = os.path.splitext(os.path.basename(weights))[0]
    model = cm.load_model(net,weights)
    wins = genRanWin(3999)
    dtRoot = os.path.join("/home/henry/WarmHole/model_generator/models/hand_classifytor/caffemodels/dtresult/",weightsname,"dtBox")
    imRoot = os.path.join(testSetRoot,"Image")

    #wrap_dtTest = partial(dtTest,wins=wins,model=model,dtRoot=dtRoot)

    impaths = [os.path.join(imRoot,image) for image in os.listdir(imRoot)]
    for impath in impaths:
        dtTest(impath,wins,model,dtRoot)
    #pool = mp.Pool(24)
    #pool.map(wrap_dtTest,impaths)




def main(argv=None):
	if argv==None:
		argv=sys.argv
        mode = argv[4]
        
        if mode == "cat":
            dataname = argv[1]
            modelname = argv[2]
            weights = argv[3]

            deploy = "CamOnly.prototxt"
            testModel(dataname,modelname,weights,deploy)

        if mode == "cb":
            imlist,deploy,weights = argv[1:4]
	    testModel2(imlist,deploy,weights)
        if mode == "dt":
            testSetRoot,net,weights = argv[1:4]
            
            testWithWindow(testSetRoot,net,weights)

if __name__ == '__main__':
	main()
