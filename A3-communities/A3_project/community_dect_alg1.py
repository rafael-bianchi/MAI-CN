import networkx as nx
import community
from .utils import utils

def run_community_dect_alg1(network, pos, network_name, partition_reference, outputdir):
    """
    Finds communities in a graph using the Clauset-Newman-Moore greedy modularity maximization method

    networkx greedy_modularity_communities method.
    """
    
    algorithm_name = 'Clauset-Newman-Moore'
    print(f'Starting greedy_modularity_communities for {network_name}')

    nodes_index = {}

    for node_name, node in network.node.items(): 
        nodes_index[node_name] = int(node['id'])-1

    com_grouped = nx.algorithms.community.greedy_modularity_communities(network)
    com_linear = [None] * len(network)

    com_dict = {}

    idx_community = 0
    for comm in com_grouped:
        for node in comm:
            com_dict[node] = idx_community
            com_linear[nodes_index[node]] = idx_community
        idx_community = idx_community + 1

    modularity = community.modularity(com_dict, network)

    danon, nvi, ji = utils.saveGraphImage(partition_reference, com_linear, modularity, network, pos, network_name, algorithm_name, outputdir)

    utils.saveCluster(com_linear, algorithm_name, network_name, outputdir)

    return modularity, danon, nvi, ji
