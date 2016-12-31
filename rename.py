import cv2
import os
import sys

def rename(imroot,stdname):

	index=0
	imglist = os.listdir(imroot)
	for img in imglist:
            #if os.path.splitext(img)[1]==".jpg":
                name = os.path.basename(imroot)
                os.rename(os.path.join(imroot,img),os.path.join(imroot,name+"_"+stdname+str(index)+".jpg"))
                index+=1

def renameRawFrame(RawFrameRoot,stdname):
    for imroot in os.listdir(RawFrameRoot):
        for file in os.listdir(os.path.join(RawFrameRoot,imroot)):
        
                name = os.path.basename(imroot)
                os.rename(os.path.join(RawFrameRoot,imroot,file), os.path.join(RawFrameRoot,imroot,name+"_"+stdname+file))

           



def main(argv=None):
	if argv==None:
		argv=sys.argv
	imroot = argv[1]
        stdname = argv[2]
        
	rename(imroot,stdname)


if __name__== '__main__':
	main()

	
