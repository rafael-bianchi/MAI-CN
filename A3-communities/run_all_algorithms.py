from A3_project.community_dect_alg1 import run_community_dect_alg1
from A3_project.community_dect_alg2 import run_community_dect_alg2
from A3_project.community_dect_alg3 import run_community_dect_alg3
from A3_project.utils import utils

outputdir = 'A3_project/output/'

networks = utils.readNetworks()

metrics = {}

for network in networks:
    metric = {}
    metric['Clauset-Newman-Moore'] = run_community_dect_alg1(network['network'], network['pos'], network['network_name'], network['partition_reference'],outputdir)
    metric['Louvain'] = run_community_dect_alg2(network['network'], network['pos'], network['network_name'], network['partition_reference'],outputdir)
    metric['Infomap'] = run_community_dect_alg3(network['network'], network['network_igraph'], network['pos'], network['network_name'], network['partition_reference'],outputdir)

    network['metrics'] = metric

    if (network['partition_reference'] != None):
        utils.saveGraphImageReference(network['network'], network['pos'], network['network_name'], network['partition_reference'], outputdir)
    
utils.saveMetrics(networks, outputdir)