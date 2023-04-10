from dataclasses import dataclass
from typing import List, Dict

from src.parser.parser import PDDL_Parser


@dataclass
class Object:
    name: str
    type: str = "object"

    def __repr__(self) -> str:
        return self.name

    def __hash__(self) -> int:
        return hash(self.name)


class ObjectDict:
    def __init__(self, parser: PDDL_Parser):
        self.by_types = {}
        for type in parser.objects:
            self.by_types[type] = [Object(name, type) for name in parser.objects[type]]
        self.by_names = {}
        for type in self.by_types:
            for obj in self.by_types[type]:
                self.by_names[obj.name] = obj

    def __repr__(self) -> str:
        return str(self.by_types)


@dataclass
class Literal:
    predicate_name: str
    params: List[Object]
    positive: bool = True

    def __post_init__(self):
        self.effects_of = set()
        self.preconditions_of = set()

    def __repr__(self) -> str:
        params_str = ""
        for param in self.params:
            params_str += param.name
            params_str += ", "
        params_str = params_str[:-2]
        return f"{'' if self.positive else '-'}{self.predicate_name}({params_str})"

    def __neg__(self):
        return Literal(self.predicate_name, self.params, not self.positive)

    def __hash__(self) -> int:
        return hash((self.predicate_name, *self.params, self.positive))


@dataclass
class Action:
    action_name: str
    params: Dict[str, Object]

    def __post_init__(self):
        self.preconditions = set()
        self.effects = set()

    def __repr__(self) -> str:
        params_str = ""
        for param in self.params:
            params_str += f"{param}: {self.params[param].name}"
            params_str += ", "
        params_str = params_str[:-2]
        return f"{self.action_name}({params_str})"

    def __hash__(self) -> int:
        return hash((self.action_name, *self.params.items()))
