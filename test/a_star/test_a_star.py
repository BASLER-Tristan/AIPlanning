from src.parser.pddlparser import PDDLParser
from src.a_star.a_star import AStar


def test_a_star():
    domain_file = "data/groupe1/domain.pddl"
    problem_file = "data/groupe1/problem0.pddl"
    domain = PDDLParser.parse(domain_file)
    problem = PDDLParser.parse(problem_file)
    a = AStar(domain, problem, with_back_cost=True)
    a.solve()
    a2 = AStar(domain, problem, with_back_cost=False)
    a2.solve()
