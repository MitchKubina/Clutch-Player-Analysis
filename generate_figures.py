import pandas as pd
import matplotlib.pyplot as plt
import os

rankings_file = "rankings/top100_clutch_players_all_years.csv"
yearly_rankings_dir = "rankings"
fig_dir = "figs"

os.makedirs(fig_dir, exist_ok=True)

print("Loading clutch rankings...")
df = pd.read_csv(rankings_file)

top15 = df.head(15)
top15 = top15.sort_values("clutch_score", ascending=True)

print("Generating Top 15 Clutch Players figure...")

plt.figure(figsize=(10, 8))
plt.barh(top15["player"], top15["clutch_score"])
plt.xlabel("Clutch Score")
plt.ylabel("Player")
plt.title("Top 15 Clutch Players (All Years)")
plt.tight_layout()

output_path1 = os.path.join(fig_dir, "top15_clutch_players.png")
plt.savefig(output_path1)
plt.show()

print(f"Saved figure → {output_path1}")

print("\nGenerating Top Player per Year figure...")

yearly_files = [
    f for f in os.listdir(yearly_rankings_dir)
    if f.startswith("top20_clutch_players_") and f.endswith(".csv")
]

year_list = []
player_list = []
score_list = []

for file in yearly_files:
    year = file.replace("top20_clutch_players_", "").replace(".csv", "")
    year = int(year)

    year_df = pd.read_csv(os.path.join(yearly_rankings_dir, file))

    top_player = year_df.iloc[0]

    year_list.append(year)
    player_list.append(top_player["player"])
    score_list.append(top_player["clutch_score"])

top_by_year_df = pd.DataFrame({
    "year": year_list,
    "player": player_list,
    "clutch_score": score_list
}).sort_values("year")

plt.figure(figsize=(12, 6))
plt.plot(top_by_year_df["year"], top_by_year_df["clutch_score"], marker="o", linewidth=2)

# Add labels above each point
for i, row in top_by_year_df.iterrows():
    plt.text(row["year"], row["clutch_score"] + 0.05, row["player"], fontsize=8, ha='center')

plt.xlabel("Year")
plt.ylabel("Clutch Score")
plt.title("Top Clutch Player Each Season (1997–2023)")
plt.grid(True, alpha=0.3)
plt.tight_layout()

output_path2 = os.path.join(fig_dir, "top_player_per_year.png")
plt.savefig(output_path2)
plt.show()

print(f"Saved figure → {output_path2}")

print("\nAll figures generated successfully!")