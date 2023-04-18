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
from typing import List, Tuple
from src.graphplan.classes import *
from src.graphplan.graphplan import GraphPlan
import itertools
from src.utils import *

# ******************************************************************************************************************** #
# Class definition
class State:
    def __init__(
        self, parser, domain, problem,
    ):
        self.parser = parser
        self.problem = problem
        self.domain = domain
        self.objects = ObjectDict(self.parser)
        self.state = self.get_initial_state()

    def get_initial_state(self):
        res = set()
        for lit in self.parser.state:
            params = [self.objects.by_names[name] for name in lit[1:]]
            res.add(Literal(lit[0], params))
        return res

    def neighborhood(self):
        new_actions = []
        new_states = set()
        new_actions_c = []
        for action in self.parser.actions:
            possible_values = {param[0]: self.objects.by_types[param[1]] for param in action.parameters}
            # See https://stackoverflow.com/questions/5228158/cartesian-product-of-a-dictionary-of-lists

            ### Determine if the action is possible
            possible = True

            for positive_precondition in action.positive_preconditions:
                for lit in self.state:
                    if lit.predicate_name == positive_precondition[0]:
                        if lit.positive:
                            for params in positive_precondition[1:]:
                                if not (params) in possible_values.keys():
                                    possible = False

            for negative_precondition in action.negative_preconditions:
                for lit in self.state:
                    if lit.predicate_name == positive_precondition[0]:
                        if (lit.positive):
                                possible = False

            if possible:
                new_actions.append(action)

        for action in new_actions:
            possible_values = {param[0]: self.objects.by_types[param[1]] for param in action.parameters}
            combinations = create_combination_dict(possible_values)
            for combination in combinations:
                new_state = self.apply_actions(
                    action,
                    combination
                )
                action_c = [action,combination]
                new_actions_c.append(action_c)
                new_states.add(new_state)
        return new_actions_c, new_states

    def apply_actions(self,action,combinaison):
        new_state = State(
            parser=self.parser,
            domain=self.domain,
            problem=self.problem
        )

        new_state_state = set()

        for lit in self.state:
            impacted = False
            for add_effect in action.add_effects:
                if add_effect[0] == lit.predicate_name:
                    impacted=True
                    new_lit = Literal(add_effect[0], [combinaison[x] for x in add_effect[1:]], True)
                    new_state_state.add(new_lit)

            for del_effect in action.add_effects:
                if del_effect[0] == lit.predicate_name:
                    impacted=True
                    new_lit = Literal(add_effect[0], [combinaison[x] for x in add_effect[1:]], False)
                    new_state_state.add(new_lit)

            if not impacted:
                new_state_state.add(lit)

        new_state.state = new_state_state
        return new_state

    def eval(self):
        raise NotImplemented
        return score

    def is_solution(self):
        raise NotImplemented
        return bool

    def __hash__(self):
        list_state = list(self.state)
        combined_hash = list_state[0].__hash__()
        for lit in list_state[1:]:
            combined_hash = combined_hash ^ lit.__hash__()
        return combined_hash

# ******************************************************************************************************************** #
# Configuration
"""
state hash function 
state.eval()
state.neighborhood()
state.is_solution()
"""
