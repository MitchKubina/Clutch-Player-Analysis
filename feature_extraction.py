import pandas as pd
from game_performance import game_performance
import os

def extract_stats(player_df):
    stats = {
        "points": 0,
        "fgm": 0,
        "fga": 0,
        "ftm": 0,
        "ft_miss": 0,
        "oreb": 0,
        "dreb": 0,
        "ast": 0,
        "stl": 0,
        "blk": 0,
        "tov": 0,
        "pf": 0,
    }

    for _, row in player_df.iterrows():
        play = row["type"]
        desc = row["desc"]

        desc = row["desc"] if isinstance(row["desc"], str) else ""

        if play == "Made Shot":
            stats["fga"] += 1
            stats["fgm"] += 1
            stats["points"] += 3 if "3PT" in desc else 2

        elif play == "Missed Shot":
            stats["fga"] += 1

        elif play == "Free Throw":
            if "MISS" in desc:
                stats["ft_miss"] += 1
            else:
                stats["ftm"] += 1
                stats["points"] += 1

        elif play == "Rebound":
            if "off" in row and row["off"] == 1:
                stats["oreb"] += 1
            else:
                stats["dreb"] += 1

        elif "STEAL" in desc:
            stats["stl"] += 1

        elif "assist" in desc or "AST" in desc:
            stats["ast"] += 1

        elif play == "Turnover":
            stats["tov"] += 1

        elif play == "Block":
            stats["blk"] += 1

        elif play == "Foul":
            stats["pf"] += 1

    return stats


def compute_features(stats, minutes):
    fgm = stats["fgm"]
    fga = stats["fga"]
    ftm = stats["ftm"]
    ft_miss = stats["ft_miss"]
    tov = stats["tov"]

    fg_pct = fgm / fga if fga > 0 else 0
    ft_pct = ftm / (ftm + ft_miss) if (ftm + ft_miss) > 0 else 0
    to_rate = tov / minutes if minutes > 0 else 0

    return {
        "fg_pct": fg_pct,
        "ft_pct": ft_pct,
        "tov_rate": to_rate,
        "oreb": stats["oreb"] / minutes if minutes else 0,
        "dreb": stats["dreb"] / minutes if minutes else 0,
        "ast": stats["ast"] / minutes if minutes else 0,
        "stl": stats["stl"] / minutes if minutes else 0,
        "blk": stats["blk"] / minutes if minutes else 0,
        "game_score_per_min": 0,  # filled later
    }


def extract_player_features(year_df):
    players = year_df["player"].dropna().unique()

    def parse_clock(clock):
        try:
            m, s = map(int, clock.split(":"))
            return m * 60 + s
        except:
            return 0

    year_df["clock_seconds"] = year_df["clock"].apply(parse_clock)
    year_df["time_left_seconds"] = year_df["clock_seconds"] + (4 - year_df["period"]) * 720

    clutch = year_df[year_df["time_left_seconds"] <= 120]
    normal = year_df[year_df["time_left_seconds"] > 120]

    rows = []

    for player in players:
        clutch_df = clutch[clutch["player"] == player]
        normal_df = normal[normal["player"] == player]

        clutch_min = 2
        normal_min = 46

        clutch_stats = extract_stats(clutch_df)
        normal_stats = extract_stats(normal_df)

        clutch_features = compute_features(clutch_stats, clutch_min)
        normal_features = compute_features(normal_stats, normal_min)

        clutch_features["game_score_per_min"] = game_performance(player, clutch) / 2
        normal_features["game_score_per_min"] = game_performance(player, normal) / 46

        row = {
            "player": player,
            "clutch_fg_pct": clutch_features["fg_pct"],
            "normal_fg_pct": normal_features["fg_pct"],
            "fg_pct_diff": clutch_features["fg_pct"] - normal_features["fg_pct"],

            "clutch_to_rate": clutch_features["tov_rate"],
            "normal_to_rate": normal_features["tov_rate"],
            "to_rate_diff": clutch_features["tov_rate"] - normal_features["tov_rate"],

            "clutch_game_score_min": clutch_features["game_score_per_min"],
            "normal_game_score_min": normal_features["game_score_per_min"],
            "gs_diff": clutch_features["game_score_per_min"] - normal_features["game_score_per_min"],
        }

        rows.append(row)

    return pd.DataFrame(rows)


if __name__ == "__main__":
    pbp_dir = "data"
    features_dir = "features_by_year"
    combined_dir = "combined_features"

    os.makedirs(features_dir, exist_ok=True)
    os.makedirs(combined_dir, exist_ok=True)

    all_years = range(1997, 2024)
    all_features = []

    for year in all_years:
        pbp_file = os.path.join(pbp_dir, f"pbp{year}.csv")
        if os.path.exists(pbp_file):
            print(f"Processing {pbp_file} ...")
            year_df = pd.read_csv(pbp_file)
            df = extract_player_features(year_df)
            df["year"] = year

            yearly_file = os.path.join(features_dir, f"player_features_{year}.csv")
            df.to_csv(yearly_file, index=False)
            print(f"Saved → {yearly_file}")

            all_features.append(df)
        else:
            print(f"Warning: {pbp_file} not found, skipping.")

    combined_file = os.path.join(combined_dir, "player_features_all_years.csv")
    combined_df = pd.concat(all_features, ignore_index=True)
    combined_df.to_csv(combined_file, index=False)
    print(f"\nSaved combined features → {combined_file}")
