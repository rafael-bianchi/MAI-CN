import os

import matplotlib.pyplot as plt
import networkx as nx

def plot(network_path, p_sequence, betas, recover_probability, p_0):
    netname = os.path.splitext(os.path.basename(network_path))[0]
    directory = os.path.join('A4_project/output/', 'images', netname)
    
    if not os.path.exists(directory):
        os.makedirs(directory)

    out_file = os.path.join(directory,f'{netname}-{str(recover_probability)}.png') 
    
    plt.plot(betas, p_sequence, 'o-')
    plt.xlabel('β')
    plt.ylabel('P')
    plt.title(netname + ', SIS(μ=%.1f, P0=%.1f)' % (recover_probability, p_0))
    plt.savefig(out_file)
    plt.close()

def generate_betas(n_betas = 51, delta_b = .02):
    betas = [0.0]
    for i in range(1,n_betas):
        betas.append(delta_b + betas[i-1])

    return betas

def read_network(path):
    pajek = nx.read_pajek(path)
    net = nx.Graph(pajek)

    return net
