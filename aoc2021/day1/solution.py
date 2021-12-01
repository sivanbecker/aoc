from collections import deque
class DailyClass:
    def __init__(self, fh_iter):
        self._fh_iter = fh_iter

    def sum_increased(self, _iterable):
        count_deeper = 0
        prev = None
        curr = None
        for l in _iterable:
            curr = l
            if not prev is None and int(curr) > int(prev):
                count_deeper += 1
            prev = curr
        return count_deeper

    def solve_part1(self):
        return self.sum_increased(self._fh_iter)

    def solve_part2(self):
        threes = deque()
        sums = []
        for e in self._fh_iter:
            if len(threes) == 3:
                sums.append(sum(threes))
                threes.popleft()

            threes.append(int(e))
        sums.append(sum(threes))
        
        return self.sum_increased(sums)