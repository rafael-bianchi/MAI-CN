import datetime

import networkx as nx

import A4_project.model.SIS as sis
from A4_project.utils import utils

#β (at least 51 values, Δβ=0.02)
n_betas = 51
delta_b = .02

#different values of the recovery probability μ (e.g. 0.1, 0.5, 0.9)
recover_probabilities = [0.1, 0.5, 0.9]

#initial fraction of infected nodes
p_0 = 0.2

#number of repetitions of the simulation
n_rep = 100

#maximum number of time steps of each simulation
t_max = 1000 

#number of steps of the transitory
t_trans = 900

networks_paths = ['A4_project/networks/real/PGP.net', #largest network
            'A4_project/networks/model/SF_1000_g2.7.net', 
            'A4_project/networks/model/ER1000k8.net']

#networks_paths = ['A4_project/networks/model/SF_500_g2.7.net']


for network_path in networks_paths:
    #networkx
    network = utils.read_network(network_path)
    
    s = sis.SIS(network)
    betas = utils.generate_betas(n_betas, delta_b)
    for recover_probability in recover_probabilities:
        ps = []
        for beta in betas:
            print(f'{datetime.datetime.now()} - {network_path} -  mu {recover_probability} - beta {str(beta)} - started')
            #Monte Carlo
            p_beta = 0
            for _ in range(n_rep):
                s.set_initial_status(beta, recover_probability, p_0)
                
                sim = []

                for _ in range(t_max):
                    p, _ = s.iterate()
                    sim.append(p)
                
                stationary = sim[t_trans:]
                p_beta += sum(stationary)/len(stationary)

            ps.append(p_beta/n_rep)
            
            print(f'{datetime.datetime.now()} - {network_path} -  mu {recover_probability} - beta {str(beta)} - ended - {str(p_beta/n_rep)}') 

        utils.plot(network_path, ps, betas, recover_probability, p_0)
