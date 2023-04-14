# ******************************************************************************************************************** #
# ********************************************* #   CENTRALESUPELEC   # ********************************************** #
# ******************************************************************************************************************** #
# Project : planauto
# File    : Graph.py
# PATH    : src/HillClimbingGraph
# Author  : trisr
# Date    : 14/04/2023
# Description :
"""




"""
# Last commit ID   :
# Last commit date :
# ******************************************************************************************************************** #
# ******************************************************************************************************************** #
# ******************************************************************************************************************** #


# ******************************************************************************************************************** #
# Importations
import numpy as np

# ******************************************************************************************************************** #
# Function definition
class HCgraph:
    def __init__(self, init_state):
        """

        Parameters
        ----------
        init_state
        """
        self.init_state = init_state
        self.current_state = init_state
        self.plan = []
        self.states_plan = [init_state]
        self.finish = False
        self.graph = {}
        self.states_values = {}
        self.closed_states = set()

    def next_state(self, method="min"):
        """

        Parameters
        ----------
        method

        Returns
        -------

        """
        ### Check if the state is solution
        if self.current_state.is_solution():
            self.finish = True

        ### Calcul the neighborhood of the current state
        state_neighborhood, actions = self.current_state.neighborhood()

        ### Clean the neighborhood state
        state_neighborhood = [state for state in state_neighborhood if not (state in self.closed_states)]
        if len(state_neighborhood) == 0:
            self.close_branch()
        else:
            ### Update Graph
            self.graph[self.current_state] = [state for state in state_neighborhood]

            ### Init the research
            next_state = None
            index_action = 0
            if method == "min":
                next_state_score = np.inf
            else:
                next_state_score = -np.inf

            for state in state_neighborhood:
                ### Calcul the score of the state
                if state in self.states_values.keys():
                    state_score = self.states_values[state]
                else:
                    state_score = state.eval()
                    self.states_values[state] = state_score

                ### Determine if the state is better than the previous one selected
                if method == "min":
                    if state.eval() < next_state_score:
                        next_state_score = state_score
                        next_state = state
                        action = actions[index_action]
                else:
                    if state.eval() > next_state_score:
                        next_state_score = state_score
                        next_state = state
                        action = actions[index_action]

                ### Update variable for action index
                index_action += 1

            self.current_state = next_state
            self.plan.append(action)
            self.states_plan.append(next_state)

    def close_branch(self):
        """
        Manage the closing of the branch.
        1. Remove last action and last state
        2. Save the status of the state
        3. Define the new state and the new plan

        Inplace function
        -------

        """

        ### Removing last action and last state
        self.plan.pop()
        self.states_plan.pop()

        ### Saving the closed state
        self.closed_states.add(self.current_state)

        ### Current state is the previous of the action
        if len(self.states_plan) > 0:
            self.current_state = self.states_plan[-1]
        else:
            ### No existing plan
            self.finish = True

    def solve_problem(self):
        """

        Returns
        -------

        """
        if self.init_state.is_solution():
            print("Init State is solution, [] is returned")
            return []

        while not (self.finish):
            self.next_state()

        if len(self.plan) > 0:
            return self.plan
        else:
            print("No existing solution, None is returned")
            return None


# ******************************************************************************************************************** #
# Main
if __name__ == "__main__":
    solver = HCgraph(init_state=State)
    plan = solver.solve_problem()
