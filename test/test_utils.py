from src.utils import *


def test_get_domains():
    get_domains()
    res = get_domains(group="groupe1")
    assert len(res) == 1
    assert res[0] == "data/groupe1/domain.pddl"


def test_get_problems():
    get_problems()
    res = get_problems(group="groupe1")
    assert "data/groupe1/domain.pddl" not in res
    assert "data/groupe1/problem0.pddl" in res
    assert "data/groupe1/problem1.pddl" in res
    assert "data/groupe1/problem2.pddl" in res
    assert "data/groupe1/problem3.pddl" in res
    assert len(res) == 4


def test_get_all_domain_problem():
    get_all_domain_problem()
