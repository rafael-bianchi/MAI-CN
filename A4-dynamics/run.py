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
n_rep = 10 #100

#maximum number of time steps of each simulation
t_max = 100 #1000 

#number of steps of the transitory
t_trans = 90 #900

networks_paths = ['A4_project/networks/real/PGP.net', 
            'A4_project/networks/model/SF_1000_g2.7.net', 
            'A4_project/networks/model/ER1000k8.net']

networks_paths = ['A4_project/networks/model/SF_500_g2.7.net']


for network_path in networks_paths:
    #networkx
    network = utils.read_network(network_path)
    
    s = sis.SIS(network)
    betas = utils.generate_betas(n_betas, delta_b)
    for recover_probability in recover_probabilities:
        p_sequence = []
        for beta in betas:
            #Monte Carlo
            p_final = 0
            for rep in range(n_rep):
                s.set_initial_status(beta, recover_probability, p_0)
                p_simulation = []
                for j in range(t_max):
                    p, _ = s.iterate()
                    p_simulation.append(p)

                stationary_p = p_simulation[t_trans:]
                mean_p = sum(stationary_p)/len(stationary_p)
                p_final += mean_p
                # get the initial state for next rep

            p_final = p_final/n_rep
            p_sequence.append(p_final)
            
            print(f'{network_path} -  mu {recover_probability} - beta {str(beta)}') 
        


        utils.plot(network_path, p_sequence, betas, recover_probability, p_0)