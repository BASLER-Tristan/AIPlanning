from typing import List, Tuple
import os

DATA_FOLDER = "data"
GROUP_DOMAIN = {
    "groupe1": "domain.pddl",
    "groupe2": "domain.pddl",
    "groupe3": "domain.pddl",
    "groupe4": "freecell_domain.pddl",
}


def get_domains(group: str = "all") -> List[str]:
    if group == "all":
        return [os.path.join(DATA_FOLDER, x, GROUP_DOMAIN[x]) for x in GROUP_DOMAIN]
    elif group in GROUP_DOMAIN:
        return [os.path.join(DATA_FOLDER, group, GROUP_DOMAIN[group])]
    else:
        raise ValueError("Group not found")


def get_problems(group: str = "all") -> List[str]:
    if group == "all":
        return [
            os.path.join(DATA_FOLDER, x, file)
            for x in GROUP_DOMAIN
            for file in os.listdir(os.path.join(DATA_FOLDER, x))
            if file != GROUP_DOMAIN[x]
        ]
    elif group in GROUP_DOMAIN:
        return [
            os.path.join(DATA_FOLDER, group, file)
            for file in os.listdir(os.path.join(DATA_FOLDER, group))
            if file != GROUP_DOMAIN[group]
        ]
    else:
        raise ValueError("Group not found")


def get_all_domain_problem() -> List[Tuple[str, str]]:
    return [
        (get_domains(group=x)[0], problem)
        for x in GROUP_DOMAIN
        for problem in get_problems(group=x)
    ]


# See https://code.activestate.com/recipes/499299/ (How to access an element of a set using an equivalent object?)


class _CaptureEq:
    'Object wrapper that remembers "other" for successful equality tests.'

    def __init__(self, obj):
        self.obj = obj
        self.match = obj

    def __eq__(self, other):
        result = self.obj == other
        if result:
            self.match = other
        return result

    def __getattr__(
        self, name
    ):  # support hash() or anything else needed by __contains__
        return getattr(self.obj, name)

    def __hash__(self) -> int:
        return hash(self.obj)


def get_equivalent(container, item, default=None):
    """Gets the specific container element matched by: "item in container".

    Useful for retreiving a canonical value equivalent to "item".  For example, a
    caching or interning application may require fetching a single representative
    instance from many possible equivalent instances).

    >>> get_equivalent(set([1, 2, 3]), 2.0)             # 2.0 is equivalent to 2
    2
    >>> get_equivalent([1, 2, 3], 4, default=0)
    0
    """
    t = _CaptureEq(item)
    if t in container:
        return t.match
    return default
