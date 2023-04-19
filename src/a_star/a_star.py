from typing import Iterator, List
import itertools
import time

from src.parser.domain import Domain, _GroundedAction
from src.parser.problem import Problem, State
from src.graphplan.graphplan import GraphPlan

Path = List[_GroundedAction]


class AStar:
    def __init__(self, domain: Domain, problem: Problem, with_back_cost: bool = True):
        # Input parameters
        self.domain = domain
        self.problem = problem
        self.with_back_cost = with_back_cost
        # Internal variables
        self.current_state = problem.initial_state
        self.priority = {
            self.current_state: {"path": [], "cost": self.compute_heuristic()}
        }
        self.visited = set()

    def get_all_grounded_actions(self) -> Iterator[_GroundedAction]:
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
                yield _GroundedAction(a, *args)

    def is_possible_action(self, grounded_action: _GroundedAction) -> bool:
        for precondition in grounded_action.preconditions.pos_preconditions:
            if precondition not in self.current_state.predicates:
                return False
        for precondition in grounded_action.preconditions.neg_preconditions:
            if precondition in self.current_state.predicates:
                return False
        return True

    def compute_heuristic(self) -> int:
        gp = GraphPlan(self.domain, self.problem, self.current_state)
        gp.build()
        res = gp.compute_heuristic()
        return res

    def update_priority(self, current_path: Path) -> None:
        if self.current_state in self.priority:
            len_current = len(current_path)
            len_old = len(self.priority[self.current_state]["path"])
            if len_current < len_old:
                self.priority[self.current_state]["path"] = current_path
                if self.with_back_cost:
                    self.priority[self.current_state]["cost"] -= len_old
                    self.priority[self.current_state]["cost"] += len_current
        else:
            heuristic = self.compute_heuristic()
            self.priority[self.current_state] = {
                "path": current_path,
                "cost": len(current_path) + heuristic
                if self.with_back_cost
                else heuristic,
            }

    def get_next_state(self) -> State:
        min_cost = None
        min_state = None
        for state in self.priority:
            cost = self.priority[state]["cost"]
            if min_cost is None or cost < min_cost:
                min_cost = cost
                min_state = state
        return min_state

    def explore(self) -> None:
        for action in self.get_all_grounded_actions():
            if self.is_possible_action(action):
                current_state = self.current_state
                path = self.priority[self.current_state]["path"]
                # Move forward
                self.current_state = self.current_state.apply(action)
                if self.current_state not in self.visited:
                    self.update_priority(path + [action])
                # Move backward
                self.current_state = current_state
        self.visited.add(self.current_state)
        self.priority.pop(self.current_state)

    def is_reached_goal(self) -> bool:
        for predicate in self.problem.goals:
            if predicate not in self.current_state.predicates:
                return False
        return True

    def solve(self):
        t0 = time.time()
        while not self.is_reached_goal():
            self.explore()
            self.current_state = self.get_next_state()
            path = self.priority[self.current_state]["path"]
            cost = self.priority[self.current_state]["cost"]
            print(
                f"Cost: {cost}, Path length: {len(path)}, Heuristic: {cost - len(path) if self.with_back_cost else cost}, Time: {time.time() - t0:.2f}"
            )
        return path
