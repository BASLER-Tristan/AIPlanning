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
