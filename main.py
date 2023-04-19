import time

from src.parser.pddlparser import PDDLParser
from src.a_star.a_star import AStar, verify
from src.graphplan.classes import GroundedActionNode


def main(domain_file: str, problem_file: str, with_back_cost: bool = True) -> None:
    # Initialization
    domain = PDDLParser.parse(domain_file)
    problem = PDDLParser.parse(problem_file)

    # Computation of the solution
    t0 = time.time()
    a = AStar(domain, problem, with_back_cost=with_back_cost)
    path = a.solve()
    delta_time = time.time() - t0

    # Verification
    assert verify(domain, problem, path)

    # Print results
    print("\n############   Results   ############")
    print("Solution :")
    for p in path:
        print(p.sig)
    print(f"Length of the solution: {len(path)}")
    print(f"Computation time: {delta_time:.2f}s")


if __name__ == "__main__":
    ##############     Parameters can be changed here     ##############
    domain_file = "data/groupe1/domain.pddl"
    problem_file = "data/groupe1/problem0.pddl"
    with_back_cost = True
    ####################################################################

    main(domain_file, problem_file, with_back_cost=with_back_cost)
