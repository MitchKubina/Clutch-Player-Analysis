import pandas as pd
import matplotlib.pyplot as plt
import os

rankings_file = "rankings/top100_clutch_players_all_years.csv"
fig_dir = "figs"

os.makedirs(fig_dir, exist_ok=True)

print("Loading clutch rankings...")
df = pd.read_csv(rankings_file)

top15 = df.head(15)

top15 = top15.sort_values("clutch_score", ascending=True)

print("Generating Top 15 Clutch Players plot...")

plt.figure(figsize=(10, 8))
plt.barh(top15["player"], top15["clutch_score"])

plt.xlabel("Clutch Score")
plt.ylabel("Player")
plt.title("Top 15 Clutch Players (All Years Combined)")

plt.tight_layout()

output_path = os.path.join(fig_dir, "top15_clutch_players.png")
plt.savefig(output_path)
plt.show()

print(f"Saved figure → {output_path}")
