# SC2replayDatasetGenerator
Outil de génération de datasets pour entraîner des réseaux de neurones à partir de fichiers de replays du jeu StarCraft 2

Ce programme nécessite d'avoir installé python 3 et sc2reader.

Utilisation :
- Copier les replays à parser dans le répertoire "replays"
  Le script de déplacement de fichiers prend en entrée le répertoire "replays" et déplace le nombre désiré de replays vers "replayBank".
	python3 replayMover.py
- Exécuter le parseur :
	python3 datasetGenerator.py
- Les datasets générés se situent dans le répertoire generatedDatasets au format csv.