import os
import sys
import tarfile
from PIL import TarIO
from PIL import Image
import numpy as np
import cv2
import random


scoreThreshold=0.6
def extract():
    for tar in os.listdir(PHD_Data_root):
        tarname = os.path.splitext(tar)[0]
        extract_root = os.path.join(subStract_path,tarname)
        if not os.path.isdir(extract_root):
                
            os.mkdir(extract_root)




        tar=tarfile.open(os.path.join(PHD_Data_root,tar))
        
        extract_image = tar.getmembers()[0]
        #tar.extractall(path = extract_root,members=extract_image)
        image  = tar.extractfile(extract_image)
        print type(image.read())


def imreadFromTar(tar_path,im_tarpath):
    fp = TarIO.TarIO(tar_path,im_tarpath)
    return Image.open(fp)



def fpdist(deploy_root,caffemodel_root,caffemodelname,PHD_Data_root,subStract_path,reportFile):
    tarList=os.listdir(PHD_Data_root)   
    import checkmodel as cm
    net_definition =os.path.join(deploy_root,"CamOnly.prototxt")
    weights=os.path.join(caffemodel_root,caffemodelname)
    model = cm.load_model(net_definition,weights)

    
    record=[]
    for tar in tarList:
        
        tar_path = os.path.join(PHD_Data_root,tar)
        tarname = os.path.splitext(tar)[0]
        extract_root = os.path.join(subStract_path,tarname)
        if tarname in os.listdir(subStract_path):
            continue

        extract_image_path = [tarinfor.name for tarinfor in tarfile.open(os.path.join(PHD_Data_root,tar   )).getmembers()[0:2000]  ]
        #print extract_image_path
        
        test_batch=np.empty((2000,30,30,3))
        save_paths=[]
        index=0
        for impath in extract_image_path:
            
            im_tarpath = impath
            
            image = imreadFromTar(tar_path,im_tarpath)
            try:           
                r,g,b = image.split()
                image = Image.merge("RGB",(b,g,r))
            except ValueError:
                continue
            
            imname = os.path.splitext(os.path.basename(impath))[0]
            PILimage = image.resize((30,30))

            save_path = os.path.join(extract_root,imname+".jpg")
	    save_paths.append(save_path)
            test_batch[index] = np.array(PILimage)
            index+=1

               
        score = cm.score(model,test_batch)
          
                       
        count = 0
        for i in xrange(2000):
            if score[i]>=scoreThreshold:
                count+=1
                if not os.path.isdir(extract_root):

                    os.mkdir(extract_root)

             	   
            	save_path=save_paths[i]
                cv2.imwrite(os.path.join(save_path) , test_batch[i] )


        print " ".join([tar,str(count)])
        record.append(" ".join( [tar,  str(count) ] ) )
    with open(reportFile,'w') as rf:
        rf.write("\n".join(record))



def random_nsample_mining(caffemodelname,number,PHD_Data_root,subStract_path,distribution=None):
    nsample_number=0
    nsample_list=[]
    
    for i in xrange(10):
        tarlist = np.random.choice(os.listdir(PHD_Data_root),60,replace=False)
        for tarname in tarlist:
            
            tar_path = os.path.join(PHD_Data_root,tarname)
            imlist = [tarinfor.name for tarinfor in tarfile.open(tar_path).getmembers()]
            print len(imlist)
            nsamples = np.random.choice(imlist,min(500,len(imlist)),replace=False)
        
            for nsample in nsamples:
                im_tarpath = nsample
                image = imreadFromTar(tar_path,im_tarpath)
                try:
                    r,g,b = image.split()
                    image = Image.merge("RGB",(b,g,r))
                except ValueError:
                    continue
                image = np.array(image.resize((30,30)))

                imname = os.path.splitext(os.path.basename(im_tarpath))[0]
                impath = os.path.join(subStract_path,imname+".jpg")

                cv2.imwrite(impath,image)


def main(argv=None):

    PHD_Data_root="/media/henry/My Passport/ImageNet/ImageNet/Train"

    deploy_root="/opt/henry/model_generator/models/hand_classifytor/deploy"
    caffemodel_root="/opt/henry/model_generator/models/hand_classifytor/caffemodels"


    if argv==None:
        argv = sys.argv
    caffemodelname = argv[1]
    
    subStract_path = "/opt/henry/model_generator/MorpxData/rawData/"+caffemodelname+"_ImageNet"
    if not os.path.isdir(subStract_path):
        os.mkdir(subStract_path)
    number = 200000
    reportFile = os.path.join("/opt/henry/model_generator/MorpxData/rawData/" ,caffemodelname+"_ImageNet_minor_report")

    fpdist(deploy_root,caffemodel_root,caffemodelname,PHD_Data_root,subStract_path,reportFile)
    #random_nsample_mining(caffemodelname,number,PHD_Data_root,subStract_path)
    


if __name__ == '__main__':
    main()
