import csv
import sc2reader
from sc2reader.events import PlayerStatsEvent
from os import path, listdir


def race_to_id(raceName):
    if raceName == "Terran":
        return 0
    
    elif raceName == "Zerg":
        return 1
    
    elif raceName == "Protoss":
        return 2

indir = "replays"
outdir = "csvOutput"

with open(outdir + "/replaysDataset.csv", "w", newline = "") as csv_file:
    
    writer = csv.writer(csv_file)
    writer.writerow(["time", "race1", "race2", "supply1", "supply2", "income1", "income2", "workers1", "workers2", "army1", "army2", "technology1", "technology2", "floatingResources1", "floatingResources2", "lostResources1", "lostResources2", "winnerNumber"])

    for filename in [f for f in listdir(indir) if f.endswith(".SC2Replay")]:
        print("Extracting", filename, "...")
        replay = sc2reader.load_replay(path.join(indir, filename))

        time = 0
        race1 = race_to_id(replay.players[0].play_race)
        race2 = race_to_id(replay.players[1].play_race)
        supply1 = 0
        supply2 = 0
        income1 = 0
        income2 = 0
        workers1 = 12
        workers2 = 12
        army1 = 0
        army2 = 0
        technology1 = 0
        technology2 = 0
        floatingResources1 = 50
        floatingResources2 = 50
        lostResources1 = 0
        lostResources2 = 0

        for player in replay.players:
            if player.result == "Win":
                winnerNumber = player.pid
        
        last_measurement_time = 0
        interval = 30

        for event in replay.events:
            if isinstance(event, PlayerStatsEvent):
                if event.pid == 1:
                    supply1 = event.food_used
                    income1 = event.minerals_collection_rate + event.vespene_collection_rate
                    workers1 = event.workers_active_count
                    army1 = event.minerals_used_current_army + event.vespene_used_current_army
                    technology1 = event.minerals_used_current_technology + event.vespene_used_current_technology
                    floatingResources1 = event.minerals_current + event.vespene_current
                    lostResources1 = event.resources_lost

                elif event.pid == 2:
                    supply2 = event.food_used
                    income2 = event.minerals_collection_rate + event.vespene_collection_rate
                    workers2 = event.workers_active_count
                    army2 = event.minerals_used_current_army + event.vespene_used_current_army
                    technology2 = event.minerals_used_current_technology + event.vespene_used_current_technology
                    floatingResources2 = event.minerals_current + event.vespene_current
                    lostResources2 = event.resources_lost
                
                time = event.second

            if time >= (last_measurement_time + interval):
                writer.writerow([time, race1, race2, supply1, supply2, income1, income2, workers1, workers2, army1, army2, technology1, technology2, floatingResources1, floatingResources2, lostResources1, lostResources2, winnerNumber])
                last_measurement_time = event.second