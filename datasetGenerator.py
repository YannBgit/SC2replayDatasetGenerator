import csv
import sc2reader
from sc2reader.events import PlayerStatsEvent, PlayerLeaveEvent
from os import path, listdir


def race_to_id(raceName):
    if raceName == "Terran":
        return 0
    
    elif raceName == "Zerg":
        return 1
    
    elif raceName == "Protoss":
        return 2

def frame_to_realtime(frame):
    return round(frame / 22.4)

def generate_dataset(indir, outfile):
    with open(outfile, "w", newline = "") as csv_file:
    
        writer = csv.writer(csv_file)
        writer.writerow(["time", "race1", "race2", "supplyMade1", "supplyMade2", "supplyUsed1", "supplyUsed2", "totalIncome1", "totalIncome2", "mineralsIncome1", "mineralsIncome2", "vespeneIncome1", "vespeneIncome2", "totalResources1", "totalResources2", "minerals1", "minerals2", "vespene1", "vespene2", "activeWorkers1", "activeWorkers2", "army1", "army2", "technology1", "technology2", "lostResources1", "lostResources2", "winner"])

        for filename in [f for f in listdir(indir) if f.endswith(".SC2Replay")]:
            print("Extracting from", filename, "...")
            replay = sc2reader.load_replay(path.join(indir, filename))

            frame = 0
            race1 = race_to_id(replay.players[0].play_race)
            race2 = race_to_id(replay.players[1].play_race)

            supplyMade1 = 0
            supplyMade2 = 0
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
            
            last_measurement_frame = 0
            frame_interval = 112

            for event in replay.events:
                if isinstance(event, PlayerStatsEvent):
                    if event.pid == 1:
                        supplyMade1 = event.food_made
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
                        supplyMade2 = event.food_made
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
                    
                    frame = event.frame

                elif isinstance(event, PlayerLeaveEvent):
                    break

                if frame >= (last_measurement_frame + frame_interval):
                    time = frame_to_realtime(frame)
                    writer.writerow([time, race1, race2, supplyMade1, supplyMade2, supplyUsed1, supplyUsed2, totalIncome1, totalIncome2, mineralsIncome1, mineralsIncome2, vespeneIncome1, vespeneIncome2, totalResources1, totalResources2, minerals1, minerals2, vespene1, vespene2, activeWorkers1, activeWorkers2, army1, army2, technology1, technology2, lostResources1, lostResources2, winner])
                    last_measurement_frame = frame

generate_dataset("replays/trainSet", "generatedDatasets/trainSet.csv")
generate_dataset("replays/testSet", "generatedDatasets/testSet.csv")