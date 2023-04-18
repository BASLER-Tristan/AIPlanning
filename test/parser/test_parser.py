from src.parser.pddlparser import PDDLParser
from src.utils import get_all_domain_problem


def test_parser():
    for (domain_file, problem_file) in get_all_domain_problem():
        print(domain_file, problem_file)
        domain = PDDLParser.parse(domain_file)
        problem = PDDLParser.parse(problem_file)
