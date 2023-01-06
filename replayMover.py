import os
import random
import shutil

src = "replays"
dst = "replayBank"
nbFiles = int(input("Nombre de fichiers à donner au parseur : "))

print("Début du déplacement des replays, n'éteignez pas votre PC...")

files = [f for f in os.listdir(src) if f.endswith(".SC2Replay")]
random.shuffle(files)

for file in files[:nbFiles]:
  srcPath = os.path.join(src, file)
  destPath = os.path.join(dst, file)
  shutil.move(srcPath, destPath)