
import numpy as np
from collections import defaultdict
class DailyClass:
    def __init__(self, fh_iter):
        self._fh_iter = fh_iter
        self.arr = None
        self.h = None
        self.w = None
        self.lows = {}
        self.basins = defaultdict(list)
        self.visited = defaultdict(bool)
        

    def digest_input(self):
        m = map(lambda line: tuple(line.strip()), self._fh_iter)
        self.arr = np.array(list(m), dtype=int)

    def find_lows(self):
        self.h, self.w = self.arr.shape
        for hi in range(self.h):
            for wi in range(self.w):
                self.test_local_low(hi,wi)

    def test_local_low(self, hi, wi):
        if self.test_up(hi, wi) and self.test_down(hi,wi) and \
            self.test_left(hi,wi) and self.test_right(hi,wi):
            self.lows[(hi,wi)] = self.arr[hi,wi]

    def test_up(self, hi, wi):
        if hi-1 >= 0:
            return self.arr[hi,wi] < self.arr[hi-1, wi]
        return True

    def test_down(self, hi, wi):
        if hi+1 < self.h:
            return self.arr[hi,wi] < self.arr[hi+1, wi]
        return True

    def test_right(self, hi, wi):
        if wi+1 < self.w:
            return self.arr[hi,wi] < self.arr[hi, wi+1]
        return True

    def test_left(self, hi, wi):
        if wi-1 >= 0:
            return self.arr[hi,wi] < self.arr[hi, wi-1]
        return True

    def calc_risk(self):
        r = 0
        for v in self.lows.values():
            r += v+1
        return r

    def low_dig_basin(self, hi, wi):
        ''' recursive '''
        points = []
        # hi, wi = low
        if hi > self.h-1 or wi > self.w-1 or hi < 0 or wi < 0:
            return []
        if self.arr[hi,wi] == 9:
            return []
        if (hi, wi) in self.visited:
            return []
        self.visited[(hi,wi)] = True
        points.append((hi, wi))
        points.extend(self.low_dig_basin(hi-1, wi))
        points.extend(self.low_dig_basin(hi+1, wi))
        points.extend(self.low_dig_basin(hi, wi-1))
        points.extend(self.low_dig_basin(hi, wi+1))
        return points

    def find_basins(self):
        for l in self.lows:
            self.basins[l] = self.low_dig_basin(*l)
            
    def mult_basins_size(self):
        sizes = []
        for b in self.basins:
            sizes.append(len(self.basins[b]))
        from functools import reduce
        return reduce(lambda a,b: a*b, sorted(sizes)[-3:], 1)

    def solve_part1(self):
        self.digest_input()
        self.find_lows()
        return self.calc_risk()

    def solve_part2(self):
        self.digest_input()
        self.find_lows()
        self.find_basins()
        return self.mult_basins_size()
        