# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 23:42:38 2021

@author: Harry
"""

import pandas as pd
import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from os import path
from sklearn.preprocessing import normalize
from sklearn.cluster import AgglomerativeClustering
import scipy.cluster.hierarchy as shc

DATA_DIR = 'C:\\Users\\Harry\\Documents\\LTCWFF\\ltcwff_files\\data'

team_data = pd.read_csv(path.join(DATA_DIR, 'team_data.csv'))

team_data

num_vars = ['FG%/G', 'TRB/G', 'AST/G', 'STL/G', 'BLK/G', 'PTS/G', 'OPP FG%/G', 'OPP TRB/G', 'OPP AST/G', 'OPP STL/G', 'OPP BLK/G', 'OPP PTS/G']
team_data_filtered = team_data[num_vars]

teams = [ f'{team}_{year}' for (team, year) in zip(team_data['Team'], team_data['Year']) ]
teams

team_data_filtered.insert(0, 'Team', teams)
team_data_filtered.set_index('Team', inplace = True)
team_data_filtered

team_data_scaled = normalize(team_data_filtered)
team_data_scaled = pd.DataFrame(team_data_scaled, columns = team_data_filtered.columns)
team_data_scaled.insert(0, 'Team', teams)
team_data_scaled.set_index('Team', inplace = True)
team_data_scaled

plt.figure(figsize = (10, 7))
plt.title('Dendrograms')
dend = shc.dendrogram(shc.linkage(team_data_scaled, method = 'ward'))
plt.axhline(y = 0.10, color = 'r', linestyle = '--')

cluster = AgglomerativeClustering(n_clusters = 6, affinity = 'euclidean', linkage = 'ward')
team_clusters = cluster.fit_predict(team_data_scaled)

groups = []

team_data_filtered['Cluster'] = np.nan

for i in range(6):
    group = []
    for j in range(len(team_clusters)):
        if team_clusters[j] == i:
            group.append(team_data_filtered.iloc[j].name)
            team_data_filtered['Cluster'].iloc[j] = i
    groups.append(group)
    
cluster_stats = []

for i in range(6):
    cluster_stats.append(team_data_filtered.loc[team_data_filtered['Cluster'] == i].mean().to_frame().transpose())
    
cluster_stats = pd.concat(cluster_stats)
cluster_stats.set_index('Cluster')
    
groups = pd.DataFrame(groups)
groups
groups.to_csv(path.join(DATA_DIR, 'team_groupings.csv'))

plt.figure(figsize = (10, 7))
plt.scatter(team_data_scaled['FG%/G'], team_data_scaled['OPP FG%/G'], c = cluster.labels_)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter3D(team_data_scaled['FG%/G'], team_data_scaled['TRB/G'], team_data_scaled['OPP FG%/G'], c = cluster.labels_)
