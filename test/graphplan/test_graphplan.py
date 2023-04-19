from src.parser.pddlparser import PDDLParser
from src.graphplan.graphplan import GraphPlan
from src.utils import get_domains, get_problems


def test_graphplan():
    group = "groupe1"
    domain_file = get_domains(group=group)[0]
    problem_file = get_problems(group=group)[0]
    domain = PDDLParser.parse(domain_file)
    problem = PDDLParser.parse(problem_file)
    gp = GraphPlan(domain, problem, problem.initial_state)
    gp.build()
    gp.compute_heuristic()
