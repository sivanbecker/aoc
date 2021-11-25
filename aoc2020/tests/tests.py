import os

import pudb
from ..base_resolver import Solver

assert "DAY" in os.environ, "Missing DAY envvar"
assert "YEAR" in os.environ, "Missing YEAR envvar"
_DAY = os.environ["DAY"]
_YEAR = os.environ["YEAR"]
# try:
#     _DAY = os.environ["DAY"]
#     _YEAR = os.environ["YEAR"]
# except KeyError:
#     print()
#     exit(1)

def test_example1():
    day = _DAY
    year = _YEAR
    
    solver = Solver(day, year)
    DUMMY_INPUT_FILE = os.path.realpath(f"{solver.basepath}/day{day}/dummy_input1.txt")
    DUMMY_SOLUTION_FILE = os.path.realpath(f"{solver.basepath}/day{day}/dummy_solution1.txt")
    assert os.path.isfile(DUMMY_INPUT_FILE), f"Missing {DUMMY_INPUT_FILE}"
    assert os.path.isfile(DUMMY_SOLUTION_FILE), f"Missing {DUMMY_SOLUTION_FILE}"
    answer = solver.run.run_test1()
    with open(DUMMY_SOLUTION_FILE, "r") as fhout:
        assert str(answer) == fhout.readline().strip() 


def test_example2():
    day = _DAY
    year = _YEAR
    solver = Solver(day, year)
    DUMMY_INPUT_FILE = os.path.realpath(f"{solver.basepath}/day{day}/dummy_input2.txt")
    DUMMY_SOLUTION_FILE = os.path.realpath(f"{solver.basepath}/day{day}/dummy_solution2.txt")
    answer = solver.run.run_test2()
    with open(DUMMY_SOLUTION_FILE, "r") as fhout:
        assert str(answer) == fhout.readline().strip()