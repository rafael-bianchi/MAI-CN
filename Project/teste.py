import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap as Basemap
from matplotlib.patches import Polygon

fig, ax = plt.subplots()
m = Basemap(projection='merc', llcrnrlat=-35, urcrnrlat=7,
            llcrnrlon=-77, urcrnrlon=-32, resolution='i')
m.ax = ax
m.drawstates()

shp = m.readshapefile('cn_project\mapdata\gadm36_BRA_0', 'states', drawbounds=True)
for nshape, seg in enumerate(m.states):
    poly = Polygon(seg, facecolor='0.75', edgecolor='k')
    ax.add_patch(poly)

plt.show()
