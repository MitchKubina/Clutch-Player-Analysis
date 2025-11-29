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


#k = 4
ks = range(3,11)
k_distances = []


for k in ks:
    kmeans = KMeans(n_clusters = k, random_state = 42)
    cluster_string = f"cluster_{k}"
    
    df[cluster_string] = kmeans.fit_predict(X_scaled)

    avg_distance = (kmeans.inertia_ / len(df)) ** 0.5
    k_distances.append(avg_distance)

    clustered_file = os.path.join(output_dir, f"player_features_all_years_with_{k}_clusters.csv")
    df.to_csv(clustered_file, index=False)
    print(f"Saved clustered player features → {clustered_file}")

    summary = df.groupby(cluster_string)[cluster_features].mean()
    print("\n", f"Cluster summary for {k} clusters:")
    print(summary)

'''
kmeans = KMeans(n_clusters=k, random_state=42)
df['cluster'] = kmeans.fit_predict(X_scaled)



clustered_file = os.path.join(output_dir, "player_features_all_years_with_clusters.csv")
df.to_csv(clustered_file, index=False)
print(f"Saved clustered player features → {clustered_file}")


summary = df.groupby('cluster')[cluster_features].mean()
print("\nCluster summary:")
print(summary)
'''
#7 seems to be the most elbow-y?
plt.title("Comparison of Clusters and Distance")
plt.ylabel("Avg Distance")
plt.xlabel("Cluster")
plt.plot(ks, k)

all_cluster_names = [
    'cluster_3', 'cluster_4', 'cluster_5', 'cluster_6',
    'cluster_7', 'cluster_8', 'cluster_9', 'cluster_10'
]
fig, axes = plt.subplots(2, 4, figsize=(16, 8))
axes = axes.flatten()

for ax, cluster in zip(axes, all_cluster_names):
    sns.scatterplot(
        data=df,
        x='gs_diff',
        y='fg_pct_diff',
        hue=cluster,
        palette='tab10',
        alpha=0.7,
        ax=ax
    )
    ax.set_title(cluster)

plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'all_clusters_gs_vs_fg.png'))
plt.show()
'''
plt.figure(figsize=(8,6))
sns.scatterplot(
    data=df,
    x='gs_diff',
    y='fg_pct_diff',
    hue='cluster',
    palette='tab10',
    alpha=0.7
)
'''
'''
plt.xlabel('Game Score Diff (Clutch - Normal)')
plt.ylabel('FG% Diff (Clutch - Normal)')
plt.title('Clutch Player Clusters')
plt.legend(title='Cluster')
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'cluster_gs_vs_fg.png'))
plt.show()
'''

'''
for k in ks:
    hue_string = f"cluster_{k}"
    sns.pairplot(df, vars=cluster_features, hue=hue_string, palette='tab10', diag_kind='kde')
    plt.suptitle('Clutch Player Cluster Pairplot', y=1.02)
    plt.savefig(os.path.join(fig_dir, f'cluster_pairplot_with_{k}_clusters.png'))
    plt.show()
'''
    

print("\nComputing final clutch score...")

scaler2 = StandardScaler()
normalized = scaler2.fit_transform(df[cluster_features].fillna(0))
df[['gs_diff_norm', 'fg_pct_diff_norm', 'to_rate_diff_norm', 'clutch_gs_min_norm']] = normalized

df['clutch_score'] = (
    0.5 * df['gs_diff_norm'] +
    0.3 * df['fg_pct_diff_norm'] -
    0.2 * df['to_rate_diff_norm']
)

if 'year' not in df.columns:
    if 'season' in df.columns:
        df['year'] = df['season']
    else:
        print("WARNING: No 'year' column found. Setting all to -1.")
        df['year'] = -1

rank_dir = "rankings"
os.makedirs(rank_dir, exist_ok=True)

for year in sorted(df['year'].unique()):
    if year == -1:
        continue

    year_df = df[df['year'] == year] \
                .sort_values('clutch_score', ascending=False) \
                .head(20)

    output_file = os.path.join(rank_dir, f"top20_clutch_players_{year}.csv")
    year_df[['player', 'clutch_score', 'gs_diff', 'fg_pct_diff', 'to_rate_diff']] \
        .to_csv(output_file, index=False)

    print(f"Saved → {output_file}")

overall = df.sort_values('clutch_score', ascending=False).head(100)
overall_file = os.path.join(rank_dir, "top100_clutch_players_all_years.csv")
overall[['player', 'year', 'clutch_score']].to_csv(overall_file, index=False)

print(f"\nSaved → {overall_file}")
print("Clutch score computation complete.")