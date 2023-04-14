# ******************************************************************************************************************** #
# ********************************************* #   CENTRALESUPELEC   # ********************************************** #
# ******************************************************************************************************************** #
# Project : planauto
# File    : State.py
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
from typing import List,Tuple

# ******************************************************************************************************************** #
# Class definition
class State:
    def __init__(self,Problem):
        self.problem = Problem


    def neighborhood(self) -> Tuple[List[State],List[Action]]:
        raise NotImplemented
        state_neighborhood, actions = None,None
        return state_neighborhood, actions


    def eval(self) -> float :
        raise NotImplemented
        return score

    def is_solution(self) -> bool:
        raise NotImplemented
        return bool

    def __hash__(self):
        raise NotImplemented

# ******************************************************************************************************************** #
# Configuration
"""
state hash function 
state.eval()
state.neighborhood()
state.is_solution()
"""

# ******************************************************************************************************************** #
# Main
if __name__ == "__main__":
    pass
