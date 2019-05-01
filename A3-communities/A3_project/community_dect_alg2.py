import community
import networkx as nx

from .utils import utils

def run_community_dect_alg2(network, pos, network_name, partition_reference, outputdir):
    """
    Finds communities in a graph using the Louvain Community Detection method

    community best_partition method.
    """
    
    algorithm_name = 'Louvain'
    print(f'Starting best_partition(Louvain) for {network_name}')

    nodes_index = {}

    for node_name, node in network.node.items(): 
        nodes_index[node_name] = int(node['id'])-1

    dict_communities = community.best_partition(network)

    com_linear = [None] * len(network)

    for n_id in nodes_index:
        com_linear[nodes_index[n_id]] = dict_communities[n_id]

    modularity = community.modularity(dict_communities, network)

    utils.saveGraphImage(partition_reference, com_linear, modularity, network, pos, network_name, algorithm_name, outputdir)

    utils.saveCluster(com_linear, algorithm_name, network_name, outputdir)
