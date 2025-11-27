import pandas as pd
import os
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

combined_file = "combined_features/player_features_all_years.csv"
output_dir = "combined_features"
fig_dir = "figs"

os.makedirs(output_dir, exist_ok=True)
os.makedirs(fig_dir, exist_ok=True)

df = pd.read_csv(combined_file)
print(f"Loaded {df.shape[0]} player-season entries")

cluster_features = ['gs_diff', 'fg_pct_diff', 'to_rate_diff', 'clutch_game_score_min']
X = df[cluster_features].fillna(0)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

k = 4
kmeans = KMeans(n_clusters=k, random_state=42)
df['cluster'] = kmeans.fit_predict(X_scaled)

clustered_file = os.path.join(output_dir, "player_features_all_years_with_clusters.csv")
df.to_csv(clustered_file, index=False)
print(f"Saved clustered player features → {clustered_file}")

summary = df.groupby('cluster')[cluster_features].mean()
print("\nCluster summary:")
print(summary)

plt.figure(figsize=(8,6))
sns.scatterplot(
    data=df,
    x='gs_diff',
    y='fg_pct_diff',
    hue='cluster',
    palette='tab10',
    alpha=0.7
)
plt.xlabel('Game Score Diff (Clutch - Normal)')
plt.ylabel('FG% Diff (Clutch - Normal)')
plt.title('Clutch Player Clusters')
plt.legend(title='Cluster')
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'cluster_gs_vs_fg.png'))
plt.show()

sns.pairplot(df, vars=cluster_features, hue='cluster', palette='tab10', diag_kind='kde')
plt.suptitle('Clutch Player Cluster Pairplot', y=1.02)
plt.savefig(os.path.join(fig_dir, 'cluster_pairplot.png'))
plt.show()
