from src.parser.pddlparser import PDDLParser
from src.graphplan.graphplan import GraphPlan

# from src.HillClimbingGraph.State import *

if __name__ == "__main__":
    domain_file = "data/groupe1/domain.pddl"
    problem_file = "data/groupe1/problem0.pddl"

    domain = PDDLParser.parse(domain_file)
    problem = PDDLParser.parse(problem_file)

    gp = GraphPlan(domain, problem, problem.initial_state)
    gp.build()
    print(gp.compute_heuristic())
