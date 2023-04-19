from dataclasses import dataclass
from typing import Tuple

from src.parser.domain import _GroundedAction


@dataclass
class PredicateNode:
    predicate: Tuple[str, str, str]

    def __post_init__(self):
        self.previous = set()
        self.next = set()
        self.level = 0

    def __repr__(self) -> str:
        params_str = ""
        for param in self.predicate[1:]:
            params_str += param
            params_str += ", "
        params_str = params_str[:-2]  # Remove last ", "
        return f"{self.predicate[0]}({params_str})"

    def __hash__(self) -> int:
        return hash(self.predicate)


class GroundedActionNode(_GroundedAction):
    def __init__(self, action, *args, static_predicates=[]):
        super().__init__(action, *args, static_predicates=static_predicates)
        self.previous = set()
        self.next = set()


class NullActionNode:
    num: int = 0

    def __init__(self) -> None:
        self.previous = set()
        self.next = set()
        self.id = NullActionNode.num
        NullActionNode.num += 1

    def __repr__(self) -> str:
        return "()"

    def __hash__(self) -> int:
        return hash(self.id)
