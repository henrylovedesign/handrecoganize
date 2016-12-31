

trainlist= "/home/henry/WarmHole/model_generator/MorpxData/TrainingSet/hands/BCam7_lessMu/BCam7_lessMu_train.data"

print sum([int(line.split(" ")[1]) for line in open(trainlist,"r")])
