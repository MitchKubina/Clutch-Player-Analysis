from game_performance import game_performance
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def parse_clock(clock):
    """Convert MM:SS into seconds."""
    try:
        m, s = map(int, clock.split(':'))
        return m * 60 + s
    except:
        return 0


def find_all_diffs():
    file = "data/pbp2020.csv"
    year_df = pd.read_csv(file)

    year_df["clock_seconds"] = year_df["clock"].apply(parse_clock)
    year_df["time_left_seconds"] = year_df["clock_seconds"] + (4 - year_df["period"]) * 720

    last_2_minutes = year_df[year_df["time_left_seconds"] <= 120]
    first_46_minutes = year_df[year_df["time_left_seconds"] > 120]

    players = last_2_minutes["player"].dropna().unique()

    diffs = []
    overall_performance = []

    for player in players:
        clutch_score = game_performance(player, last_2_minutes)
        normal_score = game_performance(player, first_46_minutes)

        clutch_per_min = clutch_score / 2
        normal_per_min = normal_score / 46

        diff = clutch_per_min - normal_per_min

        diffs.append((player, diff))
        overall_performance.append((player, clutch_per_min))

    diffs_sorted = sorted(diffs, key=lambda x: x[1], reverse=True)
    performance_sorted = sorted(overall_performance, key=lambda x: x[1], reverse=True)

    print("Players who perform best in clutch time (relative diff):")
    for player, diff in diffs_sorted:
        print(f"{player}: {diff}")

    print("\nOverall Best Clutch Players (absolute score/min):")
    for player, score in performance_sorted:
        print(f"{player}: {score}")


if __name__ == "__main__":
    find_all_diffs()
