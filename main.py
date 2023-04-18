from src.parser.parser import *
from src.graphplan.classes import *
from src.graphplan.graphplan import *
from src.HillClimbingGraph.State import *

if __name__ == "__main__":
    domain = "data/groupe1/domain.pddl"
    problem = "data/groupe1/problem0.pddl"
    parser = PDDL_Parser()
    parser.parse_domain(domain)
    parser.parse_problem(problem)
    parser.print_domain_problem()
    gp = GraphPlan(parser)
    gp.build()
    state = State(parser=parser,
                  domain=domain,
                  problem=problem)
    neigh = state.neighborhood()
    print("finish")
    # print(len(gp.actions))
    # print(len(gp.states[-1]))
