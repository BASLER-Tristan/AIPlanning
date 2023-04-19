# PlanAuto

## Description

This project aims at solving a pddl problem. For this purpose, we implemented a method that uses both A* and the heuristic of FastForward. This is part of the automated planning course of CentraleSupélec.

## Team Members

- Tristan Basler
- Vivien Conti
- Guillaume Dugat
- Xavier Jeunot

## Structure of the repository

The repository is composed of a `main.py` to run the project, a folder `data` to store the problems and domains pddl files, a `src` folder with the parser, the graphplan part to compute the heuristic and the a_star part to run A* (plus a folder HillClimbingGraph that is not used anymore), as well as a `test` folder for pytest.

## Installation

To use the project, we advise to use python 3.10 in a virtual environment. To install the dependancies, run :

```
make install
```

## Usage

To compute a solution of a planification problem, run :
```
make run
```

To change the domain or the problem to solve, the file main.py can be modified in the section under `if __name__ == "__main__:"`, with the desired file name. Moreover, our algorithm can work in two different ways: the cost in A* is either `g(n) + h(n)` or `h(n)`, where `g(n)` is the length of the path from the initial state to `n` and `h(n)` is the heuristic of FastForward. The first behaviour is obtained with `with_back_cost = True`, while the second is obtained with `with_back_cost = False` (in the same parameters section as before).

Last but not least, some tests are implemented and can be run with :
```
make pytest
```
