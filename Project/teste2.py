#%%
import pickle

import networkx as nx

G = nx.Graph()
nx.spring_layout(G)

G.add_node("Rafael", x=34, y=-23.3)

nx.write_pajek(G, 'teste.net')