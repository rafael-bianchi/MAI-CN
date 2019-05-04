import igraph as ig
import networkx as nx
import matplotlib as plt

from .utils import utils

def run_community_dect_alg3(network, network_ig, layout, network_name, partition_reference, outputdir):
    """
    Finds communities in a graph using the Infomap method of Martin Rosvall and Carl T. Bergstrom.

    """
    
    algorithm_name = 'Infomap'
    print(f'Starting community_infomap(M. Rosvall...) for {network_name}')

    c = network_ig.community_infomap(edge_weights=network_ig.es['weight'] if network_ig.is_weighted() else None)

    danon, nvi, ji = utils.saveGraphImage(partition_reference, c.membership, c.modularity, network, layout, network_name, algorithm_name, outputdir)

    #utils.saveGraphImageIgraph(partition_reference, c, c.membership, network, layout, network_name, algorithm_name, outputdir)

    utils.saveCluster(c.membership, algorithm_name, network_name, outputdir)

    return c.modularity, danon, nvi, ji