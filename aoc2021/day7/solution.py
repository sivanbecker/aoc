from collections import defaultdict
class DailyClass:
    def __init__(self, fh_iter):
        self._fh_iter = fh_iter
        self.positions = defaultdict(int)
        self.costs = {}

    def digest_input(self):
         for p in next(self._fh_iter).strip().split(","):
             self.positions[int(p)] += 1

    def calc_all_costs(self):
        for xi in self.positions:
            self.costs[xi] = sum([abs(xi-xj)*self.positions[xj] for xj in self.positions if xj != xi])

    def solve_part1(self):
        self.digest_input()
        self.calc_all_costs()
        print(self.costs)
        return min(self.costs.values())

    def solve_part2(self):
        return "Not Impl"