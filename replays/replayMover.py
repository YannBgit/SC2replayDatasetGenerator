import os, random, shutil

source = "replays"
destTrain = "trainSet"
destTest = "testSet"
nbTrain = int(input("Nombre de fichiers pour le train set : "))
nbTest = int(input("Nombre de fichiers pour le test set : "))

for i in range(nbTrain):
    rdmFile = random.choice(os.listdir(source))
    srcFile = "%s/%s"%(source, rdmFile)
    shutil.move(srcFile, destTrain)

for i in range(nbTest):
    rdmFile = random.choice(os.listdir(source))
    srcFile = "%s/%s"%(source, rdmFile)
    shutil.move(srcFile, destTest)