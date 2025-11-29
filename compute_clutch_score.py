import pandas as pd
import matplotlib.pyplot as plt

def compute_clutch_score(df):
    df = df.fillna(0)

    df["clutch_score"] = (
        0.50 * df["gs_diff"] +     
        0.30 * df["fg_pct_diff"] - 
        0.20 * df["to_rate_diff"] 
    )
    
    return df


def top_clutch_players(df, n=20):
    
    sorted_df = df.sort_values("clutch_score", ascending=False)
    top_players = sorted_df.head(n)
    return top_players


def plot_top_clutch_players(df, top_n=10):
    
    top_players = df.sort_values("clutch_score", ascending=False).head(top_n)

    plt.figure(figsize=(12, 6))
    plt.bar(top_players["player"], top_players["clutch_score"], color='orange')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel("Player")
    plt.ylabel("Clutch Score")
    plt.title(f"Top {top_n} Clutch Players – 2020")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    df = pd.read_csv("features_by_year/player_features_2020.csv")

    df = compute_clutch_score(df)

    top20 = top_clutch_players(df)
    print("Top 20 Clutch Players of 2020:")
    print(top20[["player", "clutch_score", "gs_diff", "fg_pct_diff", "to_rate_diff"]])

    top20.to_csv("top20_clutch_players_2020.csv", index=False)
    print("\nSaved → top20_clutch_players_2020.csv")

    plot_top_clutch_players(df, top_n=10)
