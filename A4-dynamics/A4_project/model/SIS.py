import random
import copy

class SIS():
    
    def __init__(self, network):
        self.network = network
        self.beta = None
        self.recover_prob = None
        self.p_0 = None
        self.iteration = None
        self.infected_count = None

    def is_node_infected(self, node):
        #TODO Remove assert
        assert(node in self.node_status)
        return self.node_status[node]

    def set_initial_status(self, beta, recover_prob, p_0):
        self.beta = beta #Infection rate
        self.recover_prob = recover_prob #Recovery rate
        self.p_0 = p_0 #initial fraction of infected nodes
        self.node_status = {}
        self.iteration = 0
        self.infected_count = 0

        for node in self.network:
            #TODO Remove assert
            assert(node not in self.node_status)

            #node_status[node] = True(Infected) or False(Susceptible)
            self.node_status[node] = random.random() < self.p_0
            self.infected_count += 1 if self.node_status[node] else 0 
        
    def iterate(self):
        current_node_status =  copy.deepcopy(self.node_status)
        self.infected_count = 0
        
        for node, currently_infected in current_node_status.items():
            # For each infected node at time step t, we recover it with probability µ: we generate
            # a uniform random number between 0.0 and 1.0, and if the value is lower than µ
            # the state of that node in the next time step t+1 will be susceptible, otherwise it will
            # remain being infected.
            if(currently_infected):
                #If random is < than recover probability, set as NOT infected
                self.node_status[node] = not (random.random() < self.recover_prob)

            # For each susceptible node at time step t, we traverse all of its neighbors. For each
            # infected neighbor (at time step t), the reference node becomes infected with
            # probability β. 
            else:
                for neighbor in self.network.neighbors(node):
                    if(current_node_status[neighbor] and random.random() < self.beta):
                        self.node_status[node] = True
                        break
        
            self.infected_count += 1 if self.node_status[node] else 0

        self.iteration += 1

        current_node_status = None

        return self.infected_count  / len(self.network), self.iteration
