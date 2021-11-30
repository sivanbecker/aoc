import click
import subprocess
import os
import pathlib


INPUT_FILES = {
    "testcase": {"part1": "input1_testcase.txt", "part2": "input2_testcase.txt"},
    "real": {"part1": "input1.txt", "part2": "input2.txt"},
}
OUTPUT_FILES = {
    "testcase": {"part1": "output1_testcase.txt", "part2": "output2_testcase.txt"},
    "real": {"part1": "output1.txt", "part2": "output2.txt"},
}

SOLUTION_PYTHON_CODE_TEMPLATE = f"{os.path.dirname(__file__)}/solution.template"


class Initializer:
    """
    day directory
    input files
    solution output files
    solution file from template
    """

    CUR_DIR = os.path.dirname(__file__)

    def __init__(self, day: str):
        self.day = day
        self.day_dir = None

    def init_daily_dir(self):
        click.secho(f"Init daily dir day{self.day}", fg="green")
        self.day_dir = f"{self.CUR_DIR}/day{self.day}"
        subprocess.run(["mkdir", "-p", self.day_dir])

    def init_input_files(self):
        click.secho(f"Init input files", fg="green")
        for _file in INPUT_FILES['testcase'].values():
            subprocess.run(["touch", f"{self.day_dir}/{_file}"])
        for _file in INPUT_FILES['real'].values():
            subprocess.run(["touch", f"{self.day_dir}/{_file}"])

    def init_solution_files(self):
        click.secho(f"Init solution files", fg="green")
        for _file in OUTPUT_FILES['testcase'].values():
            subprocess.run(["touch", f"{self.day_dir}/{_file}"])
        for _file in OUTPUT_FILES['real'].values():
            subprocess.run(["touch", f"{self.day_dir}/{_file}"])

    def init_solution_code_file(self):
        click.secho(f"Init solution python file", fg="green")
        subprocess.run(["cp", SOLUTION_PYTHON_CODE_TEMPLATE, f"{self.day_dir}/solution.py"])

    def all(self):
        self.init_daily_dir()
        self.init_input_files()
        self.init_solution_files()
        self.init_solution_code_file()