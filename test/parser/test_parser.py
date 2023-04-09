from src.parser.parser import *
from src.utils import *


def test_parser():

    for (domain, problem) in get_all_domain_problem():
        # TODO
        if "groupe2" in domain:
            continue
        if "groupe3" in domain:
            continue
        parser = PDDL_Parser()
        parser.parse_domain(domain)
        parser.parse_problem(problem)
