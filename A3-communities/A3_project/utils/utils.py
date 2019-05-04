import fnmatch
import math
import os
from pathlib import Path

import numpy as np
import community
import igraph as ig
import matplotlib.pyplot as plt
import networkx as nx
from sklearn import metrics


def getReferencePartition(netFileName, numberOfNodes, rootFolder):
    """ Finds, reads and returns a partition reference for a given pajek file.

    Keyword arguments:
    netFileName -- Pajek file name (without extension)
    numberOfNodes -- Number of nodes of the Graph read from Pajek file (just for checking)
    rootFolder -- Folder which will be searched for a .clu file.
    """ 

    #Some names are hard-coded
    if(netFileName == 'rb125'): netFileName = netFileName + '-1'
    if(netFileName == 'dolphins' or
       netFileName == 'zachary_unwh'): netFileName = netFileName + '-real'
    if(netFileName == 'football'): netFileName = netFileName + '-conferences'

    partition = []
    partFile = Path(os.path.join(rootFolder, netFileName + '.clu'))
    node_verify = 0

    if(partFile.is_file()):
        with open(partFile, 'r') as f:
            fileData = f.read()
            for line in fileData.splitlines(False)[1:]:
                partition.append(int(line)-1)
                node_verify = node_verify + 1
        
        assert node_verify == numberOfNodes, "Cluster file nodes does not match with pajek file."
        
        return partition
    else :
        return None



def readNetworks(path='A3_project/networks'):
    """ Returns all networks and their partition references for a given path.

    Keyword arguments:
    path -- Path that will be searched for .net files (default A3_project/networks)
    """ 

    networks = []
    pajek = None
    netname = None
    net = None
    partition_reference = None

    for root, _, files in os.walk(path):
        for f in fnmatch.filter(files, '*.net'):
            netname = os.path.splitext(os.path.basename(f))[0]
            
            #Networkx
            pajek = nx.read_pajek(os.path.join(root, f))
            net = nx.Graph(pajek)
        
            #igraph
            net_igraph = ig.read(os.path.join(root, f))

            pos = None
            layout = None
            
            #Get the positions
            #if hasattr(net_igraph.vs, 'x') and hasattr(net_igraph.vs, 'y'):

            print(f'Started getting coordinates for {netname}')
            try:
                coord_x = net_igraph.vs['x']
                coord_y = net_igraph.vs['y']

                ids = net_igraph.vs['id']

                pos = dict(zip(ids, np.asarray([[float(x), -float(y)] for x, y in zip(coord_x, coord_y)])))
                layout = list(zip(coord_x, coord_y))
                print('Got coordinates from the file.')
            except:
                pos = nx.kamada_kawai_layout(net)
                layout = net_igraph.layout('kk')

            print(f'Finished getting coordinates for {netname}')

            #Partition reference - if exists
            partition_reference = getReferencePartition(netname, len(net), root)

            network = {
                "network": net,
                "network_igraph": net_igraph,
                "network_name": os.path.splitext(os.path.basename(f))[0],
                "pos": pos,             #for networkx
                "layout": layout,       #for Igraph
                "partition_reference": partition_reference
            }

            networks.append(network)
    
    return networks

def saveGraphImageReference(network, pos, network_name, partition_reference, outputdir):
    saveGraphImage(None, partition_reference, 0, network, pos, network_name, 'reference', outputdir)

def saveGraphImage(partition_reference, communities, modularity, network, pos, network_name, algorithm_name, outputdir):
    graph_title = f'{network_name} - {algorithm_name} algorithm - Modularity {modularity}'
    

    danon = None    
    nvi = None
    ji = None
    if(partition_reference != None):
        danon = ig.compare_communities(partition_reference, communities, method='danon')       
        nvi = ig.compare_communities(partition_reference, communities, method='vi')/math.log(len(network))
        ji = metrics.jaccard_similarity_score(partition_reference, communities, normalize=True)
        graph_title = graph_title + f'\nJaccard Index: {ji}\nNormalized Mutual Information: {danon}\nNormalized Variation of Information: {nvi}'
    
    directory = os.path.join(outputdir, 'images', network_name)
    if not os.path.exists(directory):
        os.makedirs(directory)

    out_file = os.path.join(directory,f'{network_name}-{algorithm_name}.png') 

    fig = plt.figure()
    nx.draw_networkx(network, pos, cmap='jet', node_color=communities, node_size=100, with_labels=False)

    plt.title(graph_title, fontsize=8)
    plt.savefig(out_file)
    plt.close(fig)


    return danon, nvi, ji
def saveCluster(community, algorithm_name, network_name, outputdir):
    directory = os.path.join(outputdir, 'clusters', network_name)
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    out_file = os.path.join(directory,f'cluster-{algorithm_name}.clu') 

    with open(out_file, 'w') as f:
        f.write(f'*Vertices {len(community)}\n')
        f.writelines(f"{c+1}\n" for c in community)

def saveMetrics(networks, outputdir):
    directory = os.path.join(outputdir, 'metrics')
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    out_file = os.path.join(directory, 'network-metrics.txt') 
    with open(out_file, 'w') as f:
        f.write('NetworkName\tClauset-Newman-Moore-Modularity\tClauset-Newman-Moore-danon\tClauset-Newman-Moore-nvi\tClauset-Newman-Moore-ji\tLouvain-Modularity\tLouvain-danon\tLouvain-nvi\tLouvain-ji\tInfomap-Modularity\tInfomap-danon\tInfomap-nvi\tInfomap-ji\n')
        for network in networks:
            f.write(f'{network["network_name"]}\t')
            f.write(f' {network["metrics"]["Clauset-Newman-Moore"][0]}\t{network["metrics"]["Clauset-Newman-Moore"][1]}\t{network["metrics"]["Clauset-Newman-Moore"][2]}\t{network["metrics"]["Clauset-Newman-Moore"][3]}\t')
            f.write(f' {network["metrics"]["Louvain"][0]}\t{network["metrics"]["Louvain"][1]}\t{network["metrics"]["Louvain"][2]}\t{network["metrics"]["Louvain"][3]}\t')
            f.write(f' {network["metrics"]["Infomap"][0]}\t{network["metrics"]["Infomap"][1]}\t{network["metrics"]["Infomap"][2]}\t{network["metrics"]["Infomap"][3]}\t\n')