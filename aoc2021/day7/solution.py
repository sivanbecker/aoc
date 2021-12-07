from collections import defaultdict
from types import BuiltinMethodType
class DailyClass:
    def __init__(self, fh_iter):
        self._fh_iter = fh_iter
        self.positions = defaultdict(int)
        self.costs = {}
        self.top = None
        self.bottom = None

    def digest_input(self):
        for p in next(self._fh_iter).strip().split(","):
            self.positions[int(p)] += 1
        self.top = max(self.positions)
        self.bottom = min(self.positions)

    def arithmetic_series_cost(self, start, end):
        a1 = 1
        an = abs(end - start)
        n = abs(end-start)
        return (a1+an) * n / 2

    def calc_part2_costs(self):
        ''' this one uses arithemtic series cost'''
        for xi in range(self.bottom, self.top+1):
            self.costs[xi] = sum([self.arithmetic_series_cost(xi, xj)*self.positions[xj] for xj in self.positions if xj != xi])

    def calc_all_costs(self):
        for xi in self.positions:
            self.costs[xi] = sum([abs(xi-xj)*self.positions[xj] for xj in self.positions if xj != xi])

    def solve_part1(self):
        ''' cost per move is 1 '''
        self.digest_input()
        self.calc_all_costs()
        return min(self.costs.values())

    def solve_part2(self):
        ''' cost increases for each additional move making it a '''
        self.digest_input()
        self.calc_part2_costs()
        return min(self.costs.values())