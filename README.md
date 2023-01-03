# SC2replayDatasetGenerator
Outil de génération de datasets pour entraîner des réseaux de neurones à partir de fichiers de replays du jeu StarCraft 2

Ce programme nécessite d'avoir installé python 3 et sc2reader.

Utilisation :
- Copier les replays à parser dans le répertoire "replayBank", pour cela le script de déplacement de fichiers de masse peut être utile.
  Il prend en entrée un répertoire nommé "replays" et déplace le nombre désiré (demandé par le programme) vers "replayBank"
	python3 replayMover.py
- Exécuter le parseur :
	python3 datasetGenerator.py
- Le dataset généré se situe dans le répertoire generatedDatasets au format csv