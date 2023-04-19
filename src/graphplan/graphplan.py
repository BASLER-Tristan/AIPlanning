from typing import Tuple, Iterator, List, Set
import itertools

from src.parser.domain import Domain
from src.parser.problem import Problem, State
from src.graphplan.classes import PredicateNode, GroundedActionNode, NullActionNode
from src.utils import get_equivalent


class GraphPlan:
    def __init__(self, domain: Domain, problem: Problem, initial_state: State):
        # Input parameters
        self.domain = domain
        self.problem = problem
        self.initial_state = initial_state
        # Internal variables
        self.states = [
            set([PredicateNode(predicate) for predicate in initial_state.predicates])
        ]
        self.actions = []

    def build(self) -> None:
        while not self.is_goal_reached():
            self.add_new_layer()

    def add_new_layer(self) -> None:
        new_actions = set()
        new_states = set()
        for grounded_action in self.get_all_grounded_actions():
            possible, preconditions = self.is_possible_action(grounded_action)
            if possible:
                self.update_new_action(
                    grounded_action, preconditions, new_actions, new_states
                )
        self.add_null_actions(new_actions, new_states)
        self.update_level(new_states)
        assert len(new_states) > len(self.states[-1])  # Avoid infinite loops
        self.actions.append(new_actions)
        self.states.append(new_states)

    def get_all_grounded_actions(self) -> Iterator[GroundedActionNode]:
        for a in self.domain.actions:
            possible_values = {
                arg_name: self.problem.initial_state.objects[type]
                for type, arg_name in zip(a.types, a.arg_names)
            }
            for instance in (
                dict(zip(possible_values, x))
                for x in itertools.product(*possible_values.values())
            ):
                args = [instance[arg_name] for arg_name in a.arg_names]
                yield GroundedActionNode(a, *args)

    def is_possible_action(
        self, grounded_action: GroundedActionNode
    ) -> Tuple[bool, List[PredicateNode]]:
        res = []
        for precondition in grounded_action.preconditions.pos_preconditions:
            pn = PredicateNode(precondition)
            if pn in self.states[-1]:
                res.append(get_equivalent(self.states[-1], pn))
            else:
                return False, None
        return True, res

    def update_new_action(
        self,
        grounded_action: GroundedActionNode,
        preconditions: List[PredicateNode],
        new_actions: Set[GroundedActionNode],
        new_states: Set[PredicateNode],
    ) -> None:
        # Update new_actions
        new_actions.add(grounded_action)
        # Update new_states
        effects = [
            PredicateNode(effect) for effect in grounded_action.effects.add_effects
        ]
        new_states.update(effects)
        # Update links
        for precondition in preconditions:
            precondition.next.add(grounded_action)
        for effect in effects:
            get_equivalent(new_states, effect).previous.add(grounded_action)
        grounded_action.previous.update(preconditions)
        grounded_action.next.update(effects)

    def add_null_actions(
        self,
        new_actions: Set[GroundedActionNode],
        new_states: Set[PredicateNode],
    ) -> None:
        for s in self.states[-1]:
            # Update new_actions
            a = NullActionNode()
            new_actions.add(a)
            # Update new_states
            new_states.add(s)
            s_new = get_equivalent(new_states, s)
            # Update links
            s.next.add(a)
            s_new.previous.add(a)
            a.previous.add(s)
            a.next.add(s)

    def update_level(
        self,
        new_states: Set[PredicateNode],
    ) -> None:
        for s in new_states:
            if s in self.states[-1]:
                s.level = get_equivalent(self.states[-1], s).level
            else:
                s.level = len(self.states)

    def is_goal_reached(self) -> bool:
        for goal in self.problem.goals:
            if PredicateNode(goal) not in self.states[-1]:
                return False
        return True

    def compute_heuristic(self):
        if len(self.states) == 1:
            return 0
        heuristic = 0
        reached = set(self.states[0])
        goals = set([p for p in self.states[-1] if p.predicate in self.problem.goals])
        new_goals = set()  # future goals of the previous level
        while len(goals) > 0:
            # Compute the cost of the actions that reach a goal
            possible_actions = {}
            for goal in goals:
                for action in goal.previous:
                    if not isinstance(action, NullActionNode):
                        if action not in possible_actions:
                            cost = sum([p.level for p in action.previous])
                            possible_actions[action] = cost
            # Take action with minimal cost
            min_cost = min(possible_actions.values())
            actions = [
                action
                for action in possible_actions
                if possible_actions[action] == min_cost
            ]
            action = actions.pop()
            heuristic += 1
            # Update goals, new_goals and reached
            for effect in action.next:
                goals.discard(effect)
                reached.add(effect)
            for precondition in action.previous:
                if precondition not in reached:
                    new_goals.add(precondition)
            # If all goals are satisfied, go to previous level
            if len(goals) == 0 and len(new_goals) > 0:
                goals.update(new_goals)
                new_goals = set()

        return heuristic
