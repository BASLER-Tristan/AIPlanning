from src.parser.parser import *
from src.graphplan.graphplan import *
from src.utils import *


def test_build_graphplan():
    group = "groupe1"
    domain = get_domains(group=group)[0]
    for problem in get_problems(group=group):
        parser = PDDL_Parser()
        parser.parse_domain(domain)
        parser.parse_problem(problem)
        gp = GraphPlan(parser)
        gp.build()
