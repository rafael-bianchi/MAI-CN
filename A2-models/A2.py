
#%%
import networkx as nx
import matplotlib.pyplot as plt
import itertools
import random
import math
import numpy as np

#%% [markdown]
# #### Erdös-Rényi (ER) networks

#%%
def erdos_renyi_gen(n,p):
    net = nx.Graph()
    for node in range(0,n):
        net.add_node(node)
    
    for ini in range(0,n):
        for end in range(ini+1, n):
            if (p > 0 and random.random() <= p):
                net.add_edge(ini, end)
    return net

def erdos_renyi_gen_plot(n,p):
    net = erdos_renyi_gen(n, p)

    # nx.draw(net)
    # plt.show()

    # Actual average degree
    k = sum([d[1] for d in net.degree()])/n
    
    # Theoretical average degree
    k_ = p*(n-1)
    
    h = nx.degree_histogram(net)

    plt.plot(np.asarray(h)/float(sum(h)), 'o-', label='Experimental distribution')
    plt.axvline(x=k, ls='dashed', label='Experimental <k>=%f' % k)
    plt.plot([math.exp(-k_)*k_**i/math.factorial(i) for i in range(len(h))], 'o-', color='r', label='Theoretical distribution')
    plt.axvline(x=k_, color='r', ls='dashed', label='Theoretical <k>=%f' % k_)
    plt.legend(loc=2)
    plt.xlabel('Degree')
    plt.ylabel('P(k)')
    plt.title('ER: N=%d, p=%f' % (n,p))
    plt.show() 

#%% [markdown]
# #### Watts-Strogatz model (WS)

#%%
def watts_strogatz_gen(n, k, p):
    if (k >= n): 
        raise Exception('Invalid value for k. k must be less than n')

    net = nx.Graph()
    k_2 = math.floor(k / 2)
    edge_list = []

    for node in range(0,n):
        for node_pos_shift in range(1, k_2 + 1):
            edge_list.append([node, (node + node_pos_shift) % n])

    net.add_edges_from(edge_list)

    for edge in edge_list:
        if (p > 0 and random.random() < p):
            new_to = random.randint(0, n-1)

            while new_to == edge[1] or net.has_edge(edge[0], new_to):
                new_to = random.randint(0, n-1)

            if net.degree(edge[0]) >= n - 1:
                break
            else:
                net.remove_edge(edge[0], edge[1])
                net.add_edge(edge[0], new_to)
    
    return net

#%% [markdown]
# ##### Barabási-Albert model (BA)

#%%
def barabasi_albert_gen(n, m0, m):

    if (m0 > n):
        raise Exception('m0 must be equal or less than n.')

    if (m > m0):
        raise Exception('m must be equal or less than m0.')

    net = nx.Graph()

    for node in range(0,m0):
        #print(f'Adding node {node}')
        net.add_node(node)

    #Randomly connect them. At least one connection per node.
    for node in range(0,m0):
        if (net.degree(node) < m0 - 1):
            targets = list(range(0, m0))
            random.shuffle(targets)
            for node_to in targets:
                if (node != node_to and not net.has_edge(node, node_to) and net.degree(node_to) < m0):
                    #print (f'Adding edge {node} to {node_to}')
                    net.add_edge(node, node_to)
                    break
    while m0 < n:    
        distr_degree = []
        for degree in net.degree():
            distr_degree += [degree[0]] * degree[1]

        for _ in range(0, m):
            node = random.choice(distr_degree)
            distr_degree = [item for item in distr_degree if item != node]

            net.add_node(m0)
            net.add_edge(m0, node)     
        m0 += 1

    return net

#%% ER
for n in [50, 100]:
    for p in [.2, .5, .7]:
        net = erdos_renyi_gen(n, p)
        nx.write_pajek(net, f'./output/ER_n_{n}_p_{100*p}.net')

#%% WS
for n in [50, 100]:
    for p in [0, .1, .2, .5, 0.9, 1.0]:
        watts_strogatz_gen(n, 4, p)
        nx.write_pajek(net, f'./output/WS_n_{n}_p_{100*p}.net')

#%% BA
for n in [100]:
    for m in [1, 2, 5]:
        barabasi_albert_gen(n, n//2, m)
        nx.write_pajek(net, f'./output/BA_n_{n}_m_{m}_m0_{n//2}.net')


#%%
erdos_renyi_gen_plot(10, 1)




#%%
def ER_network(N, p):
    G = nx.Graph()
    G.add_nodes_from(range(N))
    for i in range(0, N):
        for j in range(i+1, N):
            if random.random() < p or p == 1:
                G.add_edge(i,j)
    return G

N = 10000
p = .001
G = ER_network(N, p)
nx.draw(G)
plt.show()

# plot distribution

#%%
k = 2.*len(G.edges())/N             # experimental <k>
k_ = p*(N-1)                        # theoretical <k>
h = nx.degree_histogram(G)
plt.plot(np.asarray(h)/float(sum(h)), 'o-', label='Experimental distribution')
plt.axvline(x=k, ls='dashed', label='Experimental <k>=%f' % k)
plt.plot([math.exp(-k_)*k_**i/math.factorial(i) for i in range(len(h))], 'o-', color='r', label='Theoretical distribution')
plt.axvline(x=k_, color='r', ls='dashed', label='Theoretical <k>=%f' % k_)
plt.legend(loc=2)
plt.xlabel('Degree')
plt.ylabel('P(k)')
plt.title('ER: N=%d, p=%f' % (N,p))
plt.show()

#%%