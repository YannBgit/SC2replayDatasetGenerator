import os, random, shutil

source = "replays/replayBank"
destTrain = "replays/trainSet"
destTest = "replays/testSet"
nbTrain = int(input("Nombre de fichiers pour le train set : "))
nbTest = int(input("Nombre de fichiers pour le test set : "))

print("Déplacement des replays du train set...")

for i in range(nbTrain):
    rdmFile = random.choice(os.listdir(source))
    srcFile = "%s/%s"%(source, rdmFile)
    shutil.move(srcFile, destTrain)

print("Déplacement des replays du test set...")

for i in range(nbTest):
    rdmFile = random.choice(os.listdir(source))
    srcFile = "%s/%s"%(source, rdmFile)
    shutil.move(srcFile, destTest)
