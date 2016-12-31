import os
import sys
sys.path.append("../")
import model_generator.projectroot as prt
proot = prt.project_dir
MORPXdevkit_path=os.path.join(proot,"py-faster-rcnn","data","MORPXdevkit")



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


def main(argv=None):
	if argv is None:
		argv=sys.argv

	dataname = argv[1]

	make_dir(dataname)


