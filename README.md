# SC2replayDatasetGenerator
Outil de génération de datasets pour entraîner des réseaux de neurones à partir de fichiers de replays du jeu StarCraft 2

Ce programme nécessite d'avoir installé python 3 et sc2reader.

Utilisation :
- Copier les replays à parser dans le répertoire "replays"
- Ouvrir une console à la racine du projet et y entrer :
	python3 datasetGenerator.py
- Le dataset généré se situe dans le répertoire csvOutput au format csv