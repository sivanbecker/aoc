import os
import subprocess
from pprint import pprint

import click

from base_resolver import Solver

INFO_FILE = "info.txt"


def test_examples():
    assert 1 == 1


class BootstrapError(Exception):
    pass


@click.group()
def cli():
    pass


@cli.command()
def info():
    with open(INFO_FILE, "r") as fh:
        print(*fh.readlines(), sep="\n")


@cli.command()
@click.option("--day", "--day-number", "day", help="number of the day to solve")
@click.option("--part", "part", help="part1 or part2", default=1)
@click.option("--year", "year", help="advent of code specific year", default=2020)
def solve(day, part, year):

    solver = Solver(day, year=year)

    print(solver.run.part1()) if part == 1 else print(solver.run.part2())


@cli.command()
@click.option("--day", "--day-number", "day", help="number of the day to test")
@click.option("--part", "part", help="part1 or part2", default=1)
@click.option("--year", "year", help="advent of code specific year", default=2020)
def test(day, part, year):
    
    solver = Solver(day, year=year)
    solver.test(day, part)


@cli.command()
@click.option("--day", "--day-number", "day", help="number of the day to init")
def init(day):
    files2create = [
        "input1.txt",
        "input2.txt",
        "dummy_input1.txt",
        "dummy_input2.txt",
        "dummy_solution1.txt",
        "dummy_solution2.txt",
    ]
    subprocess.run(["mkdir", f"day{day}"])
    subprocess.run(["cp", "solution.template", f"day{day}/solution.py"])
    for _file in files2create:
        subprocess.run(["touch", f"day{day}/{_file}"])


if __name__ == "__main__":
    cli(obj={})
