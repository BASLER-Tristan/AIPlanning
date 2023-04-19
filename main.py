from src.parser.pddlparser import PDDLParser
from src.graphplan.graphplan import GraphPlan
from src.a_star.a_star import AStar

if __name__ == "__main__":
    domain_file = "data/groupe1/domain.pddl"
    problem_file = "data/groupe1/problem0.pddl"

    domain = PDDLParser.parse(domain_file)
    problem = PDDLParser.parse(problem_file)

    # gp = GraphPlan(domain, problem, problem.initial_state)
    # gp.build()
    # print(gp.compute_heuristic())

    a = AStar(domain, problem, with_back_cost=False)
    path = a.solve()
    for p in path:
        print(p.sig)
