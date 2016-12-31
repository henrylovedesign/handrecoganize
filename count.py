import os

import sys
sys.path.append('../')
import model_generator.projectroot as prt
proot = prt.project_dir


rawData_root = os.path.join(proot,"MorpxData","rawData")

def webCamNum(dataName):
    cnt=0
    root = os.path.join(rawData_root,dataName,"ResultFrame")
    for dir in os.listdir(root):
        cnt+=len(os.listdir(os.path.join(root,dir)))

    return cnt

def countTrainingSet(training_imroot):
    cnt=0
    for part in os.listdir(training_imroot):
        cnt+=len(os.listdir(os.path.join(training_imroot,part)))

    return cnt


def main(argv=None):
    if argv==None:
        argv=sys.argv

    training_imroot = argv[1]

    print countTrainingSet(training_imroot)


if __name__ == "__main__":
    main()
