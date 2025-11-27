import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""
NBA Game Score Formula:
Game Score = PTS
           + 0.4 * FGM
           + 0.7 * OREB
           + 0.3 * DREB
           + STL
           + 0.7 * AST
           + 0.7 * BLK
           - 0.7 * FGA
           - 0.4 * FT Miss
           - 0.4 * PF
           - TOV
"""

def game_performance(player, table):

    player_df = table[table["player"] == player]

    points = 0
    fgm = 0
    fga = 0
    ftm = 0
    ft_miss = 0
    oreb = 0
    dreb = 0
    steals = 0
    assists = 0
    blocks = 0
    turnovers = 0
    fouls = 0

    for _, row in player_df.iterrows():
        play = row["type"]
        desc = row["desc"]

        desc = row["desc"] if isinstance(row["desc"], str) else ""

        if play == "Made Shot":
            fgm += 1
            fga += 1
            points += 3 if "3PT" in desc else 2

        elif play == "Missed Shot":
            fga += 1

        elif play == "Free Throw":
            if "MISS" in desc:
                ft_miss += 1
            else:
                points += 1
                ftm += 1

        elif play == "Rebound":
            if "off" in row and row["off"] == 1:
                oreb += 1
            else:
                dreb += 1

        elif "STEAL" in desc:
            steals += 1

        elif "assist" in desc or "AST" in desc:
            assists += 1

        elif play == "Turnover":
            turnovers += 1

        elif play == "Block":
            blocks += 1

        elif play == "Foul":
            fouls += 1

    game_score = (
        points
        + 0.4 * fgm
        + 0.7 * oreb
        + 0.3 * dreb
        + steals
        + 0.7 * assists
        + 0.7 * blocks
        - 0.7 * fga
        - 0.4 * ft_miss
        - 0.4 * fouls
        - turnovers
    )

    return game_score


def get_all_players(table):
    return table["player"].unique()


def test_performance():
    first_table = pd.read_csv("data/pbp2023.csv")

    names = get_all_players(first_table)
    scores = [game_performance(name, first_table) for name in names]

    names = np.asarray(names)
    scores = np.asarray(scores)
    indices = np.argsort(scores)

    best_names = names[indices][-20:]
    best_scores = scores[indices][-20:]

    plt.barh(best_names, best_scores)
    plt.xlabel("Game Score")
    plt.ylabel("Player")
    plt.title("Top 20 Players by Game Score (2023)")
    plt.show()


if __name__ == "__main__":
    test_performance()
