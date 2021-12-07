AdvantOfCode - all years

* Using poetry so please run poetry install after cloning the repo.

* copy the inputs manually to the right input files the init script created + manually write the expected output for each testcase part1/2 in the right files.

Once the yearly folder is created use these commands (using year 2021 for the example):

1. init daily folder: `poetry run python aoc2021/aocli.py init --day <day number>`
2. run part 1 testcase after writing a solution: `poetry run python aoc2021/aocli.py solve --day 1 --part 1 --year 2021 --test`
3. run solution part1 with real input (just remove --test flag): `poetry run python aoc2021/aocli.py solve --day 1 --part 1 --year 2021`

### Using Makefile to init/test/solve:

- *init*: make day=<> init
- *test*: make day=<> part=<1 or 2> test
- *solve*: make day=<> part=<1 or 2> solve

## -> for other then year 2021 ,Makefile and commands above should be updated !!! 