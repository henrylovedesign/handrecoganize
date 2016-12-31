import os
root="/home/henry/WarmHole/model_generator/MorpxData/classification/hands/ForTrain/TrainingSet/BCam4/Image"

def get_abspath(namelist):
    nameslb=[line.strip().split(" ") for line in open(namelist,"r")]

    for namelb in nameslb:
        name = namelb[0]
        for imroot in os.listdir(root):
            if name in os.listdir(os.path.join(root,imroot)):
                #namelb[0]=os.path.join(root,imroot,name)
                print imroot

    with open(namelist,"w") as f:
       f.write("\n".join( [" ".join(x) for x in nameslb] ))
    f.close()


namelist = "/home/henry/WarmHole/model_generator/MorpxData/classification/hands/ForTrain/TrainingSet/BCam4/BCam4_train.data"
get_abspath(namelist)
