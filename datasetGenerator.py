import csv
import random
import sc2reader
from sc2reader.events import PlayerStatsEvent, PlayerLeaveEvent
import os
from os import path, listdir


header = ["time", "race1", "race2", "map", "supplyUsed1", "supplyUsed2", "totalIncome1", "totalIncome2", "mineralsIncome1", "mineralsIncome2", "vespeneIncome1", "vespeneIncome2", "totalResources1", "totalResources2", "minerals1", "minerals2", "vespene1", "vespene2", "activeWorkers1", "activeWorkers2", "army1", "army2", "technology1", "technology2", "lostResources1", "lostResources2", "winner"]

def raceToId(raceName):
    if raceName == "Terran":
        return 0
    
    elif raceName == "Zerg":
        return 1
    
    elif raceName == "Protoss":
        return 2

    else:
        return -1

mapNames = []

def mapToId(mapName):
    if mapName in mapNames:
        return mapNames.index(mapName)
    
    else:
        mapNames.append(mapName)
        return mapNames.index(mapName)

def frameToRealtime(frame):
    return round(frame / 22.4)

def generateDataset(indir, outfile):
    with open(outfile, "w", newline = "") as csvFile:
        print("Démarrage de l'extraction, n'éteignez pas votre PC...")

        writer = csv.writer(csvFile)
        writer.writerow(header)

        for filename in [f for f in listdir(indir) if f.endswith(".SC2Replay")]:
            try:
                replay = sc2reader.load_replay(path.join(indir, filename))
            
            except Exception:
                print("Erreur de chargement du replay : replay ignoré")
                continue

            if (len(replay.players) == 2) and (replay.frames > 1344) and (replay.expansion == "LotV"):
                frame = 0

                race1 = raceToId(replay.players[0].play_race)
                race2 = raceToId(replay.players[1].play_race)

                if (race1 == -1) or (race2 == -1):
                    print("Races invalides : replay ignoré")
                    continue

                map = mapToId(replay.map_name)

                supplyUsed1 = 0
                supplyUsed2 = 0
                totalIncome1 = 0
                totalIncome2 = 0
                mineralsIncome1 = 0
                mineralsIncome2 = 0
                vespeneIncome1 = 0
                vespeneIncome2 = 0
                totalResources1 = 0
                totalResources2 = 0
                minerals1 = 0
                minerals2 = 0
                vespene1 = 0
                vespene2 = 0
                activeWorkers1 = 0
                activeWorkers2 = 0
                army1 = 0
                army2 = 0
                technology1 = 0
                technology2 = 0
                lostResources1 = 0
                lostResources2 = 0

                for player in replay.players:
                    if player.result == "Win":
                        winner = player.pid - 1
                
                lastMeasurementTime = 0
                frameInterval = 10

                for event in replay.events:
                    if isinstance(event, PlayerStatsEvent):
                        if event.pid == 1:
                            supplyUsed1 = event.food_used
                            totalIncome1 = event.minerals_collection_rate + event.vespene_collection_rate
                            mineralsIncome1 = event.minerals_collection_rate
                            vespeneIncome1 = event.vespene_collection_rate
                            totalResources1 = event.minerals_current + event.vespene_current
                            minerals1 = event.minerals_current
                            vespene1 = event.vespene_current
                            activeWorkers1 = event.workers_active_count
                            army1 = event.minerals_used_current_army + event.vespene_used_current_army
                            technology1 = event.minerals_used_current_technology + event.vespene_used_current_technology
                            lostResources1 = event.resources_lost

                        elif event.pid == 2:
                            supplyUsed2 = event.food_used
                            totalIncome2 = event.minerals_collection_rate + event.vespene_collection_rate
                            mineralsIncome2 = event.minerals_collection_rate
                            vespeneIncome2 = event.vespene_collection_rate
                            totalResources2 = event.minerals_current + event.vespene_current
                            minerals2 = event.minerals_current
                            vespene2 = event.vespene_current
                            activeWorkers2 = event.workers_active_count
                            army2 = event.minerals_used_current_army + event.vespene_used_current_army
                            technology2 = event.minerals_used_current_technology + event.vespene_used_current_technology
                            lostResources2 = event.resources_lost

                            if frame >= (lastMeasurementTime + frameInterval):
                                time = frameToRealtime(frame)
                                writer.writerow([time, race1, race2, map, supplyUsed1, supplyUsed2, totalIncome1, totalIncome2, mineralsIncome1, mineralsIncome2, vespeneIncome1, vespeneIncome2, totalResources1, totalResources2, minerals1, minerals2, vespene1, vespene2, activeWorkers1, activeWorkers2, army1, army2, technology1, technology2, lostResources1, lostResources2, winner])
                                lastMeasurementTime = frame
                        
                        frame = event.frame

                    elif isinstance(event, PlayerLeaveEvent):
                        break
                
                else:
                    print("Le replay n'est pas un 1v1, dure moins d'une minute ou n'est pas sous l'expension Legacy of the Void : replay ignoré")
                    continue

def randomizeAndSplitDataset(datasetPercent, dataset, testDataset):
    shuffledDataset = "generatedDatasets/shuffledDataset.csv"
    
    fid = open(dataset, "r")
    li = fid.readlines()[1:]
    fid.close()

    random.shuffle(li)

    fid = open(shuffledDataset, "w")
    fid.writelines(li)
    fid.close()

    os.remove(dataset)

    rowsCopied = 0
    rowsToDelete = []

    with open(shuffledDataset, "r") as shuffled:
        csvReader = csv.reader(shuffled)
        allRows = list(csvReader)

    with open(testDataset, "w", newline = "") as test:
        csvWriter = csv.writer(test)
        csvWriter.writerow(header)

        for i, row in enumerate(allRows):
            if rowsCopied < (datasetPercent * len(dataset)):
                csvWriter.writerow(row)
                rowsToDelete.append(i)
                rowsCopied += 1

    with open(shuffledDataset, "w", newline = "") as shuffled:
        csvWriter = csv.writer(shuffled)
        csvWriter.writerow(header)

        for i, row in enumerate(allRows):
            if i not in rowsToDelete:
                csvWriter.writerow(row)

fullDatasetPercent = 0.8

generateDataset("replayBank", "generatedDatasets/dataset.csv")
randomizeAndSplitDataset(fullDatasetPercent, "generatedDatasets/dataset.csv", "generatedDatasets/testDataset.csv")