from game_performance import game_performance
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import isodate

def find_all_diffs():
    all_files = os.listdir('data')
    
    diffs = []
    overall_performance = []
    
    file = "data/pbp2020.csv"

    year_df = pd.read_csv(file)
    # Separate by time period 
    year_df["time_left_seconds"] = (year_df["clock"].apply(lambda x: isodate.parse_duration(x).total_seconds()) + 720 * (4 - year_df["period"] ))
    last_2_minutes = year_df[year_df['time_left_seconds'] <= 120]
    first_46_minutes = year_df[year_df['time_left_seconds'] > 120]

    players = last_2_minutes['player'].unique()

    for player in players:
        #Average score per minute
        last_2_min_score = game_performance(player, last_2_minutes)/2
        first_46_min_score = game_performance(player, first_46_minutes)/46

        diff = last_2_min_score - first_46_min_score
        diffs.append((player, diff))
        overall_performance.append((player, last_2_min_score))
    
    diffs_sorted = sorted(diffs, key=lambda x: x[1], reverse=True)
    performance_sorted = sorted(overall_performance, key=lambda x: x[1], reverse=True)

    print("Players who perform the best in clutch time compared to rest of game:")
    for player, diff in diffs_sorted:
        print(f"{player}: {diff}")

    print("\nOverall Best Players in Clutch Time:")
    for player, score in performance_sorted:
        print(f"{player}: {score}") 



if __name__ == "__main__":
    find_all_diffs()