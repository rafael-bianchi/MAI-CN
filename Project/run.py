#%%
import pickle
import random


import community
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import Polygon
from mpl_toolkits.basemap import Basemap as Basemap

import cn_project.datafetcher as datafetcher
import cn_project.utils as utils

# This method starts the fetching process on the 
# brazilian government website to refresh all the data.
# The data is pre-stored in the pickle files and then, processed
# and saved in a pajek network format
# !!!!! This method might take several hours to complete. !!!!!
refreshData = False
if (refreshData):
    datafetcher.refresh_data()

# parties_pickle = open("cn_project/data/parties.pickle","rb")
# ps = pickle.load(parties_pickle)

# props_pickle = open("cn_project/data/propositions.pickle","rb")
# props = pickle.load(props_pickle)

# vote_pickle = open("cn_project/data/votes.pickle","rb")
# vs = pickle.load(vote_pickle)

# congressman_pickle = open("cn_project/data/congressmen.pickle","rb")
# cms = pickle.load(congressman_pickle)


###########################################################################
# Start - Parties - Community detection and ploting 
###########################################################################
g_parties = nx.Graph(nx.read_pajek( 'cn_project/data/g_parties.net'))

partition = community.best_partition(g_parties)
size = float(len(set(partition.values())))
pos = nx.circular_layout(g_parties, scale=.1)

p_values = list(pos.values())
random.shuffle(p_values)

i = 0
for p in pos.keys():
    pos[p] = p_values[i]
    i += 1

nodes_index = {}

for node_name, node in g_parties.node.items(): 
    nodes_index[node_name] = int(node['id'])-1

dict_communities = community.best_partition(g_parties)

com_linear = [None] * len(g_parties)

for n_id in nodes_index:
    com_linear[nodes_index[n_id]] = dict_communities[n_id]

nx.draw_networkx_nodes(g_parties, pos, cmap='jet', node_color=com_linear, node_size=100)

edges_weights, _, _, _ = utils.rescale_weights(g_parties, 0.1, 10)

nx.draw_networkx_edges(g_parties, pos, width=list(edges_weights.values()))

nx.draw_networkx_labels(g_parties, pos, font_size=14, font_color='#008080', font_family='sans-serif')

plt.axis('off')
plt.show()
###########################################################################
# End - Parties - Community detection and ploting 
###########################################################################


###########################################################################
# Start - Parties - Community detection and ploting 
###########################################################################
g_states = nx.Graph(nx.read_pajek('cn_project/data/g_states.net'))
x = nx.get_node_attributes(g_states, 'x')
y = nx.get_node_attributes(g_states, 'y')

fig, ax = plt.subplots()
m = Basemap(projection='merc', llcrnrlat=-35, urcrnrlat=7,
            llcrnrlon=-77, urcrnrlon=-32, resolution='i')
m.ax = ax
m.drawstates()

shp = m.readshapefile('cn_project\mapdata\gadm36_BRA_0', 'states', drawbounds=True)
for nshape, seg in enumerate(m.states):
    poly = Polygon(seg, facecolor='#00db00', edgecolor='k',zorder=0)
    ax.add_patch(poly)

# position in decimal lat/lon
lats= list(x.values())
lons= list(y.values())
# convert lat and lon to map projection
mx,my=m(lons,lats)

# The NetworkX part
# put map projection coordinates in pos dictionary
count=0
m_based_locs = {}
for key in x:
    m_based_locs[key] = (mx[count], my[count])
    count += 1

# draw
nx.draw_networkx_nodes(g_states,m_based_locs,node_size=100,node_color='k')

edges_weights, edges_colors, _, _ = utils.rescale_weights(g_states, 0.1, 3)

for edge in edges_weights:
    nx.draw_networkx_edges(g_states, m_based_locs, edgelist=[edge],
                       width=edges_weights[edge], edge_color=str(edges_colors[edge][0]))

nx.draw_networkx_labels(g_states, m_based_locs, font_size=14, font_color='white', font_family='sans-serif')

plt.show()


###########################################################################
# End - Parties - Community detection and ploting 
###########################################################################


# nx.draw(g_parties, pos=nx.spring_layout(g_parties))
# plt.draw()  # pyplot draw(
# plt.show()

# g_congressmen = nx.Graph(nx.read_pajek( 'cn_project/data/voting_relation_congressmen.net'))

# g_states = nx.Graph(nx.read_pajek( 'cn_project/data/g_states.net'))

#%%
