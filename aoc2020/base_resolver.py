import os
import importlib
import click
import subprocess
from initializer import INPUT_FILES



class BaseSolver:
    def __init__(self):
        pass
        # if os.path.isfile(input_file):
        #     self.input = input_file
        # else:
        #     raise IOError(f"Input file {input_file} does not exist")

    def _input_iter(self):
        with open(self.input, "r") as fh:
            for line in fh:
                yield line.strip()

    def part1(self, *args, **kw):
        self.input = "input1.txt"
        if not os.path.isfile("input1.txt"):
            raise IOError(f"Input file {self.input} does not exist")

        print("PART1 Not Implemented")

    def part2(self, *args, **kw):
        self.input = "input2.txt"
        if not os.path.isfile("input1.txt"):
            raise IOError(f"Input file {self.input} does not exist")
        print("PART2 Not Implemented")


class Solver(BaseSolver):
    def __init__(self, day_number, year=None, test=False):
        assert year, f"Please insert the year !!"
        self.year = year
        self.aoc_module = f"aoc{year}"
        self.basepath = f"{os.path.abspath('.')}/aoc{year}"
        self.day = day_number
        self.solver_module = None
        self.test = test
        super().__init__()

    def _day_importer(self, part):
        """ day is an integer, part can be 1 or 2"""
        assert isinstance(
            int(self.day), int
        ), f"Day must be an integer. but i got >> {self.day} <<"
        try:
            return importlib.import_module(f"day{self.day}.solution")

        except ModuleNotFoundError as exc:
            if "No module named" in exc.__str__():
                click.secho(
                    f"Day {self.day} directory or its modules were not created yet ({exc.__str__()})",
                    fg="red",
                )
                raise click.Abort

    # def test(self, day, part):
    #     click.secho(f"\nRunning Day {self.day} tests\n", fg="yellow")
    #     os.environ["DAY"] = self.day
    #     os.environ["YEAR"] = str(self.year)
    #     pytest_args = [
    #         "pytest",
    #         f"{self.basepath}/tests/tests.py",
    #         "-s",
    #         "-vvv",
    #         "-k",
    #         f"example{part}",
    #     ]
    #     print(f"About to run pytest cmd: {' '.join(pytest_args)}")
    #     subprocess.run(pytest_args)

    @property
    def run(self):
        return self

    def _input_iter(self, inp="input.txt"):
        daily_input_file = f"{self.basepath}/day{self.day}/{inp}"
        assert os.path.isfile(
            daily_input_file
        ), f"Failed finding file {daily_input_file}"
        with open(daily_input_file, "r") as fh:
            for line in fh:
                yield line.strip()

    def part1(self, inp=""):
        """ inp = input to solve"""
        inp = INPUT_FILES['testcase']['part1'] if self.test else INPUT_FILES['real']['part1']
        self.solver_module = self._day_importer("1")
        return self.solver_module.DailyClass(self._input_iter(inp=inp)).solve_part1()

    def part2(self, inp=""):
        """ inp = input to solve"""
        inp = INPUT_FILES['testcase']['part2'] if self.test else INPUT_FILES['real']['part2']
        self.solver_module = self._day_importer("2")
        return self.solver_module.DailyClass(self._input_iter(inp=inp)).solve_part2()

    # def run_test1(self, inp="input1_testcase.txt"):
    #     """ inp = input to solve"""
    #     self.solver_module = self._day_importer("")
    #     return self.solver_module.DailyClass(self._input_iter(inp=inp)).solve_part1()

    # def run_test2(self, inp="input2_testcase.txt"):
    #     """ inp = input to solve"""
    #     self.solver_module = self._day_importer("")
    #     return self.solver_module.DailyClass(self._input_iter(inp=inp)).solve_part2()