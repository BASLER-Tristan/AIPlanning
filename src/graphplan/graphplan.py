from typing import Tuple, Set
import itertools

from src.graphplan.classes import *
from src.parser.parser import PDDL_Parser
from src.utils import get_equivalent


class GraphPlan:
    def __init__(self, parser: PDDL_Parser):
        self.parser = parser
        self.objects = ObjectDict(self.parser)
        self.states = [self.get_initial_state()]
        self.actions = []

    def get_initial_state(self) -> Set[Literal]:
        res = set()
        for lit in self.parser.state:
            params = [self.objects.by_names[name] for name in lit[1:]]
            res.add(Literal(lit[0], params))
        return res

    def build(self):
        new_actions, new_states = self.get_new_actions_states()
        self.add_null_actions(new_actions, new_states)
        if self.stabilisation_test(new_states):
            return
        else:
            self.update_states_preconditions_of(new_actions)
            self.actions.append(new_actions)
            self.states.append(new_states)
            self.build()

    def get_new_actions_states(self) -> Tuple[Set[Action], Set[Literal]]:
        new_actions = set()
        new_states = set()
        for action in self.parser.actions:
            possible_values = {
                param[0]: self.objects.by_types[param[1]] for param in action.parameters
            }
            # See https://stackoverflow.com/questions/5228158/cartesian-product-of-a-dictionary-of-lists
            for instance in (
                dict(zip(possible_values, x))
                for x in itertools.product(*possible_values.values())
            ):  # Try all possible tuples of objects with correct type
                yes = True
                action_preconditions = []
                for (preconditions, positive) in [
                    (action.positive_preconditions, True),
                    (action.negative_preconditions, False),
                ]:
                    if not yes:
                        break
                    for precondition in preconditions:
                        if not yes:
                            break
                        lit = Literal(
                            precondition[0],
                            [instance[var] for var in precondition[1:]],
                            positive,
                        )
                        if lit in self.states[-1]:
                            lit = get_equivalent(self.states[-1], lit)
                            action_preconditions.append(lit)
                        else:
                            yes = False
                if yes:  # All preconditions are ok
                    new_action = Action(action.name, instance)
                    new_action.preconditions.update(action_preconditions)
                    new_actions.add(new_action)
                    # Effects
                    action_effects = []
                    for (effects, positive) in [
                        (action.add_effects, True),
                        (action.del_effects, False),
                    ]:
                        for effect in effects:
                            lit = Literal(
                                effect[0],
                                [instance[var] for var in effect[1:]],
                                positive,
                            )
                            if lit in new_states:
                                lit = get_equivalent(new_states, lit)
                            else:
                                new_states.add(lit)
                            lit.effects_of.add(new_action)
                            action_effects.append(lit)
                    new_action.effects.update(action_effects)

        return new_actions, new_states

    def add_null_actions(
        self, new_actions: Set[Action], new_states: Set[Literal]
    ) -> Tuple[Set[Action], Set[Literal]]:
        for lit in self.states[-1]:
            if lit in new_states:
                new_lit = get_equivalent(new_states, lit)
            else:
                new_lit = Literal(lit.predicate_name, lit.params, lit.positive)
                new_states.add(new_lit)
            new_action = Action("", {})
            new_actions.add(new_action)
            new_action.preconditions.add(lit)
            new_action.effects.add(new_lit)
            new_lit.effects_of.add(new_action)

    def stabilisation_test(self, new_states: Set[Literal]) -> bool:
        # Literals are increasing
        return len(self.states[-1]) == len(new_states)

    def update_states_preconditions_of(self, new_actions: Set[Action]) -> None:
        for action in new_actions:
            for lit in action.preconditions:
                lit.preconditions_of.add(action)
