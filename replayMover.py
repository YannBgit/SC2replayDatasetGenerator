import os, random, shutil

source = "replays"
dest = "replayBank"
nb = int(input("Nombre de fichiers à donner au parseur : "))

print("Déplacement des replays...")

for i in range(nb):
    rdmFile = random.choice(os.listdir(source))
    srcFile = "%s/%s"%(source, rdmFile)
    shutil.move(srcFile, dest)