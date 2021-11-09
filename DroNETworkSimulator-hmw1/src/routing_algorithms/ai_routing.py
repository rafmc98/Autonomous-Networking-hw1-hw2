
import numpy as np
from src.utilities import utilities as util
from src.routing_algorithms.BASE_routing import BASE_routing
import  random
from matplotlib import pyplot as plt
class AIRouting(BASE_routing):
    def __init__(self, drone, simulator):
        BASE_routing.__init__(self, drone, simulator)
        # random generator
        self.rnd_for_routing_ai = np.random.RandomState(self.simulator.seed)
        self.taken_actions = {}  #id event : (old_action)
        self.actions_rewards={}
        self.epsilon=10
        
    def feedback(self, drone, id_event, delay, outcome):
        """ return a possible feedback, if the destination drone has received the packet """
        # Packets that we delivered and still need a feedback
        #----------------------print(self.drone.identifier, "----------", self.taken_actions)
        # outcome == -1 if the packet/event expired; 0 if the packets has been delivered to the depot
        # Feedback from a delivered or expired packet
        print(self.drone.identifier, "----------", drone, id_event, delay, outcome)
        # Be aware, due to network errors we can give the same event to multiple drones and receive multiple feedback for the same packet!!
        # NOTE: reward or update using the old action!!
        # STORE WHICH ACTION DID YOU TAKE IN THE PAST.
        # do something or train the model (?)
        if id_event in self.taken_actions:
            action = self.taken_actions[id_event]
            del self.taken_actions[id_event]
   
    def relay_selection(self, opt_neighbors, pkd):
        """ arg min score  -> geographical approach, take the drone closest to the depot """

        # Only if you need --> several features:
        cell_index = util.TraversedCells.coord_to_cell(size_cell=self.simulator.prob_size_cell,
                                                      width_area=self.simulator.env_width,
                                                       x_pos=self.drone.coords[0],  # e.g. 1500
                                                        y_pos=self.drone.coords[1])[0]  # e.g. 500
        #print(cell_index)
        if self.drone.identifier not in set([0,1,2]):
            #Initialization of the reward dictionaty if the element (cell,neighboor) is not stored yet
            if (cell_index,None) not in self.actions_rewards:
                self.actions_rewards[(cell_index,None)]=-1
            for d in [v[1] for v in opt_neighbors]:
                if d.identifier not in self.actions_rewards:
                    self.actions_rewards[(cell_index,d.identifier)]=-1
                    
            action=None
            print(self.drone.identifier,self.actions_rewards)
            # self.drone.history_path (which waypoint I traversed. We assume the mission is repeated)
            # self.drone.residual_energy (that tells us when I'll come back to the depot).
            #  .....
            # Store your current action --- you can add several stuff if needed to take a reward later
            self.taken_actions[pkd.event_ref.identifier] = (action)
            #Check if random choice 
            isRandomChoice=random.choices([True,False],weights=(self.epsilon,90),k=1)[0]
            if isRandomChoice:
                print("Random choice")
                opt_neighbors=[v[1] for v in opt_neighbors]
                drone= self.simulator.rnd_routing.choice([v[1] for v in opt_neighbors])
               # print("I'm "+str(self.drone.identifier),str([v[1] for v in opt_neighbors])+" at cell: ",cell_index)
                action=drone.identifier
                return None
            return None
        return None

                

    def print(self):
        """
            This method is called at the end of the simulation, can be usefull to print some
                metrics about the learning process
        """
        pass
