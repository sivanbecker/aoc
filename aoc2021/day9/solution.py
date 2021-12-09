
import numpy as np

class DailyClass:
    def __init__(self, fh_iter):
        self._fh_iter = fh_iter
        self.arr = None
        self.h = None
        self.w = None
        self.lows = {}

    def digest_input(self):
        m = map(lambda line: tuple(line.strip()), self._fh_iter)
        self.arr = np.array(list(m), dtype=int)

    def gen_lows(self):
        self.h, self.w = self.arr.shape
        for hi in range(self.h):
            for wi in range(self.w):
                print(hi,wi)
                self.test_local_low(hi,wi)

    def test_local_low(self, hi, wi):
        # hi-1, wi
        # hi+1, wi
        # hi, wi-1
        # hi, wi-1
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
        print(f"{hi}, {wi}, {self.w}")
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

    def solve_part1(self):
        self.digest_input()
        self.gen_lows()
        print(self.lows)
        return self.calc_risk()

    def solve_part2(self):
        return "Not Impl"